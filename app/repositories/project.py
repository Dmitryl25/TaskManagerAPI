from .base import BaseRepository
from sqlalchemy.ext.asyncio import AsyncSession
from ..schemas.project import ProjectCreate
from uuid import UUID
from ..models.project import Project
from sqlalchemy import select

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

    async def get_workspace_projects(self, workspace_id: UUID) -> List[Project]:
        projects = await self.session.execute(select(Project).where(Project.workspace_id == workspace_id))
        return projects.scalars().all()

    async def update(self):
        pass
    async def delete(self):
        pass
