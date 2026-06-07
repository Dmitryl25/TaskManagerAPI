from pydantic import BaseModel, EmailStr, ConfigDict, Field
from typing import Optional
from datetime import datetime
from uuid import UUID

# схема для создания пользователя
class UserCreated(BaseModel):
    email: EmailStr
    password: str


# схема для обновления пользователя
class UserUpdate(BaseModel):
    email: Optional[EmailStr] = Field(default=None)


# схема для ответа
class UserResponse(BaseModel):
    id: UUID
    email: EmailStr
    is_active: bool
    is_verified: bool
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

class Tokens(BaseModel):
    token_type: str = "bearer"
    access_token: str
    refresh_token: str

class RefreshTokenRequest(BaseModel):
    refresh_token: str