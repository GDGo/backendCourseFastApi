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

class ObjectNotCreatedException(BaseException):
    detail = "Объект не может быть создан"

class ObjectAlreadyExistException(BaseException):
    detail = "Похожий объект уже существует"

class ObjectNotDeleteException(BaseException):
    detail = "Объект не может быть удален"

class ObjectNotUpdateException(BaseException):
    detail = "Объект не может быть изменен"

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

class UserAlreadyAuthorizeException(BaseException):
    detail = "Пользователь уже авторизован, не надо часто жмякать....попробуй попозже."

class UserAlreadyLogoutException(BaseException):
    detail = "Ты уже вышел из системы. Узбогойся :)"

class PasswordNotEmptyException(BaseException):
    detail = "Пароль не может быть пустым"

class PasswordNotEnogthLengthException(BaseException):
    detail = "Минимальная длина пароля 8 символов"

class FacilityAddBulkException(BaseException):
    detail = "Не удалось добавить удобства при создании номера"

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

class RoomNotDeleteHTTPException(BaseHTTPException):
    status_code = 409
    detail = "Номер не может быть удален"

class HotelNotDeleteHTTPException(BaseHTTPException):
    status_code = 409
    detail = "Отель не может быть удален"

class UserAlreadyExistHTTPException(BaseHTTPException):
    status_code = 409
    detail = "Пользователь с таким email уже зарегистрирован"

class HotelAlreadyExistHTTPException(BaseHTTPException):
    status_code = 409
    detail = "Отель уже существует"

class RoomAlreadyExistHTTPException(BaseHTTPException):
    status_code = 409
    detail = "Номер с такими характеристиками уже существует"

class FacilityAlreadyExistHTTPException(BaseHTTPException):
    status_code = 409
    detail = "Удобство уже существует"

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

class AllRoomsAreBookedHTTPException(BaseHTTPException):
    status_code = 409
    detail = "Не осталось свободных номеров"

class UserAlreadyAuthorizeHTTPException(BaseHTTPException):
    status_code = 409
    detail = "Ты уже авторизован. Узбагойся :)"

class UserAlreadyLogoutHTTPException(BaseHTTPException):
    status_code = 409
    detail = "Ты уже вышел из системы. Узбогойся :)"

class PasswordNotEmptyHTTPException(BaseHTTPException):
    status_code = 422
    detail = "Пароль не может быть пустым"

class PasswordNotEnogthLengthHTTPException(BaseHTTPException):
    status_code = 422
    detail = "Минимальная длина пароля 8 символов"

class HotelNotUpdateHTTPException(BaseHTTPException):
    status_code = 409
    detail = "Отель не может быть изменен, проверьте передаваемые значения"

class HotelNotCreatedHTTPException(BaseHTTPException):
    status_code = 409
    detail = "Отель не может быть создан без названия и его расположения"

class FileNotFoundErrorHTTPException(BaseHTTPException):
    status_code = 404
    detail = "Файл не найден"

class FacilityAddBulkHTTPException(BaseHTTPException):
    status_code = 409
    detail = "Не удалось добавить удобства при создании номера, проверьте id добавляемых удобств"