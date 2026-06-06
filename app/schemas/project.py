from pydantic import BaseModel, ConfigDict
from typing import Optional
from uuid import UUID
from datetime import datetime


class ProjectCreate(BaseModel):
    name: str
    description: Optional[str] = None
    key: str

class ProjectUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    status: Optional[str] = None

class ProjectResponse(BaseModel):
    id: UUID
    name: Optional[str] = None
    description: Optional[str] = None
    key: str
    status: str
    owner_id: UUID
    workspace_id: UUID
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)