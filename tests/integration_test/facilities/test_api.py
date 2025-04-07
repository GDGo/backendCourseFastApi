async def test_get_facilities(ac, db, jwt_token):
    response = await ac.get(
        "/facilities",
        headers={"Authorization": jwt_token},
    )
    assert response.status_code == 200
    assert isinstance(response.json(), list)


async def test_add_facilities(ac, db, jwt_token):
    facility_title = "Балкон"
    response = await ac.post(
        "/facilities",
        headers={"Authorization": jwt_token},
        json={
            "title": facility_title
        }
    )
    assert response.status_code == 200
    res = response.json()
    assert isinstance(res, dict)
    assert res["data"]["title"] == facility_title
    assert "data" in res