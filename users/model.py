from database import Base
from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import relationship


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, nullable=False)
    email = Column(String, nullable=False)
    hashed_password = Column(String, nullable=False)
    is_email_verified = Column(Boolean, default=False)

    booking = relationship("Booking", back_populates='user')

    def __str__(self):
        return f'User {self.email}'
