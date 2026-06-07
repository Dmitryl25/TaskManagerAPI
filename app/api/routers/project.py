from fastapi import APIRouter, status, HTTPException, Depends
from uuid import UUID
from app.services.project import ProjectService, ProjectUpdate
from sqlalchemy.ext.asyncio import AsyncSession
from ..deps import get_db, get_current_user
from app.models.user import User
from app.schemas.project import ProjectCreate, ProjectResponse

router = APIRouter(tags=['projects'])

@router.post("/workspaces/{workspace_id}/projects")
async def create_project(workspace_id: UUID,
                         project: ProjectCreate,
                         db: AsyncSession = Depends(get_db),
                         user: User = Depends(get_current_user)):
    project = await ProjectService(db).create(project=project,
                                              workspace_id=workspace_id,
                                              owner_id=user.id)
    return ProjectResponse.model_validate(project)

@router.get("/workspaces/{workspace_id}/projects")
async def get_projects(workspace_id: UUID,
                       db: AsyncSession = Depends(get_db),
                       user: User = Depends(get_current_user)):
    projects = await ProjectService(db).get_workspace_projects(workspace_id=workspace_id,
                                                               user_id=user.id)
    return [ProjectResponse.model_validate(project) for project in projects]

@router.get("/projects/{project_id}")
async def get_project_by_id(project_id: UUID,
                            db: AsyncSession = Depends(get_db),
                            user: User = Depends(get_current_user)):
    project = await ProjectService(db).get_by_id(project_id=project_id,
                                                 user_id=user.id)
    return ProjectResponse.model_validate(project)

@router.patch("/projects/{project_id}")
async def update_project(project_id: UUID,
                         data: ProjectUpdate,
                         db: AsyncSession = Depends(get_db),
                         user: User = Depends(get_current_user)):
    project_updated = await ProjectService(db).update_project(project_id=project_id,
                                                              data=data,
                                                              user_id=user.id)
    return ProjectResponse.model_validate(project_updated)

@router.delete("/projects/{project_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_project(project_id: UUID,
                         db: AsyncSession = Depends(get_db),
                         user: User = Depends(get_current_user)):
    await ProjectService(db).delete_project(project_id=project_id,
                                            user_id=user.id)
