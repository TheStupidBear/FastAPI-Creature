from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from core.security import verify_password
from core.settings import SECRET_KEY, ALGORITHM
from typing import Annotated
import jwt
from jwt.exceptions import InvalidTokenError
from model.user import User,TokenData
from data import user as data

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/user/login")

fake_users_db = {
    "johndoe": {
        "username": "johndoe",
        "hashed_password": "$argon2id$v=19$m=65536,t=3,p=4$wagCPXjifgvUFBzq4hqe3w$CYaIb8sB+wtD+Vu/P4uod1+Qof8h+1g7bbDlBID48Rc",
        "is_superuser": 0,
    }}

#Ищет пользователя по имени
def get_user(db, username: str):
    if username in db:
        user_dict = db[username]
        return User(**user_dict)

#Аутентифицирует пользователя: проверяет, что такой есть и пароль верный
def authenticate_user(username: str, password: str):
    user = get_user(fake_users_db, username)
    if not user:
        return None
    if not verify_password(password, user.hashed_password):
        return None
    return user


#Извлекает текущего пользователя из JWT токена. Это сердце нашей авторизации!
async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        print("payload", payload)
        username = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except InvalidTokenError:
        raise credentials_exception
    user = get_user(fake_users_db, username=token_data.username)
    if user is None:
        raise credentials_exception
    return user


#Проверяет, что пользователь не заблокирован (все пользователи активны)
async def get_current_active_user(
    current_user: Annotated[User, Depends(get_current_user)],):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user




def get_all() -> list[User]:
    return data.get_all()

def get_one(name) -> User:
    return data.get_one(name)

def check_user(name: str) -> bool:
    return data.check_user(name)

def login_user(name: str, password: str) -> bool:
    return data.login_user(name, password)

def create(user: User) -> None:
    return data.create(user)

def modify(name: str, user: User) -> User:
    return data.modify(name, user)

def delete(name: str) -> None:
    return data.delete(name)