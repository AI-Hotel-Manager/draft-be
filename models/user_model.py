from uuid import uuid4

from sqlalchemy import Column, UUID, String, TIMESTAMP, func

from db import Base

class UserModel(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    full_name = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)
    phone = Column(String, nullable=True)
    created_at = Column(TIMESTAMP, server_default=func.now())
