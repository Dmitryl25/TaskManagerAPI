import uuid

from ..db.base import Base
from sqlalchemy import Column, Integer, String, UUID, ForeignKey, DateTime
from sqlalchemy.sql import func


class Project(Base):
    __tablename__ = "projects"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    workspace_id = Column(UUID(as_uuid=True), ForeignKey('workspace.id'))
    name = Column(String)
    description = Column(String, nullable=True)
    key = Column(String)
    status = Column(String, server_default="active")
    owner_id = Column(UUID(as_uuid=True), ForeignKey('users.id'))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

