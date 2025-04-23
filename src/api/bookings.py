from fastapi import APIRouter, Body, HTTPException
from fastapi_cache.decorator import cache

from src.Exceptions import ObjectNotFoundException
from src.api.dependencies import DBDep, UserIdDep
from src.schemas.bookings import BookingAdd, BookingAddRequest


router = APIRouter(
    prefix="/bookings",
    tags=["Бронирование"]
)


@router.get("")
@cache(expire=10)
async def get_all_bookings(
        db: DBDep,
):
    return await db.bookings.get_all()


@router.get("/me")
@cache(expire=10)
async def get_my_bookings(
        user_id: UserIdDep,
        db: DBDep,
):
    return await db.bookings.get_filtered(user_id=user_id)


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
    try:
        room = await db.rooms.get_one(id=booking_data.room_id)
    except ObjectNotFoundException:
        raise HTTPException(404, detail="Номер не найден")
    room_price = room.price
    _booking_data = BookingAdd(
        user_id=user_id,
        **booking_data.model_dump(),
        price=room_price
    )
    booking = await db.bookings.add_booking(_booking_data)
    await db.commit()
    return {"status": "OK", "data": booking}