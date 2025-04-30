from datetime import date

from fastapi import Query, APIRouter, Body, Path
from fastapi_cache.decorator import cache

from src.Exceptions import ObjectNotFoundException, HotelNotFoundHTTPException, ObjectNotDeleteException, \
    HotelNotDeleteHTTPException, HotelNotFoundException, ObjectNotUpdateException, HotelNotUpdateHTTPException, \
    ObjectNotCreatedException, HotelNotCreatedHTTPException, ObjectAlreadyExistException, HotelAlreadyExistHTTPException
from src.schemas.hotels import HotelAdd, HotelPatch
from src.api.dependencies import PaginationDep, UserIdDep, DBDep
from src.services.hotels import HotelService


router = APIRouter(
    prefix="/hotels",
    tags=["Отели"]
)


#Параметры запроса
@router.get("",
            name="Доступные отели",
            description="Все доступные отели в которых есть свободные номера на определенную дату")
@cache(expire=10)
async def get_hotels(
        user: UserIdDep,
        db: DBDep,
        pagination: PaginationDep,
        location: str | None = Query(None, description="Адрес"),
        title: str | None = Query(None, description="Название отеля"),
        date_from: date = Query(examples="2025-08-01"),
        date_to: date = Query(examples="2025-08-10"),
):
    hotels = await HotelService(db).get_filtered_by_time(
        pagination,
        location,
        title,
        date_from,
        date_to,
    )
    return {"status": "OK", "data": hotels}


@router.get("/{hotel_id}",
            name="Получить отель")
@cache(expire=10)
async def get_hotel(
        user: UserIdDep,
        db: DBDep,
        hotel_id: int = Path(description="ID отеля")
):
    try:
        hotel = await HotelService(db).get_hotel(hotel_id)
        return {"status": "OK", "data": hotel}
    except ObjectNotFoundException:
        raise HotelNotFoundHTTPException

#Параметр пути
@router.post("",
            name="Добавить отель")
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
    try:
        new_hotel = await HotelService(db).create_hotel(hotel_data)
        return {"Status": "OK", "data": new_hotel}
    except ObjectNotCreatedException:
        raise HotelNotCreatedHTTPException
    except ObjectAlreadyExistException:
        raise HotelAlreadyExistHTTPException


@router.put("/{hotel_id}",
            name="Полное изменение отеля")
async def put_hotel(
        user: UserIdDep,
        db: DBDep,
        hotel_id : int,
        hotel_data: HotelAdd
):
    try:
        await HotelService(db).edit_hotel(hotel_id, hotel_data)
    except HotelNotFoundException:
        raise HotelNotFoundHTTPException
    return {"Status": "OK"}


@router.patch("/{hotel_id}",
            name="Частичное изменение отеля")
async def patch_hotel(
        user: UserIdDep,
        db: DBDep,
        hotel_id : int,
        hotel_data: HotelPatch,
):
    try:
        await HotelService(db).partionally_edit(hotel_id, hotel_data)
    except HotelNotFoundException:
        raise HotelNotFoundHTTPException
    except ObjectNotUpdateException:
        raise HotelNotUpdateHTTPException
    return {"Status": "OK"}


@router.delete("/{hotel_id}",
            name="Удаление отеля")
async def delete_hotel(
        user: UserIdDep,
        db: DBDep,
        hotel_id: int
):
    try:
        await HotelService(db).delete_hotel(hotel_id)
    except ObjectNotDeleteException as ex:
        raise HotelNotDeleteHTTPException
    except HotelNotFoundException:
        raise HotelNotFoundHTTPException
    return {"status": "OK"}