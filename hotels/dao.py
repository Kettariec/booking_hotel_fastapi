from dao.base import BaseDAO
from hotels.model import Hotel
from database import async_session_maker, engine
from datetime import date
from sqlalchemy import select, func, and_, or_
from bookings.model import Booking
from hotels.rooms.model import Room
import logging


class HotelDAO(BaseDAO):
    model = Hotel

    @classmethod
    async def search_hotels(cls, location: str, date_from: date, date_to: date):
        async with async_session_maker() as session:
            # CTE для забронированных комнат
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

            # Подзапрос для свободных комнат
            free_rooms_subquery = select(
                Room.hotel_id,
                (Room.quantity - func.count(booked_rooms.c.room_id)).label("free_rooms")
            ).select_from(Room).join(
                booked_rooms, booked_rooms.c.room_id == Room.id, isouter=True
            ).group_by(Room.hotel_id, Room.quantity).subquery()

            # Запрос на получение отелей в указанной локации с свободными комнатами
            get_hotels = select(
                Hotel.id.label("id_hotel"),
                Hotel.name,
                Hotel.location,
                Hotel.description,
                Hotel.services,
                Hotel.stars,
                Hotel.image_id,
                free_rooms_subquery.c.free_rooms.label("rooms_quantity")
            ).select_from(Hotel).join(
                free_rooms_subquery, free_rooms_subquery.c.hotel_id == Hotel.id
            ).where(
                and_(
                    Hotel.location == location,
                    free_rooms_subquery.c.free_rooms > 0
                )
            )

            logging.info(get_hotels.compile(engine, compile_kwargs={"literal_binds": True}))

            hotels_result = await session.execute(get_hotels)
            hotels = hotels_result.fetchall()

            return hotels
