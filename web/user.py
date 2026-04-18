from fastapi import APIRouter, Depends, HTTPException, status, Request, Form
from pathlib import Path
from fastapi.templating import Jinja2Templates
from typing import Annotated
from fastapi.security import OAuth2PasswordRequestForm
from service import user as service
from data.user import init_user
from model.user import User, Token
from core.security import create_access_token


router = APIRouter(prefix="/user")

parent_dir = Path(__file__).resolve().parent.parent
template_obj = Jinja2Templates(directory=f"{parent_dir}/template")

#страница входа в учетную запись
@router.get("/login")
async def reg(request: Request):
    return template_obj.TemplateResponse("login.html",
                                         {"request": request})

#Логин пользователя. Принимает username и password (form-data), возвращает JWT токен.
@router.post("/login", response_model=Token)
async def login(request: Request, form_data: OAuth2PasswordRequestForm = Depends()):
    # Проверяем пользователя
    user = service.authenticate_user(form_data.username, form_data.password)
    print(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Создаём токен
    create_access_token(data={"sub": user.username})
    message = f"Привет, {form_data.username}"
    success_login = 1
    return template_obj.TemplateResponse("index.html",
                                        {"request": request, "message": message,
                                        "success_login": success_login})


#Возвращает информацию о текущем пользователе. Требует валидный JWT токен в заголовке Authorization.
@router.get("/me")
async def read_users_me(current_user: Annotated[User, Depends(service.get_current_user)]):
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