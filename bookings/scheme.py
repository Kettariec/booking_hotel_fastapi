from pydantic import BaseModel
from datetime import date


class SchemeBooking(BaseModel):
    id: int
    room_id: int
    room_name: str
    user_id: int
    date_from: date
    date_to: date
    price: int
    total_days: int
    total_cost: int
    hotel_id: int
    hotel_name: str
    hotel_location: str

    class Config:
        from_attributes = True
