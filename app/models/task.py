import uuid

from ..db.base import Base
from sqlalchemy import Column, Integer, String, UUID, ForeignKey, DateTime
from sqlalchemy.sql import func

class Task(Base):
    __tablename__ = "tasks"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    project_id = Column(UUID(as_uuid=True), ForeignKey("projects.id"))
    title = Column(String)
    description = Column(String, nullable=True)
    status = Column(String, server_default='TODO')
    priority = Column(String, server_default='MEDIUM')
    assignee_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=True)
    reporter_id = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    parent_task_id = Column(UUID(as_uuid=True), ForeignKey("tasks.id"), nullable=True)
    due_date = Column(DateTime, nullable=True)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, onupdate=func.now(), server_default=func.now())