from uuid import uuid4

from sqlalchemy import Numeric, Integer, ARRAY, Column, String, UUID, TIMESTAMP, func, ForeignKey
from sqlalchemy.orm import relationship

from db import Base


class RoomModel(Base):
    __tablename__ = "rooms"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    room_number = Column(String, nullable=False)
    name = Column(String)
    room_type_id = Column(UUID(as_uuid=True), ForeignKey("room_types.id"))
    capacity = Column(Integer, nullable=False)
    bed_type = Column(String)
    amenities = Column(ARRAY(String))
    rating = Column(Numeric(2, 1))
    price_per_night = Column(Numeric(10, 2), nullable=False)
    image_name = Column(String)
    description = Column(String)
    created_at = Column(TIMESTAMP, server_default=func.now())

    room_type = relationship("RoomTypeModel")