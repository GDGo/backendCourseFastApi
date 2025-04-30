from fastapi import APIRouter, Response, Request

from src.Exceptions import UserNotExistException, UserNotExistHTTPException, \
    WrongPasswordException, WrongPasswordHTTPException, UserAlreadyExistHTTPException, UserAlreadyExistException, \
    UserAlreadyAuthorizeException, \
    UserAlreadyAuthorizeHTTPException, UserAlreadyLogoutException, UserAlreadyLogoutHTTPException, \
    PasswordNotEmptyException, PasswordNotEmptyHTTPException, PasswordNotEnogthLengthHTTPException, \
    PasswordNotEnogthLengthException
from src.api.dependencies import UserIdDep, DBDep
from src.database import async_session_maker
from src.schemas.users import UserRequestAdd
from src.services.auth import AuthService

router = APIRouter(prefix="/auth", tags=["Аутентификация"])


@router.post("/login",name="Вход")
async def login_user(
        db: DBDep,
        data: UserRequestAdd,
        response: Response,
        request: Request
):
    try:
        access_token = await AuthService(db).login_user(data=data, response=response, request=request)
    except UserNotExistException:
        raise UserNotExistHTTPException
    except WrongPasswordException:
        raise WrongPasswordHTTPException
    except UserAlreadyExistException:
        raise UserAlreadyExistHTTPException
    except UserAlreadyAuthorizeException:
        raise UserAlreadyAuthorizeHTTPException
    except PasswordNotEmptyException:
        raise PasswordNotEmptyHTTPException
    return {"access_token": access_token}


@router.get("/logout", name="Выход")
async def logout_user(
        db: DBDep,
        response: Response,
        request: Request
):
    try:
        await AuthService(db).logout_user(response=response, request=request)
        return {"status": "OK"}
    except UserAlreadyLogoutException:
        raise UserAlreadyLogoutHTTPException


@router.post("/register", name="Регистрация")
async def register_user(
        db: DBDep,
        data: UserRequestAdd
):
    try:
        await AuthService(db).register_user(data=data)
    except UserAlreadyExistException:
        raise UserAlreadyExistHTTPException
    except PasswordNotEmptyException:
        raise PasswordNotEmptyHTTPException
    except PasswordNotEnogthLengthException:
        raise PasswordNotEnogthLengthHTTPException
    return {"status": "OK"}


@router.get("/me",
            name="Кто я?",
            description="Информация под какой УЗ пользователь прошел аутентификацию")
async def get_me(
        db: DBDep,
        user_id: UserIdDep
):
    return await AuthService(db).get_me(user_id=user_id)