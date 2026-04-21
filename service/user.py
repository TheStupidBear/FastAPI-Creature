from model.user import User
from data import user as data

def login_user(credentials) -> bool:
    if data.check_user(credentials.username): #если есть такой пользователь в БД
        if data.login_user(credentials.username, credentials.password): #если username и пароль совпадают
            return True
        else:
            return False
    return False


def get_all() -> list[User]:
    return data.get_all()

def get_one(name) -> User:
    return data.get_one(name)

def check_user(name: str) -> bool:
    return data.check_user(name)

def create(user: User) -> None:
    return data.create(user)

def modify(name: str, user: User) -> User:
    return data.modify(name, user)

def delete(name: str) -> None:
    return data.delete(name)