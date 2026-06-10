from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import Optional
from uuid import UUID

class PresignedUrlRequest(BaseModel):
    filename: str
    content_type: str
    size: int

class PresignedUrlResponse(BaseModel):
    upload_url: str
    s3_key: str

class AttachmentCreate(BaseModel):
    filename: str
    s3_key: str
    size: int
    content_type: str

class AttachmentResponse(BaseModel):
    id: UUID
    task_id: UUID
    uploaded_by: UUID
    filename: str
    s3_key: str
    size: int
    content_type: str
    created_at: datetime
    download_url: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)