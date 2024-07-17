from pydantic import BaseModel
from pydantic import Field


class SchemeHotel(BaseModel):
    location: str
    hotel_id: int
    name: str
    description: str
    hotel_services: dict
    stars: int = Field(None, ge=1, le=5)
    rooms_quantity: int
    hotel_image_id: int
    rooms_name: str
    rooms_description: str
    room_id: int
    room_services: dict
    price: int
    room_image_id: int

    class Config:
        from_attributes = True
