import json
from fastapi import APIRouter, Body
from fastapi_cache.decorator import cache

from src.api.dependencies import UserIdDep, DBDep
from src.schemas.facilities import FacilityAdd
from src.init import redis_manager


router = APIRouter(
    prefix="/facilities",
    tags=["Удобства"]
)


@router.get("")
@cache(expire=10)
async def get_facilities(
        user_id: UserIdDep,
        db: DBDep
):
    # facilities_from_cache = await redis_manager.get("facilities")
    # if not facilities_from_cache:
    #     print("Запрос в БД")
    #     facilities = await db.facilities.get_all()
    #     facilities_schemas: list[dict] = [f.model_dump() for f in facilities]
    #     facilities_json = json.dumps(facilities_schemas)
    #     await redis_manager.set("facilities", facilities_json, 10)
    #
    #     return facilities
    # else:
    #     facilities_dict = json.loads(facilities_from_cache)
    #     return facilities_dict
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