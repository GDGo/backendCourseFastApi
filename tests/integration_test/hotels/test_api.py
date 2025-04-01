async def test_get_hotels(ac, db, jwt_token):
    response = await ac.get(
        "/hotels",
        headers={"Authorization": jwt_token},
        params={
            "date_from": "2024-08-19",
            "date_to": "2024-08-27"}
    )

    assert response.status_code == 200