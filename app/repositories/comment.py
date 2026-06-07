from .base import BaseRepository
from sqlalchemy.ext.asyncio import AsyncSession
from ..schemas.comment import CommentCreate, CommentUpdate
from ..models.comment import Comment
from sqlalchemy import select, update, delete
from typing import Sequence
from uuid import UUID


class CommentRepository(BaseRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self,
                     task_id: UUID,
                     author_id: UUID,
                     data: CommentCreate) -> Comment:
        new_comment = Comment(**data.model_dump(),
                              author_id=author_id,
                              task_id=task_id)
        self.session.add(new_comment)
        await self.session.commit()
        await self.session.refresh(new_comment)
        return new_comment

    async def get_by_id(self,
                        id: UUID) -> Comment:
        comment = await self.session.execute(select(Comment)
                                             .where(Comment.id == id))
        return comment.scalar_one_or_none()

    async def get_task_comments(self,
                                task_id: UUID) -> Sequence[Comment]:
        comments = await self.session.execute(select(Comment)
                                              .where(Comment.task_id == task_id))
        return comments.scalars().all()

    async def update(self,
                     comment_id: UUID,
                     data: CommentUpdate) -> Comment:
        await self.session.execute(update(Comment)
                                   .where(Comment.id == comment_id)
                                   .values(data.model_dump(exclude_none=True)))
        await self.session.commit()
        return await self.get_by_id(comment_id)

    async def delete(self,
                     comment_id: UUID):
        await self.session.execute(delete(Comment)
                                   .where(Comment.id == comment_id))
        await self.session.commit()