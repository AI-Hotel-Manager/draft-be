from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete, or_
from sqlalchemy.orm import selectinload
from sqlalchemy.exc import NoResultFound

from models.reservation_model import ReservationModel
from models.room_model import RoomModel
from schemas.reservation_schemas import Reservation, ReservationCreate


class ReservationManager:
    @staticmethod
    async def insert_reservation(reservation_data: ReservationCreate, db: AsyncSession) -> Reservation:
        new_reservation = ReservationModel(**reservation_data.model_dump())
        db.add(new_reservation)
        await db.commit()
        await db.refresh(new_reservation)

        # Load reservation with related room (eager loading)
        stmt = (
            select(ReservationModel)
            .options(selectinload(ReservationModel.room).selectinload(RoomModel.room_type))
            .where(ReservationModel.id == new_reservation.id)
        )
        result = await db.execute(stmt)
        full_reservation = result.scalar_one()

        return Reservation.model_validate(full_reservation)

    @staticmethod
    async def delete_reservation(reservation_id: str, db: AsyncSession) -> None:
        stmt = delete(ReservationModel).where(ReservationModel.id == reservation_id)
        await db.execute(stmt)
        await db.commit()

    @staticmethod
    async def select_reservations_by_room_id(room_id: UUID, db: AsyncSession) -> list[Reservation]:
        stmt = select(ReservationModel).where(ReservationModel.room_id == room_id)
        result = await db.execute(stmt)
        reservations = result.scalars().all()
        return [Reservation.model_validate(r) for r in reservations]

    @staticmethod
    async def select_reservations_by_user_id(user_id: UUID, db: AsyncSession) -> list[Reservation]:
        stmt = select(ReservationModel).where(ReservationModel.user_id == user_id)
        result = await db.execute(stmt)
        reservations = result.scalars().all()
        return [Reservation.model_validate(r) for r in reservations]

    @staticmethod
    async def select_reservations_by_guest_info(
        guest_name: str | None,
        guest_email: str | None,
        guest_phone: str | None,
        db: AsyncSession
    ) -> list[Reservation]:
        filters = []
        if guest_name:
            filters.append(ReservationModel.guest_name.ilike(f"%{guest_name}%"))
        if guest_email:
            filters.append(ReservationModel.guest_email.ilike(f"%{guest_email}%"))
        if guest_phone:
            filters.append(ReservationModel.guest_phone.ilike(f"%{guest_phone}%"))

        if not filters:
            raise ValueError("At least one of guest_name, guest_email, or guest_phone must be provided.")

        stmt = select(ReservationModel).options(selectinload(ReservationModel.room).selectinload(RoomModel.room_type)).where(or_(*filters))
        result = await db.execute(stmt)
        reservations = result.scalars().all()
        return [Reservation.model_validate(r) for r in reservations]
