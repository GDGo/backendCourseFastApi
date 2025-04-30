from contextlib import asynccontextmanager
from fastapi import FastAPI
import uvicorn
import logging
import sys
from pathlib import Path
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend

sys.path.append(str(Path(__file__).parent.parent))

logging.basicConfig(level=logging.INFO)

from src.init import redis_manager
from src.api.hotels import router as router_hotels
from src.api.auth import router as router_users
from src.api.rooms import router as router_rooms
from src.api.bookings import router as router_bookings
from src.api.facilities import router as router_facilities
from src.api.images import router as router_images


@asynccontextmanager
async def lifespan(app=FastAPI):
    await redis_manager.connect()
    FastAPICache.init(RedisBackend(redis_manager.client), prefix="fastapi-cache")
    yield
    await redis_manager.close()

description = """
booking-hotel API helps you do awesome stuf. 🚀

* Регистрации и аутентификации пользователей.
* Бронирование отелей и номеров.
* Изменение отелей и номеров
* Добавление удобств
* Получение всех бронирований
* Получение только собственных бронирований
* Загрузка изображений
"""

app = FastAPI(title="API для сервиса бронирования отелей и номеров",
              version="1.0.0",
              contact={
                  "name": "Dmitry Goncharov",
                  "email": "dimnagoncharov21@gmail.com",
              },
              description=description,
              lifespan=lifespan)

app.include_router(router_users)
app.include_router(router_hotels)
app.include_router(router_rooms)
app.include_router(router_facilities)
app.include_router(router_bookings)
app.include_router(router_images)


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", reload=True, port=8001)