from uuid import UUID
from typing import Optional, List

from pydantic import BaseModel, ConfigDict, field_serializer

from schemas.room_type_schemas import RoomType


class RoomBase(BaseModel):
    room_number: str
    name: Optional[str] = None
    capacity: int
    bed_type: Optional[str] = None
    amenities: List[str] = []
    price_per_night: float
    image_name: Optional[str] = None
    description: Optional[str] = None


class RoomCreate(RoomBase):
    room_type_id: str


class Room(RoomBase):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    room_type: RoomType

    @field_serializer("id")
    def serialize_id(self, id: UUID, _info):
        return str(id)
