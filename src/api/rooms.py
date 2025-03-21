from fastapi import APIRouter, Body

from src.api.dependencies import UserIdDep
from src.database import async_session_maker
from src.repositories.rooms import RoomsRepository
from src.schemas.rooms import RoomAdd, RoomPatch, RoomPut

router = APIRouter(
    prefix="/hotels",
    tags=["Номера"]
)


@router.get("/{hotel_id}/rooms")
async def get_rooms(
        user: UserIdDep,
        hotel_id: int
):
    async with async_session_maker() as session:
        return await RoomsRepository(session).get_all(hotel_id=hotel_id)


@router.post("/{hotel_id}/rooms")
async def add_rooms(
        user: UserIdDep,
        room_data: RoomAdd = Body(openapi_examples={
    "1": {"summary": "Отель 111 Номер Эконом", "value": {
        "hotel_id": "111",
        "title": "Эконом",
        "description": "Эконом",
        "price": 100,
        "quantity": 10
    }},
    "2": {"summary": "Отель 111 Номер Комфорт", "value": {
        "hotel_id": "111",
        "title": "Комфорт",
        "description": "Комфорт",
        "price": 200,
        "quantity": 5
    }},
    "3": {"summary": "Отель 111 Номер Люкс", "value": {
        "hotel_id": "111",
        "title": "Люкс",
        "description": "Люкс",
        "price": 400,
        "quantity": 2
    }},
    "4": {"summary": "Отель 112 Номер Эконом", "value": {
        "hotel_id": "112",
        "title": "Эконом",
        "description": "Эконом",
        "price": 100,
        "quantity": 15
    }},
    "5": {"summary": "Отель 112 Номер Комфорт", "value": {
        "hotel_id": "112",
        "title": "Комфорт",
        "description": "Комфорт",
        "price": 200,
        "quantity": 15
    }},
    "6": {"summary": "Отель 112 Номер Люкс", "value": {
        "hotel_id": "112",
        "title": "Люкс",
        "description": "Люкс",
        "price": 400,
        "quantity": 12
    }},
    "7": {"summary": "Отель 113 Номер Эконом", "value": {
        "hotel_id": "113",
        "title": "Эконом",
        "description": "Эконом",
        "price": 100,
        "quantity": 25
    }},
    "8": {"summary": "Отель 113 Номер Комфорт", "value": {
        "hotel_id": "113",
        "title": "Комфорт",
        "description": "Комфорт",
        "price": 200,
        "quantity": 35
    }},
    "9": {"summary": "Отель 113 Номер Люкс", "value": {
        "hotel_id": "113",
        "title": "Люкс",
        "description": "Люкс",
        "price": 400,
        "quantity": 15
    }}
    })
):
    async with async_session_maker() as session:
        room = await RoomsRepository(session).add(room_data)
        await session.commit()
    return {"status": "OK", "data": room}


@router.put("/{hotel_id}/rooms/{room_id}")
async def put_room(
        user: UserIdDep,
        hotel_id: int,
        room_id: int,
        room_data: RoomPut
):
    async with async_session_maker() as session:
        await RoomsRepository(session).edit(
            room_data,
            id=room_id,
            hotel_id=hotel_id
        )
        await session.commit()
    return {"status": "OK"}


@router.delete("/{hotel_id}/rooms/{room_id}")
async def delete_room(
        user: UserIdDep,
        hotel_id: int,
        room_id: int
):
    async with async_session_maker() as session:
        await RoomsRepository(session).delete(id=room_id, hotel_id=hotel_id)
        await session.commit()
    return {"status":"OK"}


@router.patch("/{hotel_id}/rooms/{room_id}")
async def patch_room(
        user: UserIdDep,
        hotel_id: int,
        room_id: int,
        room_data: RoomPatch
):
    async with async_session_maker() as session:
        await RoomsRepository(session).edit(
            room_data,
            exclude_unset=True,
            id=room_id,
            hotel_id=hotel_id
        )
        await session.commit()
    return {"status": "OK"}










