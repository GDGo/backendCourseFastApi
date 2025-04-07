from fastapi import APIRouter, Body
from fastapi_cache.decorator import cache

from src.api.dependencies import UserIdDep, DBDep
from src.schemas.facilities import FacilityAdd


router = APIRouter(
    prefix="/facilities",
    tags=["Удобства"]
)


@router.get("")
# @cache(expire=10)
async def get_facilities(
        user_id: UserIdDep,
        db: DBDep
):
    return await db.facilities.get_all()


@router.post("")
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
    facility = await db.facilities.add(facility_data)
    await db.commit()
    return {"status": "OK", "data": facility}