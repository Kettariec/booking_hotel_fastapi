from fastapi import APIRouter, Query
from datetime import date
from typing import List
from hotels.scheme import SchemeHotel
from hotels.dao import HotelDAO
from fastapi.templating import Jinja2Templates

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
