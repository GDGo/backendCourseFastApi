from datetime import date

from fastapi import HTTPException


class BaseException(Exception):
    detail = "Неожиданная ошибка"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

class ObjectNotFoundException(BaseException):
    detail = "Объект не найден"

class RoomNotFoundException(ObjectNotFoundException):
    detail = "Номер не найден"

class HotelNotFoundException(ObjectNotFoundException):
    detail = "Отель не найден"

class AllRoomsAreBookedException(BaseException):
    detail = "Не осталось свободных номеров"

class ObjectAlreadyExistException(BaseException):
    detail = "Похожий объект уже существует"

class ObjectNotDelete(BaseException):
    detail = "Объект не может быть удален"

def check_dates(date_from: date, date_to: date):
    if date_to <= date_from:
        raise HTTPException(422, detail="Дата заезда позже даты выезда")

class BaseHTTPException(HTTPException):
    status_code = 500
    detail = None

    def __init__(self):
        super().__init__(status_code=self.status_code, detail=self.detail)


class HotelNotFoundHTTPException(BaseHTTPException):
    status_code = 404
    detail = "Отель не найден"

class RoomNotFoundHTTPException(BaseHTTPException):
    status_code = 404
    detail = "Номер не найден"

class HotelNotDeleteHTTPException(BaseHTTPException):
    status_code = 409
    detail = "Отель не может быть удален"