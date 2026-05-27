from fastapi import APIRouter, HTTPException, status, Depends
from app.services.workspace import WorkspaceService
from ..deps import get_current_user, get_db
from app.models.user import User
from app.schemas.workspace import WorkspaceCreate, WorkspaceResponse
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
