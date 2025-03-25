from datetime import date

from src.models.rooms import RoomsOrm
from src.repositories.base import BaseRepository
from src.repositories.utils import rooms_ids_for_booking
from src.schemas.rooms import Room


class RoomsRepository(BaseRepository):
    model = RoomsOrm
    schema = Room

    async def get_filtered_by_time(
            self,
            hotel_id: int,
            date_to: date,
            date_from: date,
    ):
        rooms_ids_to_get = rooms_ids_for_booking(date_to, date_from, hotel_id)
        return await self.get_filtered(RoomsOrm.id.in_(rooms_ids_to_get))