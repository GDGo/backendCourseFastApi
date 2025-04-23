class BaseException(Exception):
    detail = "Неожиданная ошибка"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class ObjectNotFoundException(BaseException):
    detail = "Объект не найден"


class AllRoomsAreBookedException(BaseException):
    detail = "Не осталось свободных номеров"