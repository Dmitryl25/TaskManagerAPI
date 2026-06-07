from ..repositories.workspace import WorkspaceRepository
from sqlalchemy.ext.asyncio import AsyncSession
from ..schemas.workspace import WorkspaceCreate, WorkspaceUpdate
from uuid import UUID
from ..models.workspace import WorkSpace, WorkSpaceMember
from fastapi import status, HTTPException
from typing import Sequence

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
    async def get_user_workspaces(self, user_id: UUID) -> Sequence[WorkSpace]:
        workspaces = await self.repository.get_user_workspaces(user_id)
        return workspaces

    async def update_workspace(self,
                                workspace_id: UUID,
                                data: WorkspaceUpdate,
                                user_id: UUID):
        await self.get_by_id(workspace_id=workspace_id,
                             user_id=user_id)
        return await self.repository.update(workspace_id=workspace_id,
                                            data=data)

    async def delete_workspace(self,
                               workspace_id: UUID,
                               user_id: UUID):
        workspace = await self.repository.get_by_id(workspace_id)

        if not workspace:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

        user: WorkSpaceMember = await self.repository.get_member(workspace_id=workspace_id,
                                                                 user_id=user_id)
        if not user or user.role != "owner":
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)

        await self.repository.delete(workspace_id)
