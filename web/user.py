from fastapi import APIRouter, Depends, HTTPException, status, Request, Form
from pathlib import Path
from fastapi.templating import Jinja2Templates
from typing import Annotated
from fastapi.security import HTTPBasic, HTTPBasicCredentials
import secrets
from service import user as service
from data.user import init_user
from model.user import User


router = APIRouter(prefix="/user")

security = HTTPBasic()

# #создание таблицы БД
init_user()

parent_dir = Path(__file__).resolve().parent.parent
template_obj = Jinja2Templates(directory=f"{parent_dir}/template")

def get_current_user(credentials: Annotated[HTTPBasicCredentials, Depends(security)]):
    return {"username": credentials.username}
#зависимость (только для авторизованных пользователей)
get_user_depends = Annotated[dict, Depends(get_current_user)]


#отправка формы (войти в учетную запись)
@router.post("/login")
def login_post(request: Request,
    credentials: Annotated[HTTPBasicCredentials, Depends(security)],
    ):
    if service.login_user(credentials): #если прошла аутентификация
        message = f"Привет, {credentials.username}"
        return template_obj.TemplateResponse("index.html",
                                             {"request": request, "message": message})
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Basic"},
        )
        # message = f"Неправильный логин и пароль"
        # return template_obj.TemplateResponse("index.html",
        #                                  {"request": request, "message": message})





#страница регистрации
@router.get("/registration")
async def reg(request: Request, get_user: Annotated[dict, Depends(get_current_user)]):
    print(get_user)
    return template_obj.TemplateResponse("registration.html",
                                         {"request": request})


#post запрос регистрации
@router.post("/registration")
async def reg(request: Request, username: str = Form(...), password: str = Form(...),
              repeat_password: str = Form(...)):
    #проверка паролей (они одинаковы или нет)
    current_password_bytes = password.encode("utf8")
    correct_password_bytes = repeat_password.encode("utf8")
    is_correct_password = secrets.compare_digest(
        current_password_bytes, correct_password_bytes
    )
    if not is_correct_password:  # если пароли совпадают
        message = "Пароли не совпадают"
        return template_obj.TemplateResponse("registration.html",
                                             {"request": request, "message": message})
    else:
        if service.check_user(username):  # если есть в БД такой пользователь
            message = "Такой пользователь уже есть"
            return template_obj.TemplateResponse("registration.html",
                                                 {"request": request, "message": message})
        else:
            service.create(User(username=username, password=password))
            message = f"Привет, {username}"
            return template_obj.TemplateResponse("index.html",
                                                 {"request": request, "message": message})




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