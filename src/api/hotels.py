from fastapi import Query, APIRouter, Body
from src.schemas.hotels import Hotel, HotelPatch
from src.api.dependencies import PaginationDep


router = APIRouter(prefix="/hotels", tags=["Отели"])


hotels = [
    {"id": 1, "title": "Sochi", "name": "Sochi"},
    {"id": 2, "title": "Дубай", "name": "Dubai"},
    {"id": 3, "title": "Мальдивы", "name": "maldivi"},
    {"id": 4, "title": "Геленджик", "name": "gelendzhik"},
    {"id": 5, "title": "Москва", "name": "moscow"},
    {"id": 6, "title": "Казань", "name": "kazan"},
    {"id": 7, "title": "Санкт-Петербург", "name": "spb"},
]


#Параметры запроса
@router.get("")
def get_hotels(
        pagination: PaginationDep,
        id: int | None = Query(None, description="Айдишник"),
        title: str | None = Query(None, description="Название отеля")
):
    global hotels
    hotels_ = []

    for hotel in hotels:
        if id and hotel["id"] != id:
            continue
        if title and hotel["title"] != title:
            continue
        hotels_.append(hotel)

    if pagination.page and pagination.per_page:
        return hotels_[pagination.per_page * (pagination.page - 1):][:pagination.per_page]
    return hotels_


#Параметр пути
@router.delete("/{hotel_id}")
def delete_hotel(hotel_id: int):
    global hotels
    hotels = [hotel for hotel in hotels if hotel["id"] != hotel_id]
    return {"status": "OK"}


@router.post("")
def add_hotel(hotel_data: Hotel = Body(openapi_examples={
    "1": {"summary": "Сочи", "value": {
        "title": "Отель Сочи 5 звезд у моря",
        "name": "sochi_u_morya"
    }},
    "2": {"summary": "Дубай", "value": {
        "title": "Отель Дубай у фонтана",
        "name": "dubai_u_fontan"
    }},
})
):
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
            break
    return {"Status": "OK"}


@router.patch("/{hotel_id}")
def patch_hotel(hotel_id : int, hotel_data: HotelPatch):
    global hotels
    hotel = [hotel for hotel in hotels if hotel["id"] == hotel_id][0]
    if hotel_data.name:
        hotel["title"] = hotel_data.title
    if hotel_data.title:
        hotel["name"] = hotel_data.name
    return {"Status": "OK"}