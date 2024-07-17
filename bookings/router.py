from fastapi import APIRouter, Depends
from bookings.dao import BookingDAO
from users.model import User
from users.dependencies import get_current_user
from datetime import date
from exceptions import RoomCannotBeBooked
from fastapi import BackgroundTasks
from tasks.tasks import send_booking_message
from pydantic import BaseModel
from bookings.scheme import SchemeBooking

router = APIRouter(
    prefix="/booking",
    tags=["Бронирования"],
)


class BookingRequest(BaseModel):
    room_id: int
    date_from: date
    date_to: date


@router.post("/add", response_model=SchemeBooking)
async def add_booking(
        booking_request: BookingRequest,
        background_tasks: BackgroundTasks,
        user: User = Depends(get_current_user)
):
    new_booking = await BookingDAO.add(user.id, booking_request.room_id,
                                       booking_request.date_from, booking_request.date_to)

    if not new_booking:
        raise RoomCannotBeBooked

    background_tasks.add_task(send_booking_message, new_booking, user.email)
    return new_booking
