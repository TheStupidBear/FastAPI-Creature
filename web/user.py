from fastapi import APIRouter, Request, Form, Depends
from pathlib import Path
from fastapi.templating import Jinja2Templates
from typing import Annotated
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from service import user as service
from data.user import init_user
from model.user import User


router = APIRouter(prefix="/user")

parent_dir = Path(__file__).resolve().parent.parent
template_obj = Jinja2Templates(directory=f"{parent_dir}/template")

fake_users_db = {
    "johndoe": {
        "username": "johndoe",
        "hashed_password": "fakehashedsecret",
        "is_superuser": 0,
    },
    "alice": {
        "username": "alice",
        "hashed_password": "fakehashedsecret2",
        "is_superuser": 0,
    },
}

def fake_hash_password(password: str):
    return "fakehashed" + password

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

@router.get("/items/")
async def read_items(token: Annotated[str, Depends(oauth2_scheme)]):
    return {"token": token}

def fake_decode_token(token):
    return User(
        username=token + "fakedecoded", hashed_password="1234", is_superuser=0
    )

async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    user = fake_decode_token(token)
    return user


@router.get("/me")
async def read_users_me(current_user: Annotated[User, Depends(get_current_user)]):
    return current_user


# #создание таблицы БД
# init_user()
#
# #страница регистрации
# @router.get("/registration")
# async def reg(request: Request):
#     return template_obj.TemplateResponse("registration.html",
#                                          {"request": request})
#
#
#
# #post запрос регистрации
# @router.post("/registration")
# async def reg(request: Request, name: str = Form(...), password: str = Form(...),
#               repeat_password: str = Form(...)):
#     if password != repeat_password:
#         message = "Пароли не совпадают"
#         return template_obj.TemplateResponse("registration.html",
#                                              {"request": request, "message": message})
#     else:
#         if service.check_user(name) == True: #если есть в БД такой пользователь
#             message = "Такой пользователь уже есть"
#             return template_obj.TemplateResponse("registration.html",
#                                                  {"request": request, "message": message})
#         else:
#             service.create(name, password)
#             success_login = 1
#             message = f"Привет, {name}"
#             return template_obj.TemplateResponse("index.html",
#                                                  {"request": request, "message": message,
#                                                   "success_login": success_login})
#
# #страница входа в учетную запись
# @router.get("/login")
# async def reg(request: Request):
#     return template_obj.TemplateResponse("login.html",
#                                          {"request": request})
#
# #страница входа
# @router.post("/login")
# async def login(request: Request, name: str = Form(...), password: str = Form(...)):
#     if service.login_user(name, password) == True: #если есть такой пользователь в БД (правильный пароль)
#         message = f"Привет, {name}"
#         success_login = 1
#         return template_obj.TemplateResponse("index.html",
#                                              {"request": request, "message": message,
#                                               "success_login": success_login})
#     else:
#         message = "Пароль и логин не совпадают"
#         return template_obj.TemplateResponse("login.html",
#                                              {"request": request, "message": message})



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