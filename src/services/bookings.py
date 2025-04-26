from fastapi import Body

from src.schemas.bookings import BookingAddRequest, BookingAdd
from src.services.base import BaseService


class BookingService(BaseService):

    async def get_all_bookings(self):
        return await self.db.bookings.get_all()

    async def get_my_bookings(
            self,
            user_id: int,
    ):
        return await self.db.bookings.get_filtered(user_id=user_id)

    async def add_booking(
            self,
            user_id: int,
            booking_data: BookingAddRequest = Body(openapi_examples={
                "1": {"summary": "Бронь номера Эконом", "value": {
                    "date_from": "2025-08-19",
                    "date_to": "2025-08-27",
                    "room_id": 99
                }},
                "2": {"summary": "Бронь номера Люкс", "value": {
                    "date_from": "2025-09-09",
                    "date_to": "2025-09-27",
                    "room_id": 103
                }},
            })
    ):
        room = await self.db.rooms.get_one(id=booking_data.room_id)
        room_price = room.price
        _booking_data = BookingAdd(
            user_id=user_id,
            **booking_data.model_dump(),
            price=room_price
        )
        booking = await self.db.bookings.add_booking(_booking_data)
        await self.db.commit()
        return booking