from .base import BaseRepository
from sqlalchemy.ext.asyncio import AsyncSession
from ..schemas.task import TaskCreate
from uuid import UUID
from ..models.task import Task
from sqlalchemy import select

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
                                project_id: UUID) -> List[Task]:
        tasks = await self.session.execute(select(Task).where(Task.project_id == project_id))
        return tasks.scalars().all()

    async def delete(self):
        pass

    async def update(self):
        pass