import logging
from typing import List

from pydantic import BaseModel
from sqlalchemy import select, insert, delete, update
from sqlalchemy.exc import NoResultFound, IntegrityError, ProgrammingError
from asyncpg.exceptions import UniqueViolationError, ForeignKeyViolationError, PostgresSyntaxError

from src.Exceptions import ObjectNotFoundException, ObjectAlreadyExistException, ObjectNotDeleteException, \
    ObjectNotUpdateException
from src.repositories.mappers.base import DataMapper


class BaseRepository:
    model = None
    mapper: DataMapper = None

    def __init__(self, session):
        self.session = session

    async def get_filtered(self, *filter, **filter_by):
        query = (
            select(self.model)
            .filter(*filter)
            .filter_by(**filter_by)
        )
        result = await self.session.execute(query)
        return [self.mapper.map_to_domain_entity(model) for model in result.scalars().all()]

    async def get_all(self, *args, **kwargs):
        return await self.get_filtered()

    async def get_one_or_none(self, **filter_by):
        query = select(self.model).filter_by(**filter_by)
        result = await self.session.execute(query)
        model = result.scalars().one_or_none()
        if (model is None):
            return None
        return self.mapper.map_to_domain_entity(model)

    async def get_one(self, **filter_by):
        query = select(self.model).filter_by(**filter_by)
        result = await self.session.execute(query)
        try:
            model = result.scalar_one()
        except NoResultFound:
            raise ObjectNotFoundException
        return self.mapper.map_to_domain_entity(model)

    async def add(self, data: BaseModel, unique_value=True):
        try:
            if unique_value:
                obj = await self.get_one_or_none(**data.model_dump())
                if obj:
                    raise ObjectAlreadyExistException
            add_data_stmt = (insert(self.model).values(**data.model_dump()).returning(self.model))
            result = await self.session.execute(add_data_stmt)
            model = result.scalars().one()
            return self.mapper.map_to_domain_entity(model)
        except IntegrityError as ex:
            logging.error(f"Не удалось добавить данные в БД, тип ошибки: {type(ex.orig.__cause__)=}")
            if isinstance(ex.orig.__cause__, UniqueViolationError):
                raise ObjectAlreadyExistException from ex
            else:
                logging.error(f"Не знакомая ошибка: тип ошибки {type(ex.orig.__cause__)=}")
                raise ex

    async def add_bulk(self, data: List[BaseModel]):
        add_data_stmt = (
            insert(self.model).
            values([item.model_dump() for item in data])
        )
        await self.session.execute(add_data_stmt)

    async def edit(self,
                   data: BaseModel,
                   exclude_unset: bool = False,
                   **filter_by) -> None:
        try:
            update_stmt = (
                update(self.model)
                .filter_by(**filter_by)
                .values(**data.model_dump(exclude_unset=exclude_unset))
            )
            await self.session.execute(update_stmt)
        except ProgrammingError as ex:
            logging.error(f"Не удалось изменить данные в БД, тип ошибки: {type(ex.orig.__cause__)=}")
            if isinstance(ex.orig.__cause__, PostgresSyntaxError):
                raise ObjectNotUpdateException from ex
            else:
                logging.error(f"Не знакомая ошибка: тип ошибки {type(ex.orig.__cause__)=}")
                raise ex

    async def delete(self, **filter_by) -> None:
        try:
            delete_stmt = delete(self.model).filter_by(**filter_by)
            await self.session.execute(delete_stmt)
        except IntegrityError as ex:
            logging.error(f"Не удалось удалить данные из БД, тип ошибки: {type(ex.orig.__cause__)=}")
            if isinstance(ex.orig.__cause__, ForeignKeyViolationError):
                raise ObjectNotDeleteException from ex
            else:
                logging.error(f"Не знакомая ошибка: тип ошибки {type(ex.orig.__cause__)=}")
                raise ex