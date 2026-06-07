from ..schemas.comment import CommentCreate, CommentUpdate
from sqlalchemy.ext.asyncio import AsyncSession
from ..repositories.comment import CommentRepository
from ..repositories.task import TaskRepository
from ..repositories.project import ProjectRepository
from ..repositories.workspace import WorkspaceRepository
from ..models.task import Task
from ..models.project import Project
from ..models.workspace import WorkSpace
from ..models.comment import Comment
from uuid import UUID
from typing import Sequence


from fastapi import HTTPException, status

class CommentService:
    def __init__(self, db: AsyncSession):
        self.comment_rep = CommentRepository(db)
        self.project_rep = ProjectRepository(db)
        self.task_rep = TaskRepository(db)
        self.workspace_rep = WorkspaceRepository(db)

    async def create_comment(self,
                             task_id: UUID,
                             auther_id: UUID,
                             data: CommentCreate):
        task: Task = await self.task_rep.get_by_id(task_id)
        if not task:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

        project: Project = await self.project_rep.get_by_id(task.project_id)

        member = await self.workspace_rep.get_member(user_id=auther_id,
                                                     workspace_id=project.workspace_id)
        if not member:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)

        return await self.comment_rep.create(task_id=task_id,
                                             author_id=auther_id,
                                             data=data)

    async def get_task_comments(self,
                                task_id: UUID,
                                user_id: UUID) -> Sequence[Comment]:
        task: Task = await self.task_rep.get_by_id(task_id)
        if not task:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

        project: Project = await self.project_rep.get_by_id(task.project_id)

        member = await self.workspace_rep.get_member(user_id=user_id,
                                                     workspace_id=project.workspace_id)
        if not member:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)

        return await self.comment_rep.get_task_comments(task_id=task_id)

    async def update_comment(self,
                             comment_id: UUID,
                             data: CommentUpdate,
                             user_id: UUID):
        comment: Comment = await self.comment_rep.get_by_id(comment_id)

        if not comment:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

        if comment.author_id != user_id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)

        return await self.comment_rep.update(comment_id=comment_id,
                                             data=data)

    async def delete_comment(self,
                             comment_id: UUID,
                             user_id: UUID):
        comment: Comment = await self.comment_rep.get_by_id(comment_id)

        if not comment:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

        if comment.author_id != user_id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)

        return await self.comment_rep.delete(comment_id=comment_id)







