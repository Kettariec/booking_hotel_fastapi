from sqladmin import ModelView
from bookings.model import Booking
from hotels.model import Hotel
from hotels.rooms.model import Room
from users.model import User


class UserAdmin(ModelView, model=User):
    column_list = [User.id, User.email]
    can_delete = False
    name = "Пользователь"
    name_plural = "Пользователи"
    icon = "fa-solid fa-user"
    category = "accounts"
    column_list = [User.id, User.email]
    column_details_exclude_list = [User.hashed_password] # чтобы в админке не отображался хешированный пароль


class BookingAdmin(ModelView, model=Booking):
    column_list = [c.name for c in Booking.__table__.c] + [Booking.user]
    name = "Бронирование"
    name_plural = "Бронирования"


class HotelAdmin(ModelView, model=Hotel):
    column_list = [c.name for c in Hotel.__table__.c]
    name = "Отель"
    name_plural = "Отели"


class RoomAdmin(ModelView, model=Room):
    column_list = [c.name for c in Room.__table__.c] + [Room.hotel]
    name = "Комната"
    name_plural = "Комнаты"
