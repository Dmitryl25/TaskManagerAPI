from .base import BaseRepository
from sqlalchemy.ext.asyncio import AsyncSession
from ..schemas.project import ProjectCreate, ProjectUpdate
from uuid import UUID
from ..models.project import Project
from sqlalchemy import select, update, delete
from typing import List, Sequence

class ProjectRepository(BaseRepository):
    def __init__(self,
                 session: AsyncSession):
        self.session = session

    async def create(self,
               project: ProjectCreate,
               workspace_id: UUID,
               owner_id: UUID) -> Project:
        new_project = Project(workspace_id=workspace_id,
                              name=project.name,
                              description=project.description,
                              key=project.key,
                              owner_id=owner_id)
        self.session.add(new_project)
        await self.session.commit()
        await self.session.refresh(new_project)

        return new_project

    async def get_by_id(self, id: UUID) -> Project:
        project = await self.session.execute(select(Project).where(Project.id == id))
        return project.scalar_one_or_none()

    async def get_workspace_projects(self, workspace_id: UUID) -> Sequence[Project]:
        projects = await self.session.execute(select(Project).where(Project.workspace_id == workspace_id))
        return projects.scalars().all()

    async def update(self,
                     project_id: UUID,
                     data: ProjectUpdate) -> Project:
        await self.session.execute(update(Project)
                                   .where(Project.id == project_id)
                                   .values(data.model_dump(exclude_none=True)))
        await self.session.commit()
        return await self.get_by_id(project_id)

    async def delete(self,
                     project_id: UUID):
        await self.session.execute(delete(Project).where(Project.id == project_id))
        await self.session.commit()
