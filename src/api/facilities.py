from fastapi import APIRouter, Body
from fastapi_cache.decorator import cache

from src.Exceptions import FacilityAlreadyExistHTTPException, ObjectAlreadyExistException
from src.api.dependencies import UserIdDep, DBDep
from src.schemas.facilities import FacilityAdd
from src.services.facilities import FacilitiesService


router = APIRouter(
    prefix="/facilities",
    tags=["Удобства"]
)


@router.get("", name="Доступные удобства")
@cache(expire=10)
async def get_facilities(
        user_id: UserIdDep,
        db: DBDep
):
    return await FacilitiesService(db).get_facilities()


@router.post("", name="Добавить удобства")
async def add_facilities(
        user_id: UserIdDep,
        db: DBDep,
        facility_data: FacilityAdd = Body(openapi_examples={
    "1": {"summary": "Сплит-система", "value": {
        "title": "Сплит-система"
    }},
    "2": {"summary": "Холодильник в номере", "value": {
        "title": "Холодильник в номере"
    }},
    "3": {"summary": "Душ в номере", "value": {
        "title": "Душ"
    }},
    "4": {"summary": "Телевизор", "value": {
        "title": "Телевизор"
    }},
    }
)):
    try:
        facility = await FacilitiesService(db).add_facilities(facility_data=facility_data)
        return {"status": "OK", "data": facility}
    except ObjectAlreadyExistException:
        raise FacilityAlreadyExistHTTPException