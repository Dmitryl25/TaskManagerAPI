from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID
from fastapi import HTTPException, status

from ..repositories.attachment import AttachmentRepository
from ..repositories.task import TaskRepository
from ..repositories.workspace import WorkspaceRepository
from ..repositories.project import ProjectRepository
from ..schemas.attachment import AttachmentCreate, PresignedUrlRequest
from ..core.s3 import generate_presigned_upload_url, generate_presigned_download_url, delete_object


class AttachmentService:
    def __init__(self, db: AsyncSession):
        self.attachment_rep = AttachmentRepository(db)
        self.task_rep = TaskRepository(db)
        self.workspace_rep = WorkspaceRepository(db)
        self.project_rep = ProjectRepository(db)

    async def check_task_member(self, task_id: UUID, user_id: UUID):
        task = await self.task_rep.get_by_id(task_id)
        if not task:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

        project = await self.project_rep.get_by_id(task.project_id)
        member = await self.workspace_rep.get_member(user_id=user_id,
                                                     workspace_id=project.workspace_id)
        if not member:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)

        return task

    async def get_upload_url(self, task_id: UUID, user_id: UUID, data: PresignedUrlRequest):
        await self.check_task_member(task_id=task_id,
                                     user_id=user_id)

        upload_url, s3_key = await generate_presigned_upload_url(filename=data.filename,
                                                                 content_type=data.content_type)

        return {"upload_url": upload_url,
                "s3_key": s3_key}

    async def confirm_upload(self,
                             task_id: UUID,
                             user_id: UUID,
                             data: AttachmentCreate):
        await self.check_task_member(task_id=task_id,
                                     user_id=user_id)

        attachment = await self.attachment_rep.create(data=data,
                                                      task_id=task_id,
                                                      uploaded_by=user_id)
        download_url = await generate_presigned_download_url(attachment.s3_key)
        return {**attachment.__dict__, "download_url": download_url}


    async def get_task_attachments(self, task_id: UUID, user_id: UUID):
        await self.check_task_member(task_id=task_id,
                                     user_id=user_id)
        attachments = await self.attachment_rep.get_by_task_id(task_id)

        result = []
        for attachment in attachments:
            download_url = await generate_presigned_download_url(attachment.s3_key)
            result.append({**attachment.__dict__, "download_url": download_url})

        return result

    async def delete(self,
                     attachment_id: UUID,
                     user_id: UUID):
        attachment = await self.attachment_rep.get_by_id(attachment_id=attachment_id)
        if not attachment:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

        if attachment.uploaded_by != user_id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)

        await delete_object(attachment.s3_key)
        await self.attachment_rep.delete(attachment_id)
