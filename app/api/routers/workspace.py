from fastapi import APIRouter, HTTPException, status, Depends
from app.services.workspace import WorkspaceService
from ..deps import get_current_user, get_db
from app.models.user import User
from app.schemas.workspace import WorkspaceCreate, WorkspaceResponse, WorkspaceUpdate
from app.schemas.workspace import MemberResponse, MemberRoleUpdate, AddMemberRequest
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID
from typing import List


router = APIRouter(prefix="/workspace",
                   tags=["workspace"])

# создание workspace
@router.post(path="", status_code=status.HTTP_201_CREATED)
async def create_workspace(workspace: WorkspaceCreate,
                           user: User = Depends(get_current_user),
                           db: AsyncSession = Depends(get_db)):
    workspace_created = await WorkspaceService(db).create(workspace, user.id)
    return WorkspaceResponse.model_validate(workspace_created)


# получение всех workspaces для пользователя
@router.get(path="", status_code=status.HTTP_200_OK)
async def get_user_workspaces(user: User = Depends(get_current_user),
                              db: AsyncSession = Depends(get_db)) -> List[WorkspaceResponse]:
    user_workspaces = await WorkspaceService(db).get_user_workspaces(user.id)
    return [WorkspaceResponse.model_validate(workspace) for workspace in user_workspaces]


# получение workspace по id (только для пользователя, который в нем состоит)
@router.get(path="/{workspace_id}", status_code=status.HTTP_200_OK)
async def get_workspace(workspace_id: UUID,
                        user: User = Depends(get_current_user),
                        db: AsyncSession = Depends(get_db)):
    workspace = await WorkspaceService(db).get_by_id(workspace_id=workspace_id,
                                                     user_id=user.id)
    return WorkspaceResponse.model_validate(workspace)


@router.patch("/workspace/{workspace_id}")
async def update_workspace(workspace_id: UUID,
                           data: WorkspaceUpdate,
                           db: AsyncSession = Depends(get_db),
                           user: User = Depends(get_current_user)):
    workspace_updated = await WorkspaceService(db).update_workspace(workspace_id=workspace_id,
                                                                    data=data,
                                                                    user_id=user.id)
    return WorkspaceResponse.model_validate(workspace_updated)


@router.delete("/workspace/{workspace_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_workspace(workspace_id: UUID,
                           db: AsyncSession = Depends(get_db),
                           user: User = Depends(get_current_user)):
    await WorkspaceService(db).delete_workspace(workspace_id=workspace_id,
                                                user_id=user.id)


@router.get("/workspace/{workspace_id}/members")
async def get_workspace_members(workspace_id: UUID,
                                db: AsyncSession = Depends(get_db),
                                user: User = Depends(get_current_user)):
    members = await WorkspaceService(db).get_members(workspace_id=workspace_id,
                                                     user_id=user.id)
    return [MemberResponse.model_validate(member) for member in members]

@router.post("/workspace/{workspace_id}/members")
async def add_member(workspace_id: UUID,
                     data: AddMemberRequest,
                     db: AsyncSession = Depends(get_db),
                     user: User = Depends(get_current_user)):
    new_member = await WorkspaceService(db).add_member(workspace_id=workspace_id,
                                                       current_user_id=user.id,
                                                       new_user_id=data.user_id,
                                                       role=data.role)
    return MemberResponse.model_validate(new_member)

@router.patch("/workspace/{workspace_id}/members/{user_id}")
async def update_member_role(workspace_id: UUID,
                             user_id: UUID,
                             data: MemberRoleUpdate,
                             db: AsyncSession = Depends(get_db),
                             user: User = Depends(get_current_user)):
    member_updated = await WorkspaceService(db).update_member_role(workspace_id=workspace_id,
                                                                   current_user_id=user.id,
                                                                   target_user_id=user_id,
                                                                   role=data.role)
    return MemberResponse.model_validate(member_updated)

@router.delete("/workspace/{workspace_id}/members/{user_id}",
               status_code=status.HTTP_204_NO_CONTENT)
async def remove_member(workspace_id: UUID,
                        user_id: UUID,
                        db: AsyncSession = Depends(get_db),
                        user: User = Depends(get_current_user)):
    await WorkspaceService(db).remove_member(workspace_id=workspace_id,
                                             current_user_id=user.id,
                                             target_user_id=user_id)
