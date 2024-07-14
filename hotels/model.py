from database import Base
from sqlalchemy import Column, JSON, Integer, String
from sqlalchemy.orm import relationship


class Hotel(Base):
    __tablename__ = "hotels"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    location = Column(String, nullable=False)
    description = Column(String, nullable=False)
    services = Column(JSON)
    rooms_quantity = Column(Integer, nullable=False)
    stars = Column(Integer)
    image_id = Column(Integer)

    room = relationship("Room", back_populates='hotel')

    def __str__(self):
        return f'{self.name}'
