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
    ("Pushok@mail.ru", "myamya", 200)
])
async def test_register_user(username, password, status_code,
                             authenticated_ac, setup_database):
    response = await authenticated_ac.post(
        "/auth/register",
        json={
            "email":username,
            "password":password
        }
    )

    assert response.status_code == 200
    res = response.json()
    assert isinstance(res, dict)
    assert res["status"] == "OK"


@pytest.mark.parametrize("username, password, status_code", [
    ("Pushok@mail.ru", "myamya", 200),
])
async def test_login_user(username, password, status_code,
        authenticated_ac, setup_database):
    response = await authenticated_ac.post(
        "/auth/login",
        json={
            "email":username,
            "password":password
        }
    )

    assert response.status_code == 200
    token = response.json()["access_token"]
    assert isinstance(token, str)
    assert authenticated_ac.cookies["access_token"]

    me = await authenticated_ac.get(
        "/auth/me"
    )
    assert me.status_code == 200
    me_json = me.json()
    assert isinstance(me_json, dict)
    assert me_json["id"]

    payload = AuthService().token_decode(token)
    assert payload["user_id"] == me_json["id"]


async def test_logout(authenticated_ac, setup_database):
    response = await authenticated_ac.get(
        "/auth/logout"
    )
    assert response.status_code == 200
    me = await authenticated_ac.get(
        "/auth/me"
    )
    assert me.status_code == 401
    print(me.request.headers)
