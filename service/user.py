from model.user import User
from data import user as data


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