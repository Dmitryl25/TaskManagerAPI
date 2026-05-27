from ..repositories.workspace import WorkspaceRepository
from sqlalchemy.ext.asyncio import AsyncSession
from ..schemas.workspace import WorkspaceCreate, WorkspaceUpdate
from uuid import UUID
from ..models.workspace import WorkSpace
from fastapi import status, HTTPException
from typing import List

# Класс для бизнес-логики workspace
class WorkspaceService:

    def __init__(self, session: AsyncSession):
        self.repository = WorkspaceRepository(session)

    # добавление workspace
    async def create(self,
                     workspace: WorkspaceCreate,
                     owner_id: UUID) -> WorkSpace:
        return await self.repository.create(workspace, owner_id)

    # проверка является ли пользователь членом определенного workspace
    async def get_by_id(self, workspace_id: UUID,
                        user_id: UUID) -> WorkSpace:
        workspace = await self.repository.get_by_id(workspace_id)

        if not workspace:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

        user = await self.repository.get_member(user_id, workspace_id)
        if not user:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)

        return workspace

    # получение всех workspaces пользователя
    async def get_user_workspaces(self, user_id: UUID) -> List[WorkSpace]:
        workspaces = await self.repository.get_user_workspaces(user_id)
        return workspaces
