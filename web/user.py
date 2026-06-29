from fastapi import APIRouter, Request
from pathlib import Path
from fastapi.templating import Jinja2Templates
from service import user as user_service
from data.user import init_user
from model.user import User, TokenGet




router = APIRouter(prefix="/user")

# #создание таблицы БД
init_user()

parent_dir = Path(__file__).resolve().parent.parent
template_obj = Jinja2Templates(directory=f"{parent_dir}/template")



@router.post("/login")
async def login(user: User):
    #получаем токен и возращаем клиенту
    token = user_service.login_for_access_token(user.username, user.password)
    return token

@router.post("/me")
async def read_me(token: str):
    #декодируем токен и получаем обьект пользователя
    return user_service.get_current_user(token)


#страница регистрации
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



