from fastapi import APIRouter

from routers import room_router, room_type_router, chat_router, reservation_router


main_router = APIRouter()
main_router.include_router(room_router.router)
main_router.include_router(room_type_router.router)
main_router.include_router(chat_router.router)
main_router.include_router(reservation_router.router)
