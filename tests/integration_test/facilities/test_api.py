async def test_get_facilities(authenticated_ac, db):
    response = await authenticated_ac.get(
        "/facilities",
    )
    assert response.status_code == 200
    assert isinstance(response.json(), list)


async def test_add_facilities(authenticated_ac, db):
    facility_title = "Балкон"
    response = await authenticated_ac.post(
        "/facilities",
        json={
            "title": facility_title
        }
    )
    assert response.status_code == 200
    res = response.json()
    assert isinstance(res, dict)
    assert res["data"]["title"] == facility_title
    assert "data" in res