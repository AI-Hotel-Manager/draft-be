from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from models.room_type_model import RoomTypeModel
from schemas.room_type_schemas import RoomType, RoomTypeCreate


class RoomTypeManager:
    @staticmethod
    async def insert_room_type(room_type_data: RoomTypeCreate, db: AsyncSession) -> RoomType:
        new_room_type = RoomTypeModel(**room_type_data.model_dump())
        db.add(new_room_type)
        await db.commit()
        return RoomType.model_validate(new_room_type)

    @staticmethod
    async def select_all_types(db: AsyncSession) -> list[RoomType]:
        room_types = (await db.execute(select(RoomTypeModel))).scalars().all()
        return [RoomType.model_validate(room_type) for room_type in room_types]
