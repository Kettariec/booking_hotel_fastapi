from fastapi import APIRouter, Depends
from bookings.dao import BookingDAO
from users.model import User
from users.dependencies import get_current_user
from datetime import date
from exceptions import RoomCannotBeBooked
from fastapi import BackgroundTasks
from tasks.tasks import send_booking_message


router = APIRouter(
    prefix="/bookings",
    tags=["Бронирования"],
)


@router.post("")
async def add_booking(
        background_tasks: BackgroundTasks,
        room_id: int, date_from: date, date_to: date,
        user: User = Depends(get_current_user),
):
    new_booking = await BookingDAO.add(user.id, room_id, date_from, date_to)

    if not new_booking:
        raise RoomCannotBeBooked

    background_tasks.add_task(send_booking_message, user.email)
