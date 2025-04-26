from datetime import date

from src.Exceptions import check_dates, ObjectNotDelete, RoomNotFoundException, ObjectNotFoundException, \
    HotelNotFoundException
from src.api.dependencies import PaginationDep
from src.schemas.hotels import HotelAdd
from src.services.base import BaseService


class HotelService(BaseService):

    async def get_filtered_by_time(self,
        pagination: PaginationDep,
        location: str,
        title: str,
        date_from: date,
        date_to: date,
    ):
        check_dates(date_from, date_to)
        per_page = pagination.per_page or 5
        return await self.db.hotels.get_filtered_by_time(
            date_to=date_to,
            date_from=date_from,
            location=location,
            title=title,
            limit=pagination.per_page or 5,
            offset=per_page * (pagination.page - 1)
        )

    async def get_hotel(self, hotel_id: int):
        return await self.db.hotels.get_one(id=hotel_id)

    async def create_hotel(self, hotel_data: HotelAdd):
        hotel = await self.db.hotels.add(hotel_data)
        await self.db.commit()
        return hotel

    async def edit_hotel(self,hotel_id, hotel_data):
        await self.get_hotel_with_check(hotel_id=hotel_id)
        await self.db.hotels.edit(hotel_data, id=hotel_id)
        await self.db.commit()

    async def partionally_edit(self, hotel_id, hotel_data):
        await self.get_hotel_with_check(hotel_id=hotel_id)
        await self.db.hotels.edit(hotel_data, exclude_unset=True, id=hotel_id)
        await self.db.commit()

    async def delete_hotel(self, hotel_id):
        await self.get_hotel_with_check(hotel_id=hotel_id)
        await self.db.hotels.delete(id=hotel_id)
        await self.db.commit()

    async def get_hotel_with_check(self, hotel_id: int) -> None:
        try:
            return await self.db.hotels.get_one(id=hotel_id)
        except ObjectNotFoundException:
            raise HotelNotFoundException