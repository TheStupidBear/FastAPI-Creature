from fastapi import APIRouter, Request, Depends, HTTPException
from pathlib import Path
from fastapi.templating import Jinja2Templates
from fastapi.security import OAuth2PasswordRequestForm
from typing import Annotated
from service import user as service
from data.user import init_user
from model.user import User, Token



router = APIRouter(prefix="/user")




# #создание таблицы БД
# init_user()

parent_dir = Path(__file__).resolve().parent.parent
template_obj = Jinja2Templates(directory=f"{parent_dir}/template")




#получение текущего пользователя
@router.get("/me")
async def read_users_me(
    current_user: Annotated[User, Depends(service.get_current_user)],
):
    print(current_user)
    return current_user

#роутер на post запрос кнопки "Войти"
@router.post("/login")
def get_all(request: Request):
    return template_obj.TemplateResponse("login.html",
                                         {"request": request})

#post запрос с проверкой username и hashed_password (возвращает токен)
@router.post("/token")
async def login(request: Request, form_data: Annotated[OAuth2PasswordRequestForm, Depends()]) -> Token:
    user_dict = service.fake_users_db.get(form_data.username)
    print("user_dict", user_dict)
    if not user_dict:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    user = User(**user_dict)
    print("user", user)
    hashed_password = service.fake_hash_password(form_data.password)
    print("hashed_password", hashed_password)
    if not hashed_password == user.hashed_password:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    return Token(username=user.username, access_token=user.username, token_type="bearer")


# #страница регистрации
# @router.get("/registration")
# async def reg(request: Request):
#     return template_obj.TemplateResponse("registration.html",
#                                          {"request": request})
#
#
# #post запрос регистрации
# @router.post("/registration")
# async def reg(request: Request, username: str = Form(...), password: str = Form(...),
#               repeat_password: str = Form(...)):
#     #проверка паролей (они одинаковы или нет)
#     current_password_bytes = password.encode("utf8")
#     correct_password_bytes = repeat_password.encode("utf8")
#     is_correct_password = secrets.compare_digest(
#         current_password_bytes, correct_password_bytes
#     )
#     if not is_correct_password:  # если пароли совпадают
#         message = "Пароли не совпадают"
#         return template_obj.TemplateResponse("registration.html",
#                                              {"request": request, "message": message})
#     else:
#         if service.check_user(username):  # если есть в БД такой пользователь
#             message = "Такой пользователь уже есть"
#             return template_obj.TemplateResponse("registration.html",
#                                                  {"request": request, "message": message})
#         else:
#             service.create(User(username=username, password=password))
#             message = f"Привет, {username}"
#             return template_obj.TemplateResponse("main.html",
#                                                  {"request": request, "message": message})




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