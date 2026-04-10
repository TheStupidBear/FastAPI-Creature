from fastapi import APIRouter, HTTPException, Request, Form, status
from pathlib import Path
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse, JSONResponse
from fastapi.exceptions import RequestValidationError
from model.user import User
from service import user as service
from errors import Missing, Duplicate
from data.user import init_user


router = APIRouter(prefix="/user")

parent_dir = Path(__file__).resolve().parent.parent
template_obj = Jinja2Templates(directory=f"{parent_dir}/template")

#создание таблицы БД
init_user()

#страница регистрации
@router.get("/registration")
async def reg(request: Request):
    return template_obj.TemplateResponse("registration.html",
                                         {"request": request})



#post запрос регистрации
@router.post("/registration")
async def reg(name: str = Form(...), password: str = Form(...), repeat_password: str = Form(...)):
    if password != repeat_password:
        return f"Пароли не совпадают"
    else:
        if service.check_user(name) == True: #если есть в БД такой пользователь
            return f"Такой пользователь уже есть"
        else:
            service.create(name, password)
            return f"Записали в БД"


#страница входа
@router.get("/login")
async def login(request: Request):
    return template_obj.TemplateResponse("login.html",
                                         {"request": request})

#создание пользователя
# @router.post("/", status_code=201)
# def create(user: User) -> User:
#     try:
#         return service.create(user)
#     except Duplicate as exc:
#         raise HTTPException(status_code=409, detail=exc.msg)



#получение всех пользователей
# @router.get("/")
# def get_all() -> list[User]:
#     return service.get_all()
#
# #получение одного пользователя
# @router.get("/{name}")
# def get_one(name) -> User:
#     try:
#         return service.get_one(name)
#     except Missing as exc:
#         raise HTTPException(status_code=404, detail=exc.msg)



#изменение данных пользователя
# @router.patch("/")
# def modify(name: str, user: User) -> User:
#     try:
#         return service.modify(name, user)
#     except Missing as exc:
#         raise HTTPException(status_code=404, detail=exc.msg)

#удалить пользователя (переместить в другую таблицу)
# @router.delete("/{name}")
# def delete(name: str) -> None:
#     try:
#         return service.delete(name)
#     except Missing as exc:
#         raise HTTPException(status_code=404, detail=exc.msg)