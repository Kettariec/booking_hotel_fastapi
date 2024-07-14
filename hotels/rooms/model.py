from database import Base
from sqlalchemy import Column, JSON, Integer, String, ForeignKey
from sqlalchemy.orm import relationship


class Room(Base):
    __tablename__ = "rooms"

    id = Column(Integer, primary_key=True, nullable=False)
    hotel_id = Column(ForeignKey("hotels.id"), nullable=False)
    name = Column(String, nullable=False)
    description = Column(String, nullable=False)
    services = Column(JSON, nullable=False)
    price = Column(Integer, nullable=False)
    quantity = Column(Integer, nullable=False)
    image_id = Column(Integer)

    hotel = relationship("Hotel", back_populates='room')
    booking = relationship("Booking", back_populates='room')

    def __str__(self):
        return f'{self.name}'
