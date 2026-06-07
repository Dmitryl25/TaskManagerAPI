from sqlalchemy.ext.asyncio import AsyncSession
from ..schemas.user import UserCreated, UserUpdate
from fastapi import HTTPException, status
from ..repositories.user import UserRepository
from uuid import UUID
from ..models.user import User
from ..models.token import Token
from ..core.security import verify_password, create_refresh_token, create_access_token, decode_token
from ..repositories.token import TokenRepository
import hashlib
from datetime import datetime, timezone, timedelta
from ..core.config import settings


# Класс для бизнес-логики пользователя
class UserService:

    def __init__(self, session: AsyncSession):
        self.repository = UserRepository(session)
        self.token_rep = TokenRepository(session)

    # регистрация пользователя
    async def register(self, user: UserCreated) -> User:
        result = await self.repository.get_user_by_email(str(user.email))
        if result:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail="Пользователь с таким email уже существует")
        user_register = await self.repository.create(user)
        return user_register

    # получение пользователя по id
    async def get_user_by_id(self, user_id: UUID) -> User:
        user = await self.repository.get_by_id(user_id)
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail="Пользователя с таким id не существует")
        return user

    async def login(self, user: UserCreated) -> tuple[User, str]:
        user_db = await self.repository.get_user_by_email(str(user.email))
        if not user_db:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                detail="Неверные данные")
        if not verify_password(user.password, user_db.hashed_password):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

        refresh_token = create_refresh_token(user_id=user_db.id)
        hash_token = hashlib.sha256(refresh_token.encode()).hexdigest()
        token = await self.token_rep.create(user_id=user_db.id,
                                            token_hash=hash_token,
                                            expires_at=datetime.now(timezone.utc) + timedelta(days=settings.jwt.refresh_token_expire_days))

        return user_db, refresh_token

    async def update_user(self, user_id: UUID, data: UserUpdate) -> User:
        await self.get_user_by_id(user_id)
        return await self.repository.update(user_id=user_id,
                                            data=data)

    async def refresh(self, refresh_token: str):
        decoded_token = decode_token(refresh_token)

        if not decoded_token or decoded_token["type"] != "refresh":
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
        token: Token = await self.token_rep.get_by_hash(hashlib.sha256(refresh_token.encode()).hexdigest())

        if not token or token.revoked_at is not None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

        await self.token_rep.revoke(token.id)
        new_refresh_token = create_refresh_token(token.user_id)
        await self.token_rep.create(user_id=token.user_id,
                                    token_hash=hashlib.sha256(new_refresh_token.encode()).hexdigest(),
                                    expires_at=datetime.now(timezone.utc) + timedelta(days=settings.jwt.refresh_token_expire_days))
        return create_access_token(user_id=token.user_id), new_refresh_token

    async def logout(self, refresh_token: str):
        decoded_token = decode_token(refresh_token)

        if not decoded_token or decoded_token["type"] != "refresh":
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
        token: Token = await self.token_rep.get_by_hash(hashlib.sha256(refresh_token.encode()).hexdigest())

        if not token or token.revoked_at is not None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
        await self.token_rep.revoke(token.id)