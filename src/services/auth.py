from datetime import datetime, timezone, timedelta

import jwt
from fastapi import Response
from passlib.context import CryptContext
from fastapi import HTTPException

from src.Exceptions import UserNotExistException, WrongPasswordException, ObjectAlreadyExistException, \
    UserAlreadyExistException
from src.config import settings
from src.database import async_session_maker
from src.schemas.users import UserRequestAdd, UserAdd
from src.services.base import BaseService


class AuthService(BaseService):
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    async def login_user(
            self,
            data: UserRequestAdd,
            response: Response
    ):
        user = await self.db.users.get_user_with_hashed_password(email=data.email)
        if not user:
            raise UserNotExistException
        if not AuthService().verify_password(data.password, user.hashed_password):
            raise WrongPasswordException
        access_token = AuthService().create_access_token({"user_id": user.id})
        response.set_cookie("access_token", access_token)
        return access_token

    async def logout_user(
            self,
            response: Response
    ):
        async with async_session_maker() as session:
            response.delete_cookie("access_token")

    async def register_user(
            self,
            data: UserRequestAdd
    ):
        hashed_password = AuthService().hash_password(data.password)
        new_user_data = UserAdd(email=data.email, hashed_password=hashed_password)
        try:
            await self.db.users.add(new_user_data)
            await self.db.commit()
        except ObjectAlreadyExistException as ex:
            raise UserAlreadyExistException

    async def get_me(
            self,
            user_id: int
    ):
        user_data = await self.db.users.get_one_or_none(id=user_id)
        return user_data

    def create_access_token(self, data: dict) -> str:
        to_encode = data.copy()
        expire = datetime.now(timezone.utc) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)
        return encoded_jwt

    def hash_password(self, password: str):
        return self.pwd_context.hash(password)

    def verify_password(self, plain_password, hashed_password):
        return self.pwd_context.verify(plain_password, hashed_password)

    def token_decode(self, token: str) -> dict:
        try:
            return jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])
        except jwt.exceptions.DecodeError:
            raise HTTPException(status_code=401, detail="Не верный токен")
        except jwt.exceptions.ExpiredSignatureError:
            raise HTTPException(status_code=401, detail="Время действия токена закончилось")