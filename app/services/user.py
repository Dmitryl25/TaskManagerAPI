from sqlalchemy.ext.asyncio import AsyncSession
from ..schemas.user import UserCreated
from fastapi import HTTPException, status
from ..repositories.user import UserRepository
from uuid import UUID
from ..models.user import User


# Класс для бизнес-логики пользователя
class UserService:

    def __init__(self, session: AsyncSession):
        self.repository = UserRepository(session)

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
