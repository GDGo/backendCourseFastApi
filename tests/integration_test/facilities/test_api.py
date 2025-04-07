async def test_get_facilities(ac, db, jwt_token):
    response = await ac.get(
        "/facilities",
        headers={"Authorization": jwt_token},
    )
    assert response.status_code == 200


async def test_add_facilities(ac, db, jwt_token):
    response = await ac.post(
        "/facilities",
        headers={"Authorization": jwt_token},
        json={
            "title": "Балкон"
        }
    )
    assert response.status_code == 200