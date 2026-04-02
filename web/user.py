from fastapi import APIRouter, HTTPException, Depends
from model.user import User
from service import user as service
from errors import Missing, Duplicate
from data.user import init_user

ACCESS_TOKEN_EXPIRE_MINUTES = 30
router = APIRouter(prefix="/user")

#создание таблицы БД
init_user()


#получение всех пользователей
@router.get("/")
def get_all() -> list[User]:
    return service.get_all()

#получение одного пользователя
@router.get("/{name}")
def get_one(name) -> User:
    try:
        return service.get_one(name)
    except Missing as exc:
        raise HTTPException(status_code=404, detail=exc.msg)

#создание пользователя
@router.post("/", status_code=201)
def create(user: User) -> User:
    try:
        return service.create(user)
    except Duplicate as exc:
        raise HTTPException(status_code=409, detail=exc.msg)

#изменение данных пользователя
# @router.patch("/")
# def modify(name: str, user: User) -> User:
#     try:
#         return service.modify(name, user)
#     except Missing as exc:
#         raise HTTPException(status_code=404, detail=exc.msg)

#удалить пользователя (переместить в другую таблицу)
@router.delete("/{name}")
def delete(name: str) -> None:
    try:
        return service.delete(name)
    except Missing as exc:
        raise HTTPException(status_code=404, detail=exc.msg)