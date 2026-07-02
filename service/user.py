from fastapi import HTTPException, status
from model.user import User, Token
from data import user as data
from datetime import timedelta, datetime, timezone
import jwt
from jwt.exceptions import InvalidTokenError

SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"

def create_access_token(data:dict, expires_delta: timedelta) -> str:
    to_encode = data.copy()  # копируем данные для кодирования
    expire = datetime.now(timezone.utc) + expires_delta
    to_encode.update({"exp": expire})  # к текущему времени прибавляем время жизни
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def login_for_access_token(username:str, password:str) -> Token:
    # если есть такой пользователь в БД
    if data.login_user(username, password):
        access_token_expires = timedelta(minutes=30)  # время действия токена
        # данные для кодирования
        access_token = create_access_token(
            data={"username": username, "password": password},
            expires_delta=access_token_expires
        )
        # создание токена
        return Token(access_token=access_token, token_type="bearer",
                     access_token_expires=str(access_token_expires))
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )


def get_current_user(token: str):
    # заранее подготовим исключение
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        # декодировка токена
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        # данные из токена
        username: str = payload.get("username")
        password: str = payload.get("password")
        exp: str = payload.get("exp")

        # если в токене нет поля username
        if username is None:
            raise credentials_exception
        # если время жизни токена истекло
        if datetime.fromtimestamp(float(exp)) - datetime.now() < timedelta(0):
            raise credentials_exception

    except InvalidTokenError:
        raise credentials_exception

    if data.login_user(username, password):
        return User(username=username, password=password)
    else:
        raise credentials_exception