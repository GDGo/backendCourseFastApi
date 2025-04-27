from fastapi import Body

from src.schemas.facilities import FacilityAdd
from src.services.base import BaseService


class FacilitiesService(BaseService):
    async def get_facilities(self):
        return await self.db.facilities.get_all()

    async def add_facilities(self, facility_data: FacilityAdd = Body(openapi_examples={
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
            })):
        facility = await self.db.facilities.add(facility_data)
        await self.db.commit()
        return facility