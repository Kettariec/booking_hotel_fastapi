from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from redis import asyncio as aioredis
from sqladmin import Admin, ModelView
from admin.auth import authentication_backend
from bookings.router import router as router_booking
from database import engine
from hotels.router import router as router_hotel
from images.router import router as router_images
from pages.router import router as router_pages
from users.router import router as router_user
from hotels.rooms.router import router as router_rooms
from admin.admin import UserAdmin, BookingAdmin, HotelAdmin, RoomAdmin

app = FastAPI()


app.mount("/static", StaticFiles(directory="static"), "static")

app.include_router(router_user)
app.include_router(router_booking)
app.include_router(router_hotel)
app.include_router(router_rooms)
app.include_router(router_pages)
app.include_router(router_images)


admin = Admin(app, engine, authentication_backend=authentication_backend)

admin.add_view(UserAdmin)
admin.add_view(BookingAdmin)
admin.add_view(HotelAdmin)
admin.add_view(RoomAdmin)


@app.on_event("startup")
async def startup():
    redis = aioredis.from_url("redis://localhost:6379", encoding="utf8", decode_responses=True)
    FastAPICache.init(RedisBackend(redis), prefix="cache")
