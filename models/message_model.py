from uuid import uuid4

from sqlalchemy import Column, UUID, String, TIMESTAMP, func

from db import Base


class MessageModel(Base):
    __tablename__ = "messages"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    user_id = Column(UUID(as_uuid=True), nullable=True)
    role = Column(String, nullable=False)
    content = Column(String, nullable=False)
    created_at = Column(TIMESTAMP, server_default=func.now())
