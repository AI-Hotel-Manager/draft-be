from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm import selectinload

from models.room_model import RoomModel
from schemas.room_schemas import Room, RoomCreate


class RoomManager:
    @staticmethod
    async def insert_room(room_data: RoomCreate, db: AsyncSession) -> Room:
        new_room = RoomModel(**room_data.model_dump())
        db.add(new_room)
        await db.commit()
        await db.refresh(new_room)  

        stmt = select(RoomModel).options(selectinload(RoomModel.room_type)).where(RoomModel.id == new_room.id)
        result = await db.execute(stmt)
        refreshed_room = result.scalar_one()
        return Room.model_validate(refreshed_room)

    @staticmethod
    async def select_by_id(room_id: str, db: AsyncSession) -> Room:
        print('NOOOOOOOOOOOOOOOO')
        stmt = (
            select(RoomModel)
            .options(selectinload(RoomModel.room_type))
            .where(RoomModel.id == UUID(room_id))
        )
        result = await db.execute(stmt)
        room_row = result.scalar_one_or_none()
        if not room_row:
            raise NoResultFound(f"No room found with id {room_id}!")
        return Room.model_validate(room_row)

    @staticmethod
    async def select_all(db: AsyncSession) -> list[Room]:
        print('HEREEEEEEEEEEE')
        stmt = select(RoomModel).options(selectinload(RoomModel.room_type))
        result = await db.execute(stmt)
        rooms = result.scalars().all()
        return [Room.model_validate(room) for room in rooms]
