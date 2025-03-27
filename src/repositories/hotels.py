from datetime import date
from typing import List
from sqlalchemy import select

from src.database import engine
from src.models.hotels import HotelsOrm
from src.models.rooms import RoomsOrm
from src.repositories.base import BaseRepository
from src.repositories.utils import rooms_ids_for_booking
from src.repositories.mappers.mappers import HotelDataMapper

from src.schemas.hotels import Hotel


class HotelsRepository(BaseRepository):
    model = HotelsOrm
    mapper = HotelDataMapper

    async def get_all(
            self,
            location,
            title,
            limit,
            offset
    ) -> List[Hotel]:
        query = select(HotelsOrm)
        if location:
            query = query.filter(HotelsOrm.location.ilike(f"%{location.strip()}%"))
        if title:
            query = query.filter(HotelsOrm.title.ilike(f"%{title.strip()}%"))
        query = (
            query
            .limit(limit)
            .offset(offset)
        )
        result = await self.session.execute(query)
        return [self.schema.model_validate(model, from_attributes=True) for model in result.scalars().all()]

    async def get_filtered_by_time(
            self,
            location,
            title,
            limit,
            offset,
            date_to: date,
            date_from: date,
    ) -> List[Hotel]:
        rooms_ids = rooms_ids_for_booking(date_to, date_from)

        hotels_ids = (
            select(RoomsOrm.hotel_id)
            .select_from(RoomsOrm)
            .filter(RoomsOrm.id.in_(rooms_ids)))

        query = (
            select(HotelsOrm)
            .select_from(HotelsOrm)
            .filter(HotelsOrm.id.in_(hotels_ids))
        )
        if location:
            query = (query.filter(HotelsOrm.location.ilike(f"%{location.strip()}%")))
        if title:
            query = (query.filter(HotelsOrm.title.ilike(f"%{title.strip()}%")))
        query = (
            query
            .limit(limit)
            .offset(offset)
        )

        result = await self.session.execute(query)
        # print(hotels_ids.compile(bind=engine, compile_kwargs={"literal_binds": True}))

        return [self.mapper.map_to_domain_entity(model) for model in result.scalars().all()]