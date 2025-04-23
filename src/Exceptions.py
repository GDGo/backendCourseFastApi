class BaseException(Exception):
    detail = "Неожиданная ошибка"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class ObjectNotFoundException(BaseException):
    detail = "Объект не найден"


class AllRoomsAreBookedException(BaseException):
    detail = "Не осталось свободных номеров"


class RegisterUserAlreadyExistException(BaseException):
    detail = "Пользователь с таким email уже существует"


class InvalidDatesException(BaseException):
    detail = "Дата заезда позже даты выезда"