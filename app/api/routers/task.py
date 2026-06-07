from fastapi import APIRouter, Depends, status
from app.services.task import TaskService
from app.schemas.task import TaskCreate, TaskResponse, TaskUpdate, TaskFilter
from uuid import UUID
from ..deps import get_db, get_current_user
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.user import User


router = APIRouter(tags=['tasks'])

@router.post("/projects/{project_id}/tasks")
async def create_tasks(project_id: UUID,
                       task: TaskCreate,
                       db: AsyncSession = Depends(get_db),
                       user: User = Depends(get_current_user)):
    new_task = await TaskService(db).create(task=task,
                                            project_id=project_id,
                                            reporter_id=user.id)
    return TaskResponse.model_validate(new_task)


@router.get("/projects/{project_id}/tasks")
async def get_project_tasks(project_id: UUID,
                            filters: TaskFilter = Depends(),
                            db: AsyncSession = Depends(get_db),
                            user: User = Depends(get_current_user)):
    tasks = await TaskService(db).get_project_tasks(project_id=project_id,
                                                    user_id=user.id,
                                                    filters=filters)
    return [TaskResponse.model_validate(task) for task in tasks]

@router.get("/tasks/{task_id}")
async def get_task(task_id: UUID,
                   db: AsyncSession = Depends(get_db),
                   user: User = Depends(get_current_user)):
    task = await TaskService(db).get_by_id(task_id=task_id,
                                           user_id=user.id)
    return TaskResponse.model_validate(task)

@router.patch("/tasks/{task_id}")
async def update_task(task_id: UUID,
                      data: TaskUpdate,
                      db: AsyncSession = Depends(get_db),
                      user: User = Depends(get_current_user)):
    updated_task = await TaskService(db).update_task(task_id=task_id,
                                                     user_id=user.id,
                                                     data=data)
    return TaskResponse.model_validate(updated_task)

@router.delete("/tasks/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_task(task_id: UUID,
                      db: AsyncSession = Depends(get_db),
                      user: User = Depends(get_current_user)):
    await TaskService(db).delete_task(task_id=task_id,
                                      user_id=user.id)
