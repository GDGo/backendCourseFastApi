from src.services.auth import AuthService
import pytest


def test_decode_and_encode_access_token():
    data = {"user_id": 1}
    jwt_token = AuthService().create_access_token(data)

    assert jwt_token
    assert isinstance(jwt_token, str)

    payload = AuthService().token_decode(jwt_token)
    assert payload
    assert payload["user_id"] == data["user_id"]


@pytest.mark.parametrize("username, password, status_code", [
    ("Pushok@mail.ru", "myamya", 200),
    ("Pushok@mail.ru", "myamya", 409),
    ("Push0k@mail.ru", "myamya", 200),
    ("Pushok", "myamya", 422),
    ("Pushok@mail", "myamya", 422),
])
async def test_register_user(username, password, status_code,
                             ac, setup_database):
    # /register
    response = await ac.post(
        "/auth/register",
        json={
            "email":username,
            "password":password
        }
    )

    assert response.status_code == status_code
    if status_code != 200:
        return

    # /login
    resp_login = await ac.post(
        "/auth/login",
        json={
            "email":username,
            "password":password
        }
    )

    assert resp_login.status_code == 200
    assert ac.cookies["access_token"]
    token = ac.cookies["access_token"]
    assert isinstance(token, str)

    # /me
    me = await ac.get("/auth/me")
    assert me.status_code == 200
    me_json = me.json()
    assert isinstance(me_json, dict)
    assert "id" in me_json
    assert "password" not in me_json
    assert "hashed_password" not in me_json
    assert me_json["email"] == username

    payload = AuthService().token_decode(token)
    assert payload["user_id"] == me_json["id"]

    response = await ac.get("/auth/logout")
    assert response.status_code == 200
    assert "access_token" not in ac.cookies
