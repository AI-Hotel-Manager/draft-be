from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from db import get_db
from schemas.room_schemas import RoomCreate, Room
from managers.room_manager import RoomManager


router = APIRouter(prefix="/rooms", tags=["Rooms"])


@router.post("/", response_model=Room, status_code=status.HTTP_201_CREATED)
async def post_room(data: RoomCreate, db: AsyncSession = Depends(get_db)):
    room = await RoomManager.insert_room(data, db)
    return room
    

@router.get("/by-id/{room_id}", response_model=Room)
async def get_by_id(room_id: str, db = Depends(get_db)):
    print("adi be")
    room = await RoomManager.select_by_id(room_id, db)
    return room


@router.get("/all", response_model=list[Room])
async def get_all(db: AsyncSession = Depends(get_db)):
    rooms = await RoomManager.select_all(db)
    return rooms
