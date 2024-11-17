from fastapi import FastAPI, Query, Body, APIRouter
import uvicorn
from pydantic import BaseModel

router = APIRouter(prefix="/hotels", tags=["Отели"])


hotels = [
    {"id": 1, "title": "Sochi", "name": "Sochi"},
    {"id": 2, "title": "Дубай", "name": "Dubai"}
]


class Hotel(BaseModel):
    title: str
    name: str


#Параметры запроса
@router.get("")
def get_hotels(
        id: int | None = Query(None, description="Айдишник"),
        title: str | None = Query(None, description="Название отеля")
):
    hotels_ = []
    for hotel in hotels:
        if id and hotel["id"] != id:
            continue
        if title and hotel["title"] != title:
            continue
        hotels_.append(hotel)
    return hotels_


#Параметр пути
@router.delete("/{hotel_id}")
def delete_hotel(hotel_id: int):
    global hotels
    hotels = [hotel for hotel in hotels if hotel["id"] != hotel_id]
    return {"status": "OK"}


@router.post("")
def add_hotel(hotel_data: Hotel):
    global hotels
    hotels.append(
        {"id": hotels[-1]["id"] + 1,
         "title": hotel_data.title,
         "name": hotel_data.name}
    )
    return {"Status": "OK"}


@router.put("/{hotel_id}")
def put_hotel(hotel_id : int, hotels_data: Hotel):
    global hotels
    for hotel in hotels:
        if hotel["id"] == hotel_id:
            hotel["title"] = hotels_data.title
            hotel["name"] = hotels_data.name
    return {"Status": "OK"}


@router.patch("/{hotel_id}")
def patch_hotel(
        hotel_id : int,
        title: str | None = Body(None, embed=True),
        name: str | None = Body(None, embed=True)
):
    global hotels
    for hotel in hotels:
        if name:
            hotel["title"] = title
        if title:
            hotel["name"] = name
    return {"Status": "OK"}