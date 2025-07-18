from uuid import uuid4
from dataclasses import dataclass
from datetime import date
from typing import Optional

from agents import Agent, Runner, function_tool, RunContextWrapper, SQLiteSession
from sqlalchemy.ext.asyncio import AsyncSession

from schemas.message_schemas import ChatResponse, ChatRequest, MessageResponse
from schemas.room_schemas import Room
from schemas.reservation_schemas import ReservationCreate, Reservation
from managers.room_manager import RoomManager
from managers.reservation_manager import ReservationManager
from managers.availability_manager import AvailabilityManager


@dataclass
class AgentContext:
    db: AsyncSession


@function_tool
async def list_hotel_rooms(wrapper: RunContextWrapper[AgentContext]) -> list[Room]:
    return await RoomManager.select_all(wrapper.context.db)


@function_tool
async def make_reservation(wrapper: RunContextWrapper[AgentContext], reservation_data: ReservationCreate) -> Reservation:
    return await ReservationManager.insert_reservation(reservation_data, wrapper.context.db)


@function_tool
async def check_availability(wrapper: RunContextWrapper[AgentContext], desired_check_in: date, desired_check_out: date) -> list[Room]:
    return await AvailabilityManager.get_available_rooms(desired_check_in, desired_check_out, wrapper.context.db)


@function_tool
async def get_reservations_by_guest_info(wrapper: RunContextWrapper[AgentContext], guest_name: Optional[str], guest_email: Optional[str], guest_phone: Optional[str]) -> list[Reservation]:
    return await ReservationManager.select_reservations_by_guest_info(guest_name, guest_email, guest_phone, wrapper.context.db)


@function_tool
async def cancel_reservation(wrapper: RunContextWrapper[AgentContext], reservation_id: str) -> None:
    return await ReservationManager.delete_reservation(reservation_id, wrapper.context.db)


async def process_reservation_message(
    chat_req: ChatRequest, db: AsyncSession
) -> ChatResponse:
    agent = Agent(
        name="Hotel room reservation assistant",
        instructions="""
            You are a helpful and professional hotel room reservation assistant. Your role is to assist customers in finding and reserving hotel rooms based on their preferences and requirements.

            When assisting a customer, always ask for and confirm the following details:
            - Check-in and check-out dates
            - Number of guests
            - Room type preferences (e.g., single, double, suite)
            - Any special requirements (e.g., pet-friendly, wheelchair access, sea view)
            - Budget or price range (if relevant)
            - Contact information (e.g., name, phone number, email)

            Once you have all the required information:
            - Check room availability using the tools or functions available to you.
            - Suggest available rooms that match their preferences.
            - Confirm the reservation with the user before finalizing it.

            Be friendly, polite, and concise. If the customer asks a question outside of your responsibilities (e.g., tourist recommendations), politely redirect them back to the reservation process.

            Always confirm with the customer before making a booking, and summarize the reservation details clearly before completion.
        """,
        tools=[list_hotel_rooms, make_reservation, check_availability, get_reservations_by_guest_info, cancel_reservation]
    )

    conversation_id = chat_req.conversation_id if chat_req.conversation_id else str(uuid4())

    session = SQLiteSession(conversation_id, "conversation_history.db")

    agent_context = AgentContext(
        db=db,
    )

    result = await Runner.run(
        starting_agent=agent, input=chat_req.message, context=agent_context, session=session
    )
    output = result.final_output

    return ChatResponse(
        messages=[MessageResponse(content=output)], conversation_id=conversation_id
    )
