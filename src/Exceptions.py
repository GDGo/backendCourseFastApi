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

class ObjectNotDeleteException(BaseException):
    detail = "Объект не может быть удален"

class UserAlreadyExistException(BaseException):
    detail = "Пользователь с таким email уже зарегистрирован"

class UserNotExistException(BaseException):
    detail = "Пользователь с таким email не зарегистрирован"

class WrongPasswordException(BaseException):
    detail = "Пароль не верный"

class WrongTokenException(BaseException):
    detail = "Не верный токен"

class TokenExpiredException(BaseException):
    detail = "Время действия токена закончилось"

class TokenNotSetRequestException(BaseException):
    detail = "Требуется авторизация"

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

class UserAlreadyExistHTTPException(BaseHTTPException):
    status_code = 409
    detail = "Пользователь с таким email уже зарегистрирован"

class UserNotExistHTTPException(BaseHTTPException):
    status_code = 404
    detail = "Пользователь с таким email не зарегистрирован"

class WrongPasswordHTTPException(BaseHTTPException):
    status_code = 409
    detail = "Пароль не верный"

class WrongTokenHTTPException(BaseHTTPException):
    status_code = 401
    detail = "Не верный токен"

class TokenExpiredHTTPException(BaseHTTPException):
    status_code = 401
    detail = "Время действия токена закончилось"

class TokenNotSetRequestHTTPException(BaseHTTPException):
    status_code = 401
    detail = "Требуется авторизация"