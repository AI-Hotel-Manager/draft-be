from fastapi import APIRouter, status, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from db import get_db
from schemas.message_schemas import ChatRequest, ChatResponse
from agent.reservation_agent import process_reservation_message


router = APIRouter(prefix="/chat", tags=["Chat"])


@router.post("/", response_model=ChatResponse, status_code=status.HTTP_201_CREATED)
async def post_chat_message(chat_req: ChatRequest, db: AsyncSession = Depends(get_db)):
    resp = await process_reservation_message(chat_req, db)
    return resp
