from fastapi import APIRouter, Body

from src.api.dependencies import DBDep, UserIdDep
from src.schemas.bookings import BookingAdd, BookingAddRequest


router = APIRouter(
    prefix="/bookings",
    tags=["Бронирование"]
)


@router.post("")
async def add_booking(
        user_id: UserIdDep,
        db: DBDep,
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
    price = await db.bookings.get_price(id=booking_data.room_id)
    _booking_data = BookingAdd(
        user_id=user_id,
        **booking_data.model_dump(),
        price=price
    )
    booking = await db.bookings.add(_booking_data)
    await db.commit()
    return {"status": "OK", "data":booking}