from fastapi import APIRouter, Body, HTTPException
from fastapi_cache.decorator import cache

from src.Exceptions import ObjectNotFoundException, AllRoomsAreBookedException, RoomNotFoundHTTPException, \
    AllRoomsAreBookedHTTPException
from src.api.dependencies import DBDep, UserIdDep
from src.schemas.bookings import BookingAdd, BookingAddRequest
from src.services.bookings import BookingService


router = APIRouter(
    prefix="/bookings",
    tags=["Бронирование"]
)


@router.get("",
            name="Все бронирования",
            description="Бронирования всех пользователей, для просмотра не требуется аутентификация")
@cache(expire=10)
async def get_all_bookings(
        db: DBDep,
):
    return await BookingService(db).get_all_bookings()


@router.get("/me",
            name="Мои бронирования",
            description="Бронирования только текущего пользователя")
@cache(expire=10)
async def get_my_bookings(
        user_id: UserIdDep,
        db: DBDep,
):
    return await BookingService(db).get_my_bookings(user_id=user_id)


@router.post("", name="Добавить бронирование")
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
        booking = await BookingService(db).add_booking(user_id=user_id, booking_data=booking_data)
    except ObjectNotFoundException:
        raise RoomNotFoundHTTPException
    except AllRoomsAreBookedException:
        raise AllRoomsAreBookedHTTPException
    return {"status": "OK", "data": booking}