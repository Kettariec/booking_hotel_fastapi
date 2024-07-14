from fastapi import APIRouter, Query
from datetime import datetime, date
from hotels.rooms.dao import RoomDAO
from typing import List
from pydantic import BaseModel
from hotels.rooms.scheme import SchemeRoom

router = APIRouter(
    prefix="",
    tags=["Комнаты"],
)

@router.get("/{hotel_id}/rooms")
async def get_rooms_by_time(
        hotel_id: int,
        date_from: date = Query(..., description=f"Например, {datetime.now().date()}"),
        date_to: date = Query(..., description=f"Например, {datetime.now().date()}"),
) -> List[SchemeRoom]:
    rooms = await RoomDAO.search_for_rooms(hotel_id, date_from, date_to)
    return rooms
