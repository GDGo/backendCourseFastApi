from datetime import date

from sqlalchemy import select

from src.Exceptions import AllRoomsAreBookedException
from src.models.bookings import BookingsOrm
from src.models.rooms import RoomsOrm
from src.repositories.base import BaseRepository
from src.repositories.mappers.mappers import BookingDataMapper
from src.repositories.utils import rooms_ids_for_booking
from src.schemas.bookings import BookingAdd


class BookingsRepository(BaseRepository):
    model = BookingsOrm
    mapper = BookingDataMapper

    async def get_bookings_with_today_chekin(self):
        query = (
            select(BookingsOrm)
            .filter(BookingsOrm.date_from == date.today())
        )
        bookings = await self.session.execute(query)
        return [self.mapper.map_to_domain_entity(booking) for booking in bookings.scalars().all()]

    async def add_booking(self, data: BookingAdd):
        id_hotel = (await self.session.execute(
            select(RoomsOrm.hotel_id)
            .filter(RoomsOrm.id == data.room_id)
            )
        ).scalars().all()[0]

        rooms_ids_to_get = rooms_ids_for_booking(
            hotel_id=id_hotel,
            date_to=data.date_to,
            date_from=data.date_from
        )

        ids_room = (await self.session.execute(
            rooms_ids_to_get
            )
        ).scalars().all()

        if data.room_id not in ids_room:
            raise AllRoomsAreBookedException

        return await self.add(data)