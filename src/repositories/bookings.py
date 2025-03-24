from sqlalchemy import select

from src.models.bookings import BookingsOrm
from src.models.rooms import RoomsOrm
from src.schemas.rooms import Room
from src.repositories.base import BaseRepository
from src.schemas.bookings import Booking


class BookingsRepository(BaseRepository):
    model = BookingsOrm
    schema = Booking

    async def get_price(self, **filter_by):
        query = select(RoomsOrm).filter_by(**filter_by)
        result = await self.session.execute(query)
        model = result.scalars().one_or_none()
        if (model is None):
            return None
        room = Room.model_validate(model, from_attributes=True)
        return room.price