from typing import Annotated

from fastapi import Query, Depends, HTTPException, Request
from pydantic import BaseModel

from src.services.auth import AuthService


class PaginationParams(BaseModel):
    page: Annotated[int | None, Query(1, description="Страница", ge=1)]
    per_page: Annotated[int | None, Query(None, description="Количество отелей", ge=1, le=30)]


PaginationDep = Annotated[PaginationParams, Depends()]


def get_token(request: Request) -> str:
    token = request.cookies.get("access_token")
    if not token:
        token = request.headers.get("Authorization")
        if not token:
            raise HTTPException(status_code=401, detail="Токен отсутствует")
    return token


def get_current_user_id(token: str = Depends(get_token)) -> int:
    data = AuthService().token_decode(token)
    return data.get("user_id")


UserIdDep = Annotated[int, Depends(get_current_user_id)]