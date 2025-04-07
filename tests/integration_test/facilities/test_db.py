from src.schemas.facilities import FacilityAdd


async def test_add_facility(db):
    facility_data = FacilityAdd(
        title="Балкон"
    )
    facility_add = await db.facilities.add(facility_data)
    facility = await db.facilities.get_one_or_none(id=facility_add.id)

    assert facility
    assert facility.id == facility_add.id
    await db.commit()