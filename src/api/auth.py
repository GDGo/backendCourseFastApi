from fastapi import APIRouter

from passlib.context import CryptContext

from src.database import async_session_maker
from src.repositories.users import UsersRepository
from src.schemas.users import UserRequestAdd, UserAdd


router = APIRouter(prefix="/auth", tags=["Авторизация и аутентификация"])

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


@router.post("/register")
async def register_user(
        data: UserRequestAdd
):
    hashed_password = pwd_context.hash(data.password)
    new_user_data = UserAdd(email=data.email, hashed_password=hashed_password)
    async with async_session_maker() as session:
        # exist_user = await UsersRepository(session).get_one_or_none(email=data.email)
        # if exist_user:
        #     return {"status": "User already exists."}
        await UsersRepository(session).add(new_user_data)
        await session.commit()

    return {"status": "OK"}