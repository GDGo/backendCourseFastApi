from fastapi import Query, APIRouter, Body

from sqlalchemy import insert, select

from src.database import async_session_maker, engine
from src.models.hotels import HotelsOrm
from src.schemas.hotels import Hotel, HotelPatch
from src.api.dependencies import PaginationDep


router = APIRouter(prefix="/hotels", tags=["Отели"])


#Параметры запроса
@router.get("")
async def get_hotels(
        pagination: PaginationDep,
        id: int | None = Query(None, description="Айдишник"),
        title: str | None = Query(None, description="Название отеля")
):
    async with async_session_maker() as session:
        query = select(HotelsOrm)
        result = await session.execute(query)
        hotels = result.scalars().all()
        return hotels

    # if pagination.page and pagination.per_page:
    #     return hotels_[pagination.per_page * (pagination.page - 1):][:pagination.per_page]


#Параметр пути
@router.delete("/{hotel_id}")
def delete_hotel(hotel_id: int):
    global hotels
    hotels = [hotel for hotel in hotels if hotel["id"] != hotel_id]
    return {"status": "OK"}


@router.post("")
async def add_hotel(hotel_data: Hotel = Body(openapi_examples={
    "1": {"summary": "Сочи", "value": {
        "title": "Отель Сочи 5 звезд у моря",
        "location": "ул. Моря, 1"
    }},
    "2": {"summary": "Дубай", "value": {
        "title": "Отель Дубай у фонтана",
        "location": "ул. Шейха, 1"
    }},
})
):
    async with async_session_maker() as session:
        add_hotel_stmt = insert(HotelsOrm).values(**hotel_data.model_dump())
        print(add_hotel_stmt.compile(engine, compile_kwargs={"literal_binds": True}))
        await session.execute(add_hotel_stmt)
        await session.commit()

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