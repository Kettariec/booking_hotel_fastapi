from fastapi import APIRouter, Depends, HTTPException, status
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


@router.delete("/delete/{booking_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_booking(
        booking_id: int,
        user: User = Depends(get_current_user)
):
    booking = await BookingDAO.get_bookings_by_user_id(user.id)
    if not any(b.id == booking_id for b in booking):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Бронирование не найдено")

    deleted = await BookingDAO.delete_booking_by_id(booking_id)
    if not deleted:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Не удалось удалить бронирование")

    return None
