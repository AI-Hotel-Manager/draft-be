from datetime import date
from uuid import UUID
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from models.room_model import RoomModel
from models.reservation_model import ReservationModel
from schemas.room_schemas import Room


class AvailabilityManager:
    @staticmethod
    async def get_available_rooms(
        desired_check_in: date,
        desired_check_out: date,
        db: AsyncSession
    ) -> List[Room]:
        # Subquery for rooms that are already reserved during the period
        subquery = (
            select(ReservationModel.room_id)
            .where(
                ReservationModel.check_in < desired_check_out,
                ReservationModel.check_out > desired_check_in,
            )
            .subquery()
        )

        # Main query: rooms not in reserved list
        stmt = (
            select(RoomModel)
            .options(selectinload(RoomModel.room_type))
            .where(RoomModel.id.not_in(select(subquery)))
        )

        result = await db.execute(stmt)
        available_rooms = result.scalars().all()
        return [Room.model_validate(room) for room in available_rooms]
