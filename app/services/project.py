from ..repositories.project import ProjectRepository
from sqlalchemy.ext.asyncio import AsyncSession
from ..schemas.project import ProjectCreate
from ..models.project import Project
from ..repositories.workspace import WorkspaceRepository

from fastapi import HTTPException, status

from uuid import UUID


class ProjectService:
    def __init__(self, session: AsyncSession):
        self.repository = ProjectRepository(session)
        self.workspace_repository = WorkspaceRepository(session)

    async def create(self, project: ProjectCreate,
                     workspace_id: UUID,
                     owner_id: UUID) -> Project:
        project = await self.repository.create(project=project,
                                               workspace_id=workspace_id,
                                               owner_id=owner_id)
        return project

    async def get_by_id(self,
                        project_id: UUID,
                        user_id: UUID):
        project: Project = await self.repository.get_by_id(id=project_id)

        if not project:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
        workspace_id = project.workspace_id
        member = await self.workspace_repository.get_member(user_id=user_id,
                                                            workspace_id=workspace_id)
        if not member:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)
        return project

    async def get_workspace_projects(self,
                                     workspace_id: UUID,
                                     user_id: UUID):

        workspace = await self.workspace_repository.get_by_id(workspace_id)

        if not workspace:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

        member = await self.workspace_repository.get_member(user_id=user_id,
                                                            workspace_id=workspace_id)
        if not member:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)

        projects = await self.repository.get_workspace_projects(workspace_id=workspace_id)
        if not projects:
            return []
        return projects




