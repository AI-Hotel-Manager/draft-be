from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from db import get_db
from schemas.room_type_schemas import RoomType, RoomTypeCreate
from managers.room_type_manager import RoomTypeManager


router = APIRouter(prefix="/room-types", tags=["Room types"])


@router.post("/", response_model=RoomType, status_code=status.HTTP_201_CREATED)
async def post_room_type(data: RoomTypeCreate, db: AsyncSession = Depends(get_db)):
    room_type = await RoomTypeManager.insert_room_type(data, db)
    return room_type


@router.get("/all", response_model=list[RoomType])
async def get_all(db: AsyncSession = Depends(get_db)):
    room_types = await RoomTypeManager.select_all_types(db)
    return room_types
