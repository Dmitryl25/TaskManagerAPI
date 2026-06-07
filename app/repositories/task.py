from .base import BaseRepository
from sqlalchemy.ext.asyncio import AsyncSession
from ..schemas.task import TaskCreate, TaskUpdate, TaskFilter
from uuid import UUID
from ..models.task import Task
from sqlalchemy import select, update, delete
from typing import Sequence

class TaskRepository(BaseRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self,
                     task: TaskCreate,
                     project_id: UUID,
                     reporter_id: UUID) -> Task:
        new_task = Task(**task.model_dump(),
                        project_id=project_id,
                        reporter_id=reporter_id)
        self.session.add(new_task)
        await self.session.commit()
        await self.session.refresh(new_task)
        return new_task

    async def get_by_id(self,
                        task_id: UUID) -> Task:
        task = await self.session.execute(select(Task).where(Task.id == task_id))
        return task.scalar_one_or_none()

    async def get_project_tasks(self,
                                project_id: UUID,
                                filters: TaskFilter) -> Sequence[Task]:
        query = select(Task).where(Task.project_id == project_id)

        if filters.status:
            query = query.where(Task.status == filters.status)

        if filters.priority:
            query = query.where(Task.priority == filters.priority)

        if filters.assignee_id:
            query = query.where(Task.assignee_id == filters.assignee_id)

        if filters.search:
            query = query.where(Task.title.ilike(f"%{filters.search}%"))

        tasks = await self.session.execute(query)

        return tasks.scalars().all()

    async def delete(self, task_id: UUID):
        await self.session.execute(delete(Task).where(Task.id == task_id))


    async def update(self,
                     task_id: UUID,
                     data: TaskUpdate) -> Task:
        await self.session.execute(update(Task)
                                   .where(Task.id == task_id)
                                   .values(data.model_dump(exclude_none=True)))
        await self.session.commit()
        return await self.get_by_id(task_id=task_id)
