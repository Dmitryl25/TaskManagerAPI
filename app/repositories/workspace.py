from .base import BaseRepository
from sqlalchemy.ext.asyncio import AsyncSession
from ..models.workspace import WorkSpace, WorkSpaceMember
from ..models.user import User
from ..schemas.workspace import WorkspaceCreate, WorkspaceUpdate
from uuid import UUID
from sqlalchemy.sql import select, update, delete
from typing import Sequence


class WorkspaceRepository(BaseRepository):

    def __init__(self, session: AsyncSession):
        self.session = session

    # Добавление workspace в БД
    async def create(self, workspace: WorkspaceCreate,
                     owner_id: UUID) -> WorkSpace:
        new_workspace = WorkSpace(name=workspace.name,
                                  description=workspace.description,
                                  owner_id=owner_id)
        self.session.add(new_workspace)
        await self.session.flush()

        new_member = WorkSpaceMember(workspace_id=new_workspace.id,
                                     user_id=owner_id,
                                     role="owner")
        self.session.add(new_member)

        await self.session.commit()
        await self.session.refresh(new_workspace)

        return new_workspace


    # получение workspace по id
    async def get_by_id(self, id: UUID) -> WorkSpace:
        workspace = await self.session.execute(select(WorkSpace).where(WorkSpace.id == id))
        return workspace.scalar_one_or_none()

    async def update(self,
                     workspace_id: UUID,
                     data: WorkspaceUpdate) -> WorkSpace:
        await self.session.execute(update(WorkSpace)
                                   .where(WorkSpace.id == workspace_id)
                                   .values(data.model_dump(exclude_none=True)))
        await self.session.commit()
        return await self.get_by_id(workspace_id)


    async def delete(self,
                     workspace_id: UUID):
        await self.session.execute(delete(WorkSpace)
                                   .where(WorkSpace.id == workspace_id))
        await self.session.commit()


    # получение всех workspaces пользователя
    async def get_user_workspaces(self, user_id: UUID) -> Sequence[WorkSpace]:
        workspaces = await self.session.execute(select(WorkSpace)
                                           .join(WorkSpaceMember, WorkSpace.id == WorkSpaceMember.workspace_id)
                                           .where(WorkSpaceMember.user_id == user_id))
        return workspaces.scalars().all()

    # получение пользователя одного workspace
    async def get_member(self, user_id: UUID,
                         workspace_id: UUID) -> WorkSpaceMember | None:
        member = await self.session.execute(select(WorkSpaceMember)
                                            .where(WorkSpaceMember.workspace_id == workspace_id,
                                                   WorkSpaceMember.user_id == user_id))
        return member.scalar_one_or_none()

    async def get_members(self, workspace_id: UUID) -> Sequence[WorkSpaceMember]:
        members = await self.session.execute(select(WorkSpaceMember)
                                             .where(WorkSpaceMember.workspace_id == workspace_id))
        return members.scalars().all()

    async def add_member(self,
                         workspace_id: UUID,
                         user_id: UUID,
                         role: str) -> WorkSpaceMember:
        new_member = WorkSpaceMember(workspace_id=workspace_id,
                                     user_id=user_id,
                                     role=role)
        self.session.add(new_member)
        await self.session.commit()
        await self.session.refresh(new_member)
        return new_member

    async def update_member_role(self,
                                 workspace_id: UUID,
                                 user_id: UUID,
                                 role: str) -> WorkSpaceMember | None:

        await self.session.execute(update(WorkSpaceMember)
                                   .where(WorkSpaceMember.workspace_id == workspace_id,
                                          WorkSpaceMember.user_id == user_id)
                                   .values(role=role))

        await self.session.commit()
        return await self.get_member(user_id, workspace_id)

    async def remove_member(self,
                            workspace_id: UUID,
                            user_id: UUID) -> None:
        await self.session.execute(delete(WorkSpaceMember)
                                   .where(WorkSpaceMember.workspace_id == workspace_id,
                                          WorkSpaceMember.user_id == user_id))
        await self.session.commit()

