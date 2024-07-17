from dao.base import BaseDAO
from hotels.rooms.model import Room
from database import async_session_maker
from datetime import date
from bookings.model import Booking
from sqlalchemy import select, and_, or_, not_, func


class RoomDAO(BaseDAO):
    model = Room

    @classmethod
    async def search_available_rooms(cls, hotel_id: int, date_from: date, date_to: date):
        async with async_session_maker() as session:
            booked_rooms = select(Booking.room_id).where(
                or_(
                    and_(
                        Booking.date_from >= date_from,
                        Booking.date_from <= date_to
                    ),
                    and_(
                        Booking.date_from <= date_from,
                        Booking.date_to > date_from
                    )
                )
            ).cte("booked_rooms")

            free_rooms_query = (
                select(Room)
                .join(booked_rooms, isouter=True)
                .group_by(Room.id)
                .having((Room.quantity - func.count(booked_rooms.c.room_id)) > 0)
                .where(Room.hotel_id == hotel_id)
            )

            result = await session.execute(free_rooms_query)
            return result.scalars().all()
