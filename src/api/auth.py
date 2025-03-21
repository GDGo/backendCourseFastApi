from fastapi import APIRouter, HTTPException, Response

from src.api.dependencies import UserIdDep, DBDep
from src.database import async_session_maker
from src.schemas.users import UserRequestAdd, UserAdd
from src.services.auth import AuthService

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/login")
async def login_user(
        db: DBDep,
        data: UserRequestAdd,
        response: Response
):
    user = await db.users.get_user_with_hashed_password(email=data.email)
    if not user:
        raise HTTPException(status_code=401, detail="Пользователь с таким email не зарегистрирован")
    if not AuthService().verify_password(data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Пароль не верный")
    access_token = AuthService().create_access_token({"user_id": user.id})
    response.set_cookie("access_token", access_token)
    return {"access_token": access_token}


@router.get("/logout")
async def logout_user(
        db: DBDep,
        response: Response
):
    async with async_session_maker() as session:
        response.delete_cookie("access_token")
        return {"status": "OK"}



@router.post("/register")
async def register_user(
        user: UserIdDep,
        db: DBDep,
        data: UserRequestAdd
):
    hashed_password = AuthService().hash_password(data.password)
    new_user_data = UserAdd(email=data.email, hashed_password=hashed_password)
    await db.users.add(new_user_data)
    await db.commit()

    return {"status": "OK"}


@router.get("/me")
async def get_me(
        db: DBDep,
        user_id: UserIdDep
):
    user_data = await db.users.get_one_or_none(id=user_id)
    return user_data