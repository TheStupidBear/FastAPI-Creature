from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from typing import Annotated
from model.user import User
from data import user as data

fake_users_db = {
    "johndoe": {
        "username": "johndoe",
        "hashed_password": "fakehashedsecret",
    },
    "alice": {
        "username": "alice",
        "hashed_password": "fakehashedsecret2",
    },
}

#создание схемы oauth2
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/user/token")

def fake_hash_password(password: str):
    return "fakehashed" + password

def get_user(db, username: str):
    if username in db:
        user_dict = db[username]
        return User(**user_dict)

def fake_decode_token(token):
    # This doesn't provide any security at all
    # Check the next version
    user = get_user(fake_users_db, token)
    return user

async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    print(token)
    user = fake_decode_token(token)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user


# def login_user(credentials) -> bool:
#     if data.check_user(credentials.username): #если есть такой пользователь в БД
#         if data.login_user(credentials.username, credentials.password): #если username и пароль совпадают
#             return True
#         else:
#             return False
#     return False
#
# def check_user(username: str) -> bool:
#     return data.check_user(username)
#
# def create(user: User) -> None:
#     return data.create(user)

# def get_all() -> list[User]:
#     return data.get_all()
#
# def get_one(name) -> User:
#     return data.get_one(name)
#
# def modify(name: str, user: User) -> User:
#     return data.modify(name, user)
#
# def delete(name: str) -> None:
#     return data.delete(name)