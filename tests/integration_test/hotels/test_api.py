async def test_get_hotels(authenticated_ac, db):
    response = await authenticated_ac.get(
        "/hotels",
        params={
            "date_from": "2024-08-19",
            "date_to": "2024-08-27"}
    )

    assert response.status_code == 200