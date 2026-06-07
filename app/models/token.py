import uuid

from ..db.base import Base
from sqlalchemy import Column, Integer, String, UUID, ForeignKey, DateTime
from sqlalchemy.sql import func


class Token(Base):
    __tablename__ = "tokens"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    token_hash = Column(String)
    expires_at = Column(DateTime)
    revoked_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, server_default=func.now())