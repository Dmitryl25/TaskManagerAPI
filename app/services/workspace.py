from ..repositories.workspace import WorkspaceRepository
from ..repositories.user import UserRepository
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
        self.user_rep = UserRepository(session)


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


    async def get_members(self,
                          workspace_id: UUID,
                          user_id: UUID) -> Sequence[WorkSpaceMember]:
        await self.get_by_id(workspace_id=workspace_id,
                             user_id=user_id)
        return await self.repository.get_members(workspace_id=workspace_id)

    async def add_member(self,
                         workspace_id: UUID,
                         current_user_id: UUID,
                         new_user_id: UUID,
                         role: str) -> WorkSpaceMember:
        workspace = await self.repository.get_by_id(workspace_id)

        if not workspace:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

        user = await self.repository.get_member(current_user_id, workspace_id)
        if not user or user.role not in ['admin', 'owner']:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)

        new_user = await self.user_rep.get_by_id(new_user_id)
        if not new_user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

        new_member = await self.repository.add_member(workspace_id=workspace_id,
                                                      user_id=new_user_id,
                                                      role=role)
        return new_member

    async def update_member_role(self,
                                 workspace_id: UUID,
                                 current_user_id: UUID,
                                 target_user_id: UUID,
                                 role: str):
        workspace = await self.repository.get_by_id(workspace_id)

        if not workspace:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

        user = await self.repository.get_member(current_user_id, workspace_id)
        if not user or user.role not in ['admin', 'owner']:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)

        target_user = await self.repository.get_member(target_user_id, workspace_id)
        if not target_user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

        member_updated = await self.repository.update_member_role(workspace_id=workspace_id,
                                                                  user_id=target_user_id,
                                                                  role=role)
        return member_updated

    async def remove_member(self,
                            workspace_id: UUID,
                            current_user_id: UUID,
                            target_user_id: UUID):
        workspace = await self.repository.get_by_id(workspace_id)

        if not workspace:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

        user = await self.repository.get_member(current_user_id, workspace_id)
        if not user or user.role not in ['admin', 'owner']:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)

        target_user = await self.repository.get_member(target_user_id, workspace_id)
        if not target_user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

        if target_user.role == "owner":
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)

        await self.repository.remove_member(workspace_id=workspace_id,
                                            user_id=target_user_id)


