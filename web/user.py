from fastapi import APIRouter, Request, Form
from pathlib import Path
from fastapi.templating import Jinja2Templates
from typing import Annotated
from service import user as user_service
from model.user import User

router = APIRouter(prefix="/user")

parent_dir = Path(__file__).resolve().parent.parent
template_obj = Jinja2Templates(directory=f"{parent_dir}/template")

#главная страница
@router.post("/login")
async def top(request: Request):
    return template_obj.TemplateResponse("login.html",
                                         {"request": request})


@router.post("/get_token")
async def login(username: Annotated[str, Form()], password: Annotated[str, Form()]):
    #получаем токен и возращаем клиенту
    token = user_service.login_for_access_token(username, password)
    return token

@router.post("/me")
async def read_me(token: str):
    #декодируем токен и получаем обьект пользователя
    return user_service.get_current_user(token)