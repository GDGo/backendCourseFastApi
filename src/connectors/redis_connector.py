import redis.asyncio as redis
from typing import Optional, Any


class RedisManager:
    def __init__(self, host: str, port: int, db: int = 0):
        """
        Инициализация RedisManager.

        :param host: Хост Redis (по умолчанию 'localhost')
        :param port: Порт Redis (по умолчанию 6379)
        :param db: Номер базы данных (по умолчанию 0)
        """
        self.host = host
        self.port = port
        self.db = db
        self.client: Optional[redis.Redis] = None

    async def connect(self) -> None:
        """Асинхронное подключение к Redis."""
        self.client = redis.Redis(host=self.host, port=self.port, db=self.db)
        try:
            await self.client.ping()  # Проверяем подключение
            print("Успешное подключение к Redis")
        except Exception as e:
            print(f"Ошибка подключения к Redis: {e}")
            raise

    async def set(self, key: str, value: Any, expire: Optional[int] = None) -> bool:
        """
        Установка значения по ключу.

        :param key: Ключ
        :param value: Значение (будет автоматически сериализовано в строку)
        :param expire: Время жизни ключа в секундах (опционально)
        :return: True, если успешно
        """
        if not self.client:
            raise ConnectionError("Redis не подключен. Вызовите connect() сначала.")

        try:
            await self.client.set(key, str(value), ex=expire)
            return True
        except Exception as e:
            print(f"Ошибка при установке значения: {e}")
            return False

    async def get(self, key: str) -> Optional[str]:
        """
        Получение значения по ключу.

        :param key: Ключ
        :return: Значение или None, если ключ не существует
        """
        if not self.client:
            raise ConnectionError("Redis не подключен. Вызовите connect() сначала.")

        try:
            value = await self.client.get(key)
            return value.decode() if value else None
        except Exception as e:
            print(f"Ошибка при получении значения: {e}")
            return None

    async def delete(self, key: str) -> bool:
        """
        Удаление ключа.

        :param key: Ключ
        :return: True, если ключ удален, False если не существует
        """
        if not self.client:
            raise ConnectionError("Redis не подключен. Вызовите connect() сначала.")

        try:
            deleted = await self.client.delete(key)
            return deleted > 0
        except Exception as e:
            print(f"Ошибка при удалении ключа: {e}")
            return False

    async def close(self) -> None:
        """Закрытие соединения с Redis."""
        if self.client:
            await self.client.close()
            self.client = None
            print("Соединение с Redis закрыто")