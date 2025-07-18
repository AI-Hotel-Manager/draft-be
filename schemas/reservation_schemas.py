from uuid import UUID
from typing import Optional
from datetime import date, datetime
from pydantic import BaseModel, ConfigDict, field_serializer

from schemas.room_schemas import Room


class ReservationBase(BaseModel):
    check_in: date
    check_out: date
    total_price: Optional[float] = None
    status: Optional[str] = "confirmed"

    # Guest fields for voice/anonymous reservations
    guest_name: Optional[str] = None
    guest_email: Optional[str] = None
    guest_phone: Optional[str] = None


class ReservationCreate(ReservationBase):
    room_id: str
    user_id: Optional[str] = None  # Nullable for guest/voice reservations


class Reservation(ReservationBase):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    room: Room
    user_id: Optional[UUID] = None
    created_at: Optional[datetime]

    @field_serializer("id", "user_id")
    def serialize_uuids(self, value: UUID, _info):
        return str(value)
