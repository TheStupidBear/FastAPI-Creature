from fastapi import APIRouter
from service import user as user_service
from model.user import User

router = APIRouter(prefix="/user")

@router.post("/get_token")
async def login(user: User):
    #получаем токен и возращаем клиенту
    token = user_service.login_for_access_token(user.username, user.password)
    return token

@router.post("/me")
async def read_me(token: str):
    #декодируем токен и получаем обьект пользователя
    return user_service.get_current_user(token)