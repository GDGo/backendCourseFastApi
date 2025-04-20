import pytest

from tests.conftest import get_db_null_pool


@pytest.mark.parametrize("room_id, date_from, date_to, status_code", [
    (1, "2024-08-01", "2024-08-10", 200),
    (1, "2024-08-02", "2024-08-11", 200),
    (1, "2024-08-03", "2024-08-12", 200),
    (1, "2024-08-04", "2024-08-13", 200),
    (1, "2024-08-05", "2024-08-14", 200),
    (1, "2024-08-06", "2024-08-15", 404),
    (1, "2024-08-17", "2024-08-25", 200),
])
async def test_add_booking(
        room_id, date_from, date_to, status_code,
        db, authenticated_ac):
    # room_id = (await db.rooms.get_all())[0].id
    response = await authenticated_ac.post(
        "/bookings",
        json={
            "room_id": room_id,
            "date_from": date_from,
            "date_to": date_to
        }
    )
    if status_code == 200:
        res = response.json()
        assert isinstance(res, dict)
        assert res["status"] == "OK"
        assert "data" in res


@pytest.mark.parametrize("room_id, date_from, date_to, count", [
    (1, "2024-08-01", "2024-08-10", 1),
    (1, "2024-08-02", "2024-08-11", 2),
    (1, "2024-08-03", "2024-08-12", 3),
])
async def test_add_and_get_bookings(
        room_id, date_from, date_to, count,
        db, authenticated_ac, delete_all_bookings):
    await authenticated_ac.post(
        "/bookings",
        json={
            "room_id": room_id,
            "date_from": date_from,
            "date_to": date_to
        }
    )
    bookings = await authenticated_ac.get("/bookings/me")
    assert bookings.status_code == 200
    all_bookings = bookings.json()
    assert isinstance(all_bookings, list)
    assert len(all_bookings) == count


@pytest.fixture(scope="module")
async def delete_all_bookings():
    async for _db in get_db_null_pool():
        await _db.bookings.delete()
        await _db.commit()