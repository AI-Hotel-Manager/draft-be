from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.exc import NoResultFound

from models.room_model import RoomModel
from schemas.room_schemas import Room, RoomCreate


class RoomManager:
    @staticmethod
    async def insert_room(room_data: RoomCreate, db: AsyncSession) -> Room:
        new_room = RoomModel(**room_data.model_dump())
        db.add(new_room)
        await db.commit()
        return Room.model_validate(new_room)

    @staticmethod
    async def select_by_id(room_id: str, db: AsyncSession) -> Room:
        stmt = select(RoomModel).where(RoomModel.id == UUID(room_id))
        result = await db.execute(stmt)
        room_row = result.scalar()
        if not room_row:
            NoResultFound(f"No room found with id {room_id}!")
        
        return Room.model_validate(room_row)
    
    @staticmethod
    async def select_all(db: AsyncSession) -> list[Room]:
        rooms = (await db.execute(select(RoomModel))).scalars().all()
        return [Room.model_validate(room) for room in rooms]
