import uuid

from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, DateTime
from sqlalchemy.sql import func
from ..db.base import Base
from uuid import UUID
from sqlalchemy.dialects.postgresql import UUID


class WorkSpace(Base):
    __tablename__ = "workspace"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String)
    description = Column(String, nullable=True)
    owner_id = Column(UUID(as_uuid=True), ForeignKey('users.id'))
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), server_onupdate=func.now())


class WorkSpaceMember(Base):
    __tablename__ = 'workspacemember'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    workspace_id = Column(UUID(as_uuid=True), ForeignKey('workspace.id', ondelete='CASCADE'))
    user_id = Column(UUID(as_uuid=True), ForeignKey('users.id'))
    role = Column(String)
    created_at = Column(DateTime, server_default=func.now())

