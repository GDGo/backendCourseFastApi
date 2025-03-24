from fastapi import Query, APIRouter, Body, Path

from src.schemas.hotels import HotelAdd, HotelPatch
from src.api.dependencies import PaginationDep, UserIdDep, DBDep


router = APIRouter(
    prefix="/hotels",
    tags=["Отели"],
)


#Параметры запроса
@router.get("")
async def get_hotels(
        user: UserIdDep,
        db: DBDep,
        pagination: PaginationDep,
        location: str | None = Query(None, description="Адрес"),
        title: str | None = Query(None, description="Название отеля"),
):
    per_page = pagination.per_page or 5
    return await db.hotels.get_all(
        location=location,
        title=title,
        limit=pagination.per_page or 5,
        offset=per_page * (pagination.page - 1)
    )


@router.get("/{hotel_id}")
async def get_hotel(
        user: UserIdDep,
        db: DBDep,
        hotel_id: int = Path(description="ID отеля")
):
    return await db.hotels.get_one_or_none(id=hotel_id)


#Параметр пути
@router.post("")
async def add_hotel(
        user: UserIdDep,
        db: DBDep,
        hotel_data: HotelAdd = Body(openapi_examples={
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
    hotel = await db.hotels.add(hotel_data)
    await db.commit()
    return {"Status": "OK", "data": hotel}


@router.put("/{hotel_id}")
async def put_hotel(
        user: UserIdDep,
        db: DBDep,
        hotel_id : int,
        hotel_data: HotelAdd
):
    await db.hotels.edit(hotel_data, id=hotel_id)
    await db.commit()
    return {"Status": "OK"}


@router.delete("/{hotel_id}")
async def delete_hotel(
        user: UserIdDep,
        db: DBDep,
        hotel_id: int
):
    await db.hotels.delete(id=hotel_id)
    await db.commit()
    return {"status": "OK"}


@router.patch("/{hotel_id}")
async def patch_hotel(
        user: UserIdDep,
        db: DBDep,
        hotel_id : int,
        hotel_data: HotelPatch,
):
    await db.hotels.edit(hotel_data, exclude_unset=True, id=hotel_id)
    await db.commit()
    return {"Status": "OK"}