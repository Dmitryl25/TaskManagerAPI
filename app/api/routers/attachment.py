from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID

from app.services.attachment import AttachmentService
from app.schemas.attachment import PresignedUrlRequest, PresignedUrlResponse, AttachmentCreate, AttachmentResponse
from app.api.deps import get_db, get_current_user
from app.models.user import User

router = APIRouter(tags=["attachments"])


@router.post("/tasks/{task_id}/attachments/upload-url", response_model=PresignedUrlResponse)
async def get_upload_url(task_id: UUID,
                         data: PresignedUrlRequest,
                         db: AsyncSession = Depends(get_db),
                         user: User = Depends(get_current_user)):
    return await AttachmentService(db).get_upload_url(task_id=task_id,
                                                      user_id=user.id,
                                                      data=data)


@router.post("/tasks/{task_id}/attachments", response_model=AttachmentResponse)
async def confirm_upload(task_id: UUID,
                         data: AttachmentCreate,
                         db: AsyncSession = Depends(get_db),
                         user: User = Depends(get_current_user)):
    return await AttachmentService(db).confirm_upload(task_id=task_id,
                                                      user_id=user.id,
                                                      data=data)


@router.get("/tasks/{task_id}/attachments")
async def get_task_attachments(task_id: UUID,
                               db: AsyncSession = Depends(get_db),
                               user: User = Depends(get_current_user)):
    return await AttachmentService(db).get_task_attachments(task_id=task_id,
                                                            user_id=user.id)


@router.delete("/attachments/{attachment_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_attachment(attachment_id: UUID,
                            db: AsyncSession = Depends(get_db),
                            user: User = Depends(get_current_user)):
    await AttachmentService(db).delete(attachment_id=attachment_id,
                                       user_id=user.id)
