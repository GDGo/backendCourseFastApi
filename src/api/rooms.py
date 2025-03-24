from fastapi import APIRouter, Body

from src.api.dependencies import UserIdDep, DBDep
from src.schemas.rooms import RoomAdd, RoomPatch, RoomAddRequest, RoomPatchRequest


router: APIRouter = APIRouter(
    prefix="/hotels",
    tags=["Номера"]
)


@router.get("/{hotel_id}/rooms")
async def get_rooms(
        user: UserIdDep,
        db: DBDep,
        hotel_id: int
):
    return await db.rooms.get_filtered(hotel_id=hotel_id)


@router.get("/{hotel_id}/rooms/{room_id}")
async def get_room(
        user: UserIdDep,
        db: DBDep,
        hotel_id: int,
        room_id: int):
    return await db.rooms.get_one_or_none(id=room_id, hotel_id=hotel_id)


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
        "quantity": 10
    }},
    "2": {"summary": "Номер Комфорт", "value": {
        "title": "Комфорт",
        "description": "Комфорт",
        "price": 200,
        "quantity": 5
    }},
    "3": {"summary": "Номер Люкс", "value": {
        "title": "Люкс",
        "description": "Люкс",
        "price": 400,
        "quantity": 2
    }}
    })
):
    _room_data = RoomAdd(hotel_id=hotel_id, **room_data.model_dump())
    room = await db.rooms.add(_room_data)
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
    _room_data = RoomAdd(hotel_id=hotel_id, **room_data.model_dump())
    await db.rooms.edit(
        _room_data,
        id=room_id,
        hotel_id=hotel_id
    )
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
    _room_data = RoomPatch(hotel_id=hotel_id, **room_data.model_dump(exclude_unset=True))
    await db.rooms.edit(
        _room_data,
        exclude_unset=True,
        id=room_id,
        hotel_id=hotel_id
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
    await db.rooms.delete(id=room_id, hotel_id=hotel_id)
    await db.commit()
    return {"status":"OK"}