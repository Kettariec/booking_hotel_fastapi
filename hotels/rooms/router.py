from fastapi import APIRouter, Query
from datetime import date
from typing import List
from hotels.rooms.dao import RoomDAO
from hotels.rooms.scheme import SchemeRoom

router = APIRouter(
    prefix="/rooms",
    tags=["Комнаты"],
)


@router.get("", response_model=List[SchemeRoom])
async def get_rooms_by_hotel_and_time(
    hotel_id: int,
    date_from: date = Query(..., description="Дата начала в формате YYYY-MM-DD"),
    date_to: date = Query(..., description="Дата окончания в формате YYYY-MM-DD")
):
    rooms = await RoomDAO.search_available_rooms(hotel_id, date_from, date_to)
    return rooms
