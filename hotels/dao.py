from dao.base import BaseDAO
from hotels.model import Hotel
from database import async_session_maker, engine
from datetime import date
from sqlalchemy import select, func, and_, or_
from bookings.model import Booking
from hotels.rooms.model import Room
import logging
from hotels.scheme import SchemeHotel


class HotelDAO(BaseDAO):
    model = Hotel

    @classmethod
    async def search_hotels(cls, location: str, date_from: date, date_to: date):
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

            free_rooms_subquery = select(
                Room.id,
                Room.name.label("rooms_name"),
                Room.description.label("rooms_description"),
                Room.hotel_id,
                Room.services.label("room_services"),
                Room.price,
                Room.image_id.label("room_image_id"),
                (Room.quantity - func.count(booked_rooms.c.room_id)).label("free_rooms")
            ).select_from(Room).join(
                booked_rooms, booked_rooms.c.room_id == Room.id, isouter=True
            ).group_by(Room.id, Room.quantity).subquery()

            get_hotels = select(
                Hotel.id.label("hotel_id"),
                Hotel.name,
                Hotel.location,
                Hotel.description,
                Hotel.services.label("hotel_services"),
                Hotel.stars,
                Hotel.image_id.label("image_id"),
                free_rooms_subquery.c.free_rooms.label("rooms_quantity"),
                free_rooms_subquery.c.rooms_name.label("rooms_name"),
                free_rooms_subquery.c.rooms_description.label("rooms_description"),
                free_rooms_subquery.c.id.label("room_id"),
                free_rooms_subquery.c.hotel_id,
                free_rooms_subquery.c.room_services.label("room_services"),
                free_rooms_subquery.c.price.label("price"),
                free_rooms_subquery.c.room_image_id.label("room_image_id"),
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

            # Преобразование результатов запроса в список объектов SchemeHotel
            scheme_hotels = []
            for hotel_row in hotels:
                hotel_data = {
                    "hotel_id": hotel_row.hotel_id,
                    "name": hotel_row.name,
                    "location": hotel_row.location,
                    "description": hotel_row.description,
                    "hotel_services": hotel_row.hotel_services,
                    "stars": hotel_row.stars,
                    "hotel_image_id": int(hotel_row.image_id),
                    "rooms_quantity": hotel_row.rooms_quantity,
                    "rooms_name": str(hotel_row.rooms_name),
                    "rooms_description": str(hotel_row.rooms_description),
                    "room_id": int(hotel_row.room_id),
                    "room_services": hotel_row.room_services,
                    "price": int(hotel_row.price),
                    "room_image_id": int(hotel_row.room_image_id),
                }
                scheme_hotel = SchemeHotel(**hotel_data)
                scheme_hotels.append(scheme_hotel)

            return scheme_hotels
