from .base import BaseRepository
from ..models.token import Token
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update
from uuid import UUID
from datetime import datetime, timezone


class TokenRepository(BaseRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, user_id: UUID,
                     token_hash: str, expires_at: datetime) -> Token:
        new_token = Token(user_id=user_id,
                          token_hash=token_hash,
                          expires_at=expires_at)
        self.session.add(new_token)
        await self.session.commit()
        await self.session.refresh(new_token)
        return new_token

    async def get_by_hash(self, token_hash: str) -> Token | None:
        token =await self.session.execute(select(Token)
                                          .where(Token.token_hash == token_hash))
        return token.scalar_one_or_none()

    async def revoke(self, token_id: UUID) -> None:
        await self.session.execute(update(Token)
                                   .where(Token.id == token_id)
                                   .values(revoked_at=datetime.now(timezone.utc)))
        await self.session.commit()

    async def update(self, **kwargs):
        pass

    async def delete(self, **kwargs):
        pass

    async def get_by_id(self, id: UUID):
        pass

