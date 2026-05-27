from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime
from uuid import UUID

# схема для создания workspace
class WorkspaceCreate(BaseModel):
    name: str
    description: Optional[str]

# схема для обновления workspace
class WorkspaceUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None

# схема для ответа
class WorkspaceResponse(BaseModel):
    id: UUID
    name: str
    description: Optional[str] = None
    owner_id: UUID
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


