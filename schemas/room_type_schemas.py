from uuid import UUID

from pydantic import BaseModel, ConfigDict, field_serializer


class RoomTypeBase(BaseModel):
    name: str
    description: str


class RoomTypeCreate(RoomTypeBase):
    pass 


class RoomType(RoomTypeBase):
    model_config = ConfigDict(from_attributes=True)

    id: UUID

    @field_serializer("id")
    def serialize_id(self, id: UUID, _info):
        return str(id)
