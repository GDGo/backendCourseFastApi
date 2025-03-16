from src.models.hotels import HotelsOrm
from src.repositories.base import BaseRepository
from sqlalchemy import select


class HotelsRepository(BaseRepository):
    model = HotelsOrm

    async def get_all(
            self,
            location,
            title,
            limit,
            offset
    ):
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
        return result.scalars().all()