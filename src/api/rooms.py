from datetime import date

from fastapi import APIRouter, Body, Query, HTTPException
from fastapi_cache.decorator import cache

from src.Exceptions import ObjectNotFoundException, InvalidDatesException
from src.api.dependencies import UserIdDep, DBDep
from src.repositories.utils import check_dates
from src.schemas.facilities import RoomFacilityAdd
from src.schemas.rooms import RoomAdd, RoomPatch, RoomAddRequest, RoomPatchRequest


router: APIRouter = APIRouter(
    prefix="/hotels",
    tags=["Номера"]
)


@router.get("/{hotel_id}/rooms")
@cache(expire=10)
async def get_rooms(
        user: UserIdDep,
        db: DBDep,
        hotel_id: int,
        date_from: date = Query(examples="2025-08-01"),
        date_to: date = Query(examples="2025-08-10"),

):
    try:
        check_dates(date_from, date_to)
    except InvalidDatesException as ex:
        raise HTTPException(422, detail=ex.detail)

    return await db.rooms.get_filtered_by_time(
        hotel_id=hotel_id,
        date_to= date_to,
        date_from= date_from,
    )


@router.get("/{hotel_id}/rooms/{room_id}")
@cache(expire=10)
async def get_room(
        user: UserIdDep,
        db: DBDep,
        hotel_id: int,
        room_id: int
):
    try:
        return await db.rooms.get_one_or_none_with_rels(id=room_id, hotel_id=hotel_id)
    except ObjectNotFoundException:
        raise HTTPException(404, detail="Номера не существует")


@router.post("/{hotel_id}/rooms")
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
        await db.rooms.get_one(hotel_id=hotel_id)
    except ObjectNotFoundException:
        raise HTTPException(404, detail="Отеля не существует")
    _room_data = RoomAdd(hotel_id=hotel_id, **room_data.model_dump())
    room = await db.rooms.add(_room_data)

    rooms_facilities_data = [RoomFacilityAdd(room_id=room.id, facility_id=f_id) for f_id in room_data.facilities_ids]
    await db.rooms_facilities.add_bulk(rooms_facilities_data)
    await db.commit()
    return {"status": "OK", "data": room}


@router.put("/{hotel_id}/rooms/{room_id}")
async def put_room(
        user: UserIdDep,
        db: DBDep,
        hotel_id: int,
        room_id: int,
        room_data: RoomAddRequest
):
    try:
        await db.rooms.get_one(id=room_id)
    except ObjectNotFoundException:
        raise HTTPException(404, detail="Номера не существует")
    _room_data = RoomAdd(hotel_id=hotel_id, **room_data.model_dump())
    await db.rooms.edit(
        _room_data,
        id=room_id,
        hotel_id=hotel_id
    )
    await db.rooms_facilities.set_rooms_facilities(room_id=room_id, facilities_ids=room_data.facilities_ids)
    await db.commit()
    return {"status": "OK"}


@router.patch("/{hotel_id}/rooms/{room_id}")
async def patch_room(
        user: UserIdDep,
        db: DBDep,
        hotel_id: int,
        room_id: int,
        room_data: RoomPatchRequest
):
    try:
        await db.rooms.get_one(id=room_id)
    except ObjectNotFoundException:
        raise HTTPException(404, detail="Номера не существует")
    _room_data_dict = room_data.model_dump(exclude_unset=True)
    _room_data = RoomPatch(hotel_id=hotel_id, **_room_data_dict)
    await db.rooms.edit(
        _room_data,
        exclude_unset=True,
        id=room_id,
        hotel_id=hotel_id
    )
    if "facilities_ids" in _room_data_dict:
        await (db.rooms_facilities.set_rooms_facilities(
            room_id=room_id,
            facilities_ids=_room_data_dict["facilities_ids"])
        )
    await db.commit()
    return {"status": "OK"}


@router.delete("/{hotel_id}/rooms/{room_id}")
async def delete_room(
        user: UserIdDep,
        db: DBDep,
        hotel_id: int,
        room_id: int
):
    try:
        await db.rooms.get_one(id=room_id)
    except ObjectNotFoundException:
        raise HTTPException(404, detail="Номера не существует")
    await db.rooms.delete(id=room_id, hotel_id=hotel_id)
    await db.commit()
    return {"status":"OK"}