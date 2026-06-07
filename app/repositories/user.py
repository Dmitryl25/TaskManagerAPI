from .base import BaseRepository
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID
from ..models.user import User
from sqlalchemy import select, update, delete
from ..schemas.user import UserCreated, UserUpdate
from ..core.security import hash_password


# Класс для python-логики (работа с БД) пользователя
class UserRepository(BaseRepository):

    def __init__(self, session: AsyncSession):
        self.session: AsyncSession = session


    # получение User-объекта по id
    async def get_by_id(self, id: UUID):
        user = await self.session.execute(select(User).where(User.id == id))
        return user.scalar_one_or_none()

    # получение User-объекта по email
    async def get_user_by_email(self, email: str):
        user = await self.session.execute(select(User).where(User.email == email))
        return user.scalar_one_or_none()

    # добавление записи в БД и возвращение User-объекта
    async def create(self, user: UserCreated) -> User:
        new_user = User(email=str(user.email),
                        hashed_password=hash_password(user.password))
        self.session.add(new_user)
        await self.session.commit()

        await self.session.refresh(new_user)
        return new_user

    async def update(self,
                     user_id: UUID,
                     data: UserUpdate) -> User:
        await self.session.execute(update(User)
                                   .where(User.id == user_id)
                                   .values(data.model_dump(exclude_none=True)))
        await self.session.commit()
        return await self.get_by_id(user_id)

    def delete(self):
        pass
