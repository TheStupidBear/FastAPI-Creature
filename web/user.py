from fastapi import APIRouter, Request, Form
from pathlib import Path
from fastapi.templating import Jinja2Templates
from service import user as service
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
async def reg(request: Request, name: str = Form(...), password: str = Form(...),
              repeat_password: str = Form(...)):
    if password != repeat_password:
        message = "Пароли не совпадают"
        return template_obj.TemplateResponse("registration.html",
                                             {"request": request, "message": message})
    else:
        if service.check_user(name) == True: #если есть в БД такой пользователь
            message = "Такой пользователь уже есть"
            return template_obj.TemplateResponse("registration.html",
                                                 {"request": request, "message": message})
        else:
            service.create(name, password)
            message = f"Привет, {name}"
            return template_obj.TemplateResponse("index.html",
                                                 {"request": request, "message": message})

#страница входа в учетную запись
@router.get("/login")
async def reg(request: Request):
    return template_obj.TemplateResponse("login.html",
                                         {"request": request})

#страница входа
@router.post("/login")
async def login(request: Request, name: str = Form(...), password: str = Form(...)):
    if service.login_user(name, password) == True: #если есть такой пользователь в БД (правильный пароль)
        message = f"Привет, {name}"
        success_login = 1
        return template_obj.TemplateResponse("index.html",
                                             {"request": request, "message": message,
                                              "success_login": success_login})
    else:
        message = "Пароль и логин не совпадают"
        return template_obj.TemplateResponse("login.html",
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