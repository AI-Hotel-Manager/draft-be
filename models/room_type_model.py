from uuid import uuid4

from sqlalchemy import Column, UUID, String

from db import Base


class RoomTypeModel(Base):
    __tablename__ = "room_types"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    name = Column(String, nullable=False)
    description = Column(String)
