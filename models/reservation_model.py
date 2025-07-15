from uuid import uuid4

from sqlalchemy import Column, UUID, String, Date, Numeric, TIMESTAMP, func, ForeignKey
from sqlalchemy.orm import relationship

from db import Base


class ReservationModel(Base):
    __tablename__ = "reservations"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    room_id = Column(UUID(as_uuid=True), ForeignKey("rooms.id"), nullable=False)
    check_in = Column(Date, nullable=False)
    check_out = Column(Date, nullable=False)
    total_price = Column(Numeric(10, 2))
    status = Column(String, default='confirmed')
    created_at = Column(TIMESTAMP, server_default=func.now())

    user = relationship("UserModel")
    room = relationship("RoomModel")
