from uuid import uuid4

from sqlalchemy import Numeric, Integer, ARRAY, Column, String, UUID, TIMESTAMP, func

from db import Base


class RoomModel(Base):
    __tablename__ = "rooms"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    room_number = Column(String, nullable=False)
    name = Column(String, nullable=True)
    type_id = Column(UUID(as_uuid=True), nullable=True)  # FK later if needed
    capacity = Column(Integer, nullable=False)
    bed_type = Column(String, nullable=True)
    amenities = Column(ARRAY(String), nullable=True)
    rating = Column(Numeric(2, 1), nullable=True)
    price_per_night = Column(Numeric(10, 2), nullable=False)
    image_name = Column(String, nullable=True)
    description = Column(String, nullable=True)
    created_at = Column(TIMESTAMP, server_default=func.now())
