from typing import List

from src.models.hotels import HotelsOrm
from src.repositories.base import BaseRepository

from src.schemas.hotels import Hotel


class HotelsRepository(BaseRepository):
    model = HotelsOrm
    schema = Hotel

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