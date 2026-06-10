import uuid

from sqlalchemy import Column, Integer, String, UUID, DateTime, ForeignKey
from ..db.base import Base
from sqlalchemy.sql import func

class Comment(Base):
    __tablename__ = "comments"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    task_id = Column(UUID(as_uuid=True), ForeignKey("tasks.id", ondelete='CASCADE'))
    author_id = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    content = Column(String)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, onupdate=func.now(), server_default=func.now())