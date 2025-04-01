from src.services.auth import AuthService


async def test_get_hotels(ac, db):
    user_id = (await db.users.get_all())[0].id
    jwt_token = AuthService().create_access_token({"user_id": user_id})
    response = await ac.get(
        "/hotels",
        headers={"Authorization": jwt_token},
        params={
            "date_from": "2024-08-19",
            "date_to": "2024-08-27"}
    )

    assert response.status_code == 200