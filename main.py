from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
# from fastapi_cache import FastAPICache
# from fastapi_cache.backends.redis import RedisBackend
# from redis import asyncio as aioredis
from sqladmin import Admin, ModelView
from admin.auth import authentication_backend
from bookings.model import Booking
from bookings.router import router as router_booking
from database import engine
from hotels.model import Hotel
from hotels.rooms.model import Room
from hotels.rooms.router import router as router_room
from hotels.router import router as router_hotel
from images.router import router as router_images
from pages.router import router as router_pages
from users.model import User
from users.router import router as router_user

app = FastAPI()


app.mount("/static", StaticFiles(directory="static"), "static")

app.include_router(router_user)
app.include_router(router_booking)
app.include_router(router_hotel)
app.include_router(router_room)
app.include_router(router_pages)
app.include_router(router_images)


# @app.on_event("startup")
# async def startup():
#     redis = aioredis.from_url("redis://localhost:6379", encoding="utf8", decode_responses=True)
#     FastAPICache.init(RedisBackend(redis), prefix="cache")

# админка
admin = Admin(app, engine, authentication_backend=authentication_backend)


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
    name = "Бронь"
    name_plural = "Брони"


class HotelAdmin(ModelView, model=Hotel):
    column_list = [c.name for c in Hotel.__table__.c]
    name = "Отель"
    name_plural = "Отели"


class RoomAdmin(ModelView, model=Room):
    column_list = [c.name for c in Room.__table__.c] + [Room.hotel]
    name = "Комната"
    name_plural = "Комнаты"


admin.add_view(UserAdmin)
admin.add_view(BookingAdmin)
admin.add_view(HotelAdmin)
admin.add_view(RoomAdmin)
