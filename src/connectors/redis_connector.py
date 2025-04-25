import logging

import redis.asyncio as redis
from typing import Optional, Any


class RedisManager:
    def __init__(self, host: str, port: int, db: int = 0):
        self.host = host
        self.port = port
        self.db = db
        self.client: Optional[redis.Redis] = None

    async def connect(self) -> None:
        logging.info(f"Подключение к Redis host={self.host}, port={self.port}")
        self.client = redis.Redis(host=self.host, port=self.port, db=self.db)
        logging.info(f"Подключено к Redis host={self.host}, port={str(self.port)}")

    async def set(self, key: str, value: Any, expire: int = None) -> bool:
        if not self.client:
            raise ConnectionError("Redis не подключен. Вызовите connect() сначала.")

        try:
            await self.client.set(key, str(value), ex=expire)
            return True
        except Exception as e:
            print(f"Ошибка при установке значения: {e}")
            return False

    async def get(self, key: str) -> Optional[str]:
        if not self.client:
            raise ConnectionError("Redis не подключен. Вызовите connect() сначала.")

        value = await self.client.get(key)
        return value.decode() if value else None

    async def delete(self, key: str) -> bool:
        if not self.client:
            raise ConnectionError("Redis не подключен. Вызовите connect() сначала.")

        deleted = await self.client.delete(key)
        return deleted > 0

    async def close(self) -> None:
        if self.client:
            await self.client.close()
            self.client = None