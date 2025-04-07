import json

from unittest import mock

mock.patch("fastapi_cache.decorator.cache", lambda *args, **kwargs: lambda f: f).start()

import pytest
from httpx import AsyncClient, ASGITransport

from src.api.dependencies import get_db
from src.config import settings
from src.database import Base, engine_null_pool, async_session_maker_null_pool
from src.main import app
from src.models import *
from src.schemas.hotels import HotelAdd
from src.schemas.rooms import RoomAdd
from src.services.auth import AuthService
from src.utils.db_manager import DBManager


@pytest.fixture(scope="session", autouse=True)
async def check_test_mode():
    assert settings.MODE == "TEST"


async def get_db_null_pool() -> DBManager:
    async with DBManager(session_factory=async_session_maker_null_pool) as db:
        yield db


@pytest.fixture()
async def db() -> DBManager:
    async for db in get_db_null_pool():
        yield db


app.dependency_overrides[get_db] = get_db_null_pool


@pytest.fixture(scope="session", autouse=True)
async def setup_database(check_test_mode):
    async with engine_null_pool.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    with open(r"tests\mock_hotels.json", encoding="utf-8") as mock_hotels, \
            open(r"tests\mock_rooms.json", encoding="utf-8") as mock_rooms:
        hotels = json.load(mock_hotels)
        rooms = json.load(mock_rooms)

    hotels = [HotelAdd.model_validate(hotel) for hotel in hotels]
    rooms = [RoomAdd.model_validate(room) for room in rooms]

    async with DBManager(session_factory=async_session_maker_null_pool) as db_:
        await db_.hotels.add_bulk(hotels)
        await db_.rooms.add_bulk(rooms)
        await db_.commit()


@pytest.fixture(scope="session")
async def ac() -> AsyncClient:
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        yield ac


@pytest.fixture(scope="session", autouse=True)
async def register_user(ac, setup_database):
    await ac.post(
        "/auth/register",
        json={
            "email":"kot@pes.ru",
            "password":"1234"
        }
    )


@pytest.fixture(autouse=True)
async def jwt_token(db, register_user):
    user_id = (await db.users.get_all())[0].id
    token = AuthService().create_access_token({"user_id": user_id})

    assert token
    assert isinstance(token, str)

    return token


@pytest.fixture(scope="session", autouse=True)
async def authenticated_ac(ac, register_user):
    response = await ac.post(
        "/auth/login",
        json={
            "email": "kot@pes.ru",
            "password": "1234"
        }
    )
    assert response.status_code == 200
    token = response.json()["access_token"]
    assert isinstance(token, str)
    yield ac