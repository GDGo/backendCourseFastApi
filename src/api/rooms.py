from datetime import date

from fastapi import APIRouter, Body, Query
from fastapi_cache.decorator import cache

from src.Exceptions import ObjectNotFoundException, HotelNotFoundHTTPException, RoomNotFoundHTTPException, \
    RoomNotFoundException, HotelNotFoundException, RoomAlreadyExistHTTPException, ObjectAlreadyExistException, \
    ObjectNotDeleteException, RoomNotDeleteHTTPException, ObjectNotCreatedException, FacilityAddBulkHTTPException
from src.api.dependencies import UserIdDep, DBDep
from src.schemas.rooms import RoomAddRequest, RoomPatchRequest
from src.services.rooms import RoomService

router: APIRouter = APIRouter(
    prefix="/hotels",
    tags=["Номера"]
)


@router.get("/{hotel_id}/rooms",
            name="Получить номера",
            description="Все доступные номера в отеле на определенную дату")
@cache(expire=10)
async def get_rooms(
        user: UserIdDep,
        db: DBDep,
        hotel_id: int,
        date_from: date = Query(examples="2025-08-01"),
        date_to: date = Query(examples="2025-08-10"),

):
    try:
        await db.hotels.get_one(id=hotel_id)
    except ObjectNotFoundException:
        raise HotelNotFoundHTTPException
    rooms = await RoomService(db).get_filtered_by_time(
        hotel_id=hotel_id,
        date_from=date_from,
        date_to=date_to)
    return {"status": "OK", "data": rooms}


@router.get("/{hotel_id}/rooms/{room_id}",
            name="Получить один номер")
@cache(expire=10)
async def get_room(
        user: UserIdDep,
        db: DBDep,
        hotel_id: int,
        room_id: int
):
    try:
        await db.hotels.get_one(id=hotel_id)
    except ObjectNotFoundException:
        raise HotelNotFoundHTTPException

    try:
        return await RoomService(db).get_one_or_none_with_rels(room_id=room_id, hotel_id=hotel_id)
    except RoomNotFoundException:
        raise RoomNotFoundHTTPException


@router.post("/{hotel_id}/rooms",
             name="Добавить номер")
async def add_rooms(
        user: UserIdDep,
        db: DBDep,
        hotel_id: int,
        room_data: RoomAddRequest = Body(openapi_examples={
    "1": {"summary": "Номер Эконом", "value": {
        "title": "Эконом",
        "description": "Эконом",
        "price": 100,
        "quantity": 10,
        "facilities_ids": [1,2,3,4]
    }},
    "2": {"summary": "Номер Комфорт", "value": {
        "title": "Комфорт",
        "description": "Комфорт",
        "price": 200,
        "quantity": 5,
        "facilities_ids": [1,2,3,4]
    }},
    "3": {"summary": "Номер Люкс", "value": {
        "title": "Люкс",
        "description": "Люкс",
        "price": 400,
        "quantity": 2,
        "facilities_ids": [1,2,3,4]
    }}
    })
):
    try:
        room = await RoomService(db).create_room(hotel_id=hotel_id, room_data=room_data)
    except HotelNotFoundException:
        raise HotelNotFoundHTTPException
    except ObjectAlreadyExistException:
        raise RoomAlreadyExistHTTPException
    except ObjectNotCreatedException:
        raise FacilityAddBulkHTTPException
    return {"status": "OK", "data": room}


@router.put("/{hotel_id}/rooms/{room_id}",
            name="Полное обновление номера")
async def put_room(
        user: UserIdDep,
        db: DBDep,
        hotel_id: int,
        room_id: int,
        room_data: RoomAddRequest
):
    try:
        await RoomService(db).put_room(hotel_id=hotel_id,room_id=room_id,room_data=room_data)
    except HotelNotFoundException:
        raise HotelNotFoundHTTPException
    except RoomNotFoundException:
        raise RoomNotFoundHTTPException
    return {"status": "OK"}


@router.patch("/{hotel_id}/rooms/{room_id}",
              name="Частичное изменение номера")
async def patch_room(
        user: UserIdDep,
        db: DBDep,
        hotel_id: int,
        room_id: int,
        room_data: RoomPatchRequest
):
    try:
        await RoomService(db).patch_room(hotel_id=hotel_id,room_id=room_id,room_data=room_data)
    except HotelNotFoundException:
        raise HotelNotFoundHTTPException
    except RoomNotFoundException:
        raise RoomNotFoundHTTPException
    return {"status": "OK"}


@router.delete("/{hotel_id}/rooms/{room_id}",
               name="Удалить номер")
async def delete_room(
        user: UserIdDep,
        db: DBDep,
        hotel_id: int,
        room_id: int
):
    try:
        await RoomService(db).delete_room(hotel_id=hotel_id, room_id=room_id)
    except HotelNotFoundException:
        raise HotelNotFoundHTTPException
    except RoomNotFoundException:
        raise RoomNotFoundHTTPException
    except ObjectNotDeleteException as ex:
        raise RoomNotDeleteHTTPException
    return {"status": "OK"}