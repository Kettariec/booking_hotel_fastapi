from dao.base import BaseDAO
from hotels.rooms.model import Room


class RoomDAO(BaseDAO):
    model = Room

    @classmethod
    async def search_for_rooms(cls):
        pass
