from pydantic import BaseModel, ConfigDict
from typing import Optional
from uuid import UUID
from datetime import datetime


class TaskCreate(BaseModel):
    title: str
    description: Optional[str] = None
    priority: Optional[str] = 'MEDIUM'
    assignee_id: Optional[UUID] = None
    parent_task_id: Optional[UUID] = None
    due_date: Optional[datetime] = None

class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    assignee_id: Optional[UUID] = None
    parent_task_id: Optional[UUID] = None
    due_date: Optional[datetime] = None
    status: Optional[str] = None

class TaskResponse(BaseModel):
    id: UUID
    project_id: UUID
    title: str
    description: Optional[str] = None
    status: str
    priority: str
    assignee_id: Optional[UUID] = None
    reporter_id: UUID
    parent_task_id: Optional[UUID] = None
    due_date: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)