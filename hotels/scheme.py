from pydantic import BaseModel
from pydantic import Field


class SchemeHotel(BaseModel):
    location: str
    id_hotel: int
    name: str
    description: str
    services: dict
    rooms_quantity: int
    stars: int = Field(None, ge=1, le=5)
    image_id: int

    class Config:
        from_attributes = True
