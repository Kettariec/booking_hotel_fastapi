from bookings.model import Booking
from dao.base import BaseDAO
from datetime import date
from sqlalchemy import insert, select, func, and_, or_
from hotels.rooms.model import Room
from database import async_session_maker, engine
import logging

logging.basicConfig(level=logging.INFO)


class BookingDAO(BaseDAO):
    model = Booking

    @classmethod
    async def add(cls,
                  user_id: int,
                  room_id: int,
                  date_from: date,
                  date_to: date,
                  ):
        async with async_session_maker() as session:
            booked_rooms = select(Booking).where(
                and_(
                    Booking.room_id == room_id,
                    or_(
                        and_(
                            Booking.date_from >= date_from,
                            Booking.date_from <= date_to
                        ),
                        and_(
                            Booking.date_from <= date_from,
                            Booking.date_to > date_from
                        ),
                    )
                )
            ).cte("booked_rooms")

            get_free_rooms = select(
                (Room.quantity - func.count(booked_rooms.c.room_id)).label("free_rooms")
            ).select_from(Room).join(
                booked_rooms, booked_rooms.c.room_id == Room.id, isouter=True
            ).where(Room.id == room_id).group_by(
                Room.quantity, booked_rooms.c.room_id
            )

            print(get_free_rooms.compile(engine, compile_kwargs={"literal_binds": True}))

            free_rooms = await session.execute(get_free_rooms)
            free_rooms: int = free_rooms.scalar()
            print(free_rooms)

            if free_rooms is None or free_rooms > 0:
                get_price = select(Room.price).where(Room.id == room_id)
                price = await session.execute(get_price)
                price: int = price.scalar()
                add_booking = insert(Booking).values(
                    room_id=room_id,
                    user_id=user_id,
                    date_from=date_from,
                    date_to=date_to,
                    price=price,
                ).returning(Booking)

                new_booking = await session.execute(add_booking)
                await session.commit()

                return new_booking.scalar()

            else:
                return None
