from fastapi import APIRouter, Query
from datetime import date
from typing import List
from hotels.scheme import SchemeHotel
from hotels.dao import HotelDAO
from fastapi.templating import Jinja2Templates
from hotels.rooms.dao import RoomDAO
from hotels.rooms.scheme import SchemeRoom

router = APIRouter(
    prefix="/hotels",
    tags=["Отели"],
)

templates = Jinja2Templates(directory="templates")


@router.get("", response_model=List[SchemeHotel])
async def get_hotels_by_location_and_time(
    location: str,
    date_from: date = Query(..., description="Дата начала в формате YYYY-MM-DD"),
    date_to: date = Query(..., description="Дата окончания в формате YYYY-MM-DD")
):
    hotels = await HotelDAO.search_hotels(location, date_from, date_to)
    return hotels


@router.get("/rooms", response_model=List[SchemeRoom])
async def get_rooms_by_hotel_time(
    hotel_id: int,
    date_from: date = Query(..., description="Дата начала в формате YYYY-MM-DD"),
    date_to: date = Query(..., description="Дата окончания в формате YYYY-MM-DD")
):
    rooms = await RoomDAO.find_available_rooms(hotel_id, date_from, date_to)
    return rooms
