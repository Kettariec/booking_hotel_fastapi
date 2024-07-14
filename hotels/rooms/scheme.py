from pydantic import BaseModel


class SchemeRoom(BaseModel):
    id: int
    hotel_id: int
    name: str
    description: str
    services: dict
    price: int
    quantity: int
    image_id: int

    class Config:
        from_attributes = True
