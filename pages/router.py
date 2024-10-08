from fastapi import APIRouter, Request, Depends, Query
from fastapi.templating import Jinja2Templates
from hotels.router import get_hotels_by_location_and_time
from datetime import date
from hotels.rooms.dao import RoomDAO
from hotels.rooms.scheme import SchemeRoom
from fastapi.responses import HTMLResponse
from typing import List
from hotels.scheme import SchemeHotel
# from fastapi_cache.decorator import cache

router = APIRouter(
    prefix="",
    tags=["Фронтенд"]
)

templates = Jinja2Templates(directory="templates")


@router.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@router.get("/search", response_class=HTMLResponse,
            response_model=List[SchemeHotel])
# @cache(expire=180)
async def get_hotels_page(
        request: Request,
        location: str,
        date_from: date,
        date_to: date,
        hotels=Depends(get_hotels_by_location_and_time)
):
    return templates.TemplateResponse(name="hotels.html",
                                      context={"request": request,
                                               "hotels": hotels,
                                               "date_from": date_from,
                                               "date_to": date_to})


@router.get("/hotels/{hotel_id}", response_class=HTMLResponse,
            response_model=List[SchemeHotel])
# @cache(expire=180)
async def get_hotel_rooms_page(
    request: Request,
    hotel_id: int,
    date_from: date = Query(..., description="Дата начала в формате YYYY-MM-DD"),
    date_to: date = Query(..., description="Дата окончания в формате YYYY-MM-DD")
):
    rooms = await RoomDAO.search_available_rooms(hotel_id, date_from, date_to)
    return templates.TemplateResponse("hotel_rooms.html", {
        "request": request,
        "rooms": rooms,
        "date_from": date_from,
        "date_to": date_to
    })


@router.get("/rooms/{room_id}", response_class=HTMLResponse,
            response_model=SchemeRoom)
async def get_room_page(
        request: Request,
        room_id: int,
        date_from: date = Query(..., description="Дата начала в формате YYYY-MM-DD"),
        date_to: date = Query(..., description="Дата окончания в формате YYYY-MM-DD")
):
    room = await RoomDAO.find_by_id(room_id)
    return templates.TemplateResponse("room.html", {
        "request": request,
        "room": room,
        "date_from": date_from,
        "date_to": date_to
    })
