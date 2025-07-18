from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from db import get_db
from schemas.reservation_schemas import ReservationCreate, Reservation
from managers.reservation_manager import ReservationManager


router = APIRouter(prefix="/reservations", tags=["reservations"])


@router.post("/", response_model=Reservation, status_code=status.HTTP_201_CREATED)
async def post_reservation(data: ReservationCreate, db: AsyncSession = Depends(get_db)):
    reservation = await ReservationManager.insert_reservation(data, db)
    return reservation
