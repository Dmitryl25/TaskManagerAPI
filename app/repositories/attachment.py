from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete
from uuid import UUID
from typing import Sequence

from ..models.attachment import Attachment
from ..schemas.attachment import AttachmentCreate


class AttachmentRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self,
                     data: AttachmentCreate,
                     task_id: UUID,
                     uploaded_by: UUID) -> Attachment:
        attachment = Attachment(task_id=task_id,
                                uploaded_by=uploaded_by,
                                filename=data.filename,
                                s3_key=data.s3_key,
                                size=data.size,
                                content_type=data.content_type)
        self.session.add(attachment)
        await self.session.commit()
        await self.session.refresh(attachment)
        return attachment

    async def get_by_id(self, attachment_id: UUID) -> Attachment | None:
        result = await self.session.execute(select(Attachment)
                                            .where(Attachment.id == attachment_id))
        return result.scalar_one_or_none()

    async def get_by_task_id(self, task_id: UUID) -> Sequence[Attachment]:
        result = await self.session.execute(select(Attachment)
                                            .where(Attachment.task_id == task_id))
        return result.scalars().all()

    async def delete(self, attachment_id: UUID) -> None:
        await self.session.execute(delete(Attachment)
                                   .where(Attachment.id == attachment_id))
        await self.session.commit()
