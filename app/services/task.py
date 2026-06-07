from ..repositories.task import TaskRepository
from ..repositories.workspace import WorkspaceRepository
from ..repositories.project import ProjectRepository
from sqlalchemy.ext.asyncio import AsyncSession

from ..schemas.task import TaskCreate, TaskUpdate
from uuid import UUID

from fastapi import HTTPException, status

from ..models.project import Project
from ..models.workspace import WorkSpace
from ..models.task import Task


class TaskService:
    def __init__(self, db: AsyncSession):
        self.task_rep = TaskRepository(db)
        self.workspace_rep = WorkspaceRepository(db)
        self.project_rep = ProjectRepository(db)

    async def create(self,
                     task: TaskCreate,
                     project_id: UUID,
                     reporter_id: UUID) -> Task:
        project: Project = await self.project_rep.get_by_id(project_id)
        if not project:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
        user = await self.workspace_rep.get_member(reporter_id, project.workspace_id)
        if not user:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)
        new_task = await self.task_rep.create(task,
                                              project_id=project_id,
                                              reporter_id=reporter_id)
        return new_task

    async def get_by_id(self,
                        task_id: UUID,
                        user_id: UUID) -> Task:
        task: Task = await self.task_rep.get_by_id(task_id)
        if not task:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

        project: Project = await self.project_rep.get_by_id(task.project_id)
        user = await self.workspace_rep.get_member(user_id=user_id,
                                                   workspace_id=project.workspace_id)
        if not user:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)

        return task

    async def get_project_tasks(self,
                                project_id: UUID,
                                user_id: UUID):
        project: Project = await self.project_rep.get_by_id(project_id)
        if not project:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
        user = await self.workspace_rep.get_member(user_id=user_id,
                                                   workspace_id=project.workspace_id)
        if not user:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)

        return await self.task_rep.get_project_tasks(project_id)

    async def update_task(self,
                          task_id: UUID,
                          user_id: UUID,
                          data: TaskUpdate):
        task: Task = await self.task_rep.get_by_id(task_id)

        if not task:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

        project: Project = await self.project_rep.get_by_id(task.project_id)
        if not project:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
        user = await self.workspace_rep.get_member(user_id=user_id,
                                                   workspace_id=project.workspace_id)
        if not user:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)

        return await self.task_rep.update(task_id=task_id,
                                          data=data)

    async def delete_task(self,
                          task_id: UUID,
                          user_id: UUID):
        task: Task = await self.task_rep.get_by_id(task_id)
        if not task:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
        project: Project = await self.project_rep.get_by_id(task.project_id)
        if not project:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

        user = await self.workspace_rep.get_member(user_id=user_id,
                                                   workspace_id=project.workspace_id)
        if not user:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)

        await self.task_rep.delete(task_id=task_id)