import time
from datetime import date
from enum import nonmember

from src.schemas.bookings import BookingAdd


async def test_booking_crud(db):
    user_id = (await db.users.get_all())[0].id
    room_id = (await db.rooms.get_all())[0].id
    booking_data = BookingAdd(
        user_id=user_id,
        room_id=room_id,
        date_from=date(year=2025, month=8, day=19),
        date_to=date(year=2025, month=8, day=27),
        price=100
    )
    await db.bookings.add(booking_data)

    booking = await db.bookings.get_one_or_none(
        user_id=user_id,
        room_id=room_id,
        date_from=date(year=2025, month=8, day=19),
        date_to=date(year=2025, month=8, day=27),
        price=100
    )

    assert booking

    booking_data_new = BookingAdd(
        user_id=user_id,
        room_id=2,
        date_from=date(year=2025, month=9, day=19),
        date_to=date(year=2025, month=10, day=27),
        price=200
    )

    await db.bookings.edit(
        booking_data_new,
        user_id=user_id,
        room_id=room_id,
        date_from=date(year=2025, month=8, day=19),
        date_to=date(year=2025, month=8, day=27),
        price=100
    )

    booking = await db.bookings.get_one_or_none(
        user_id=user_id,
        room_id=2,
        date_from=date(year=2025, month=9, day=19),
        date_to=date(year=2025, month=10, day=27),
        price=200
    )

    assert booking

    await db.bookings.delete(
        user_id=user_id,
        room_id=2,
        date_from=date(year=2025, month=9, day=19),
        date_to=date(year=2025, month=10, day=27),
        price=200
    )

    booking = await db.bookings.get_one_or_none(
        user_id=user_id,
        room_id=2,
        date_from=date(year=2025, month=9, day=19),
        date_to=date(year=2025, month=10, day=27),
        price=200
    )

    assert booking is None