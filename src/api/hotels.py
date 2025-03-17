from fastapi import Query, APIRouter, Body
from src.database import async_session_maker
from src.repositories.hotels import HotelsRepository
from src.schemas.hotels import Hotel, HotelPatch
from src.api.dependencies import PaginationDep


router = APIRouter(prefix="/hotels", tags=["Отели"])


#Параметры запроса
@router.get("")
async def get_hotels(
        pagination: PaginationDep,
        location: str | None = Query(None, description="Адрес"),
        title: str | None = Query(None, description="Название отеля")
):
    per_page = pagination.per_page or 5
    async with async_session_maker() as session:
        return await HotelsRepository(session).get_all(
            location=location,
            title=title,
            limit=pagination.per_page or 5,
            offset=per_page * (pagination.page - 1)
        )


#Параметр пути
@router.post("")
async def add_hotel(hotel_data: Hotel = Body(openapi_examples={
    "1": {"summary": "Сочи", "value": {
        "title": "Адмирал 3",
        "location": "Сочи, ул. Нижнеимеретинская, 139А"
    }},
    "2": {"summary": "Дубай", "value": {
        "title": "Отель у фонтана",
        "location": "Дубай, ул. Шейха, 1"
    }},
    "3": {"summary": "Адлер-Коралл", "value": {
        "title": "Коралл",
        "location": "Адлер, улица Ленина, 219"
    }},
    "4": {"summary": "Адлер-Дельфин", "value": {
        "title": "Дельфин",
        "location": "Адлер, улица Ленина, 219а к2"
    }},
    "5": {"summary": "Адлер-Нептун", "value": {
        "title": "Нептун",
        "location": "Адлер, ул. Ленина, 219 к4"
    }},
    "6": {"summary": "Джубга", "value": {
        "title": "Гостиночно-ресторанный комплекс Grand Paradise",
        "location": "п. Джубгское, мкр. Прибой, 3 «А»"
    }},
    })
):
    async with async_session_maker() as session:
        hotel = await HotelsRepository(session).add(hotel_data)
        await session.commit()
    return {"Status": "OK", "data": hotel}


@router.put("/{hotel_id}")
async def put_hotel(hotel_id : int, hotel_data: Hotel):
    async with async_session_maker() as session:
        await HotelsRepository(session).edit(hotel_data, id=hotel_id)
        await session.commit()
    return {"Status": "OK"}


@router.delete("/{hotel_id}")
async def delete_hotel(hotel_id: int):
    async with async_session_maker() as session:
        await HotelsRepository(session).delete(id=hotel_id)
        await session.commit()
    return {"status": "OK"}


@router.patch("/{hotel_id}")
async def patch_hotel(hotel_id : int, hotel_data: HotelPatch):
    async with async_session_maker() as session:
        await HotelsRepository(session).edit(hotel_data, exclude_unset=True, id=hotel_id)
        await session.commit()
    return {"Status": "OK"}