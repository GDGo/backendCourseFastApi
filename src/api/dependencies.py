from typing import Annotated

from fastapi import Query, Depends
from pydantic import BaseModel


class PaginationParams(BaseModel):
    page: Annotated[int | None, Query(1, description="Страница", ge=1)]
    per_page: Annotated[int | None, Query(None, description="Количество отелей", ge=1, le=30)]


PaginationDep = Annotated[PaginationParams, Depends()]