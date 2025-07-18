from uuid import uuid4

from sqlalchemy import Column, UUID, String, Date, Numeric, TIMESTAMP, func, ForeignKey
from sqlalchemy.orm import relationship

from db import Base


class ReservationModel(Base):
    __tablename__ = "reservations"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)

    # User can be null for guest reservations
    user_id = Column(UUID(as_uuid=True), nullable=True)

    room_id = Column(UUID(as_uuid=True), ForeignKey("rooms.id"), nullable=False)

    # Guest info for voice/anonymous reservations
    guest_name = Column(String, nullable=True)
    guest_email = Column(String, nullable=True)
    guest_phone = Column(String, nullable=True)

    check_in = Column(Date, nullable=False)
    check_out = Column(Date, nullable=False)

    total_price = Column(Numeric(10, 2))
    status = Column(String, default="confirmed")

    created_at = Column(TIMESTAMP, server_default=func.now())

    room = relationship("RoomModel")
