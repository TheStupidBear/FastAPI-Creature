from fastapi import APIRouter, Request, Form, Depends, HTTPException, status, Header
from pathlib import Path
from fastapi.templating import Jinja2Templates
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
import secrets
from typing import Annotated
from service import user as service
from data.user import init_user
from model.user import User, Token, TokenData

fake_users_db = {
    "johndoe": {
        "username": "johndoe",
        "hashed_password": "fakehashedsecret",
    },
    "alice": {
        "username": "alice",
        "hashed_password": "fakehashedsecret2",
    },
}

router = APIRouter(prefix="/user")

# #создание таблицы БД
# init_user()
#создание схемы oauth2
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="user/token")

parent_dir = Path(__file__).resolve().parent.parent
template_obj = Jinja2Templates(directory=f"{parent_dir}/template")

def fake_hash_password(password: str):
    return "fakehashed" + password

def get_user(db, username: str):
    if username in db:
        user_dict = db[username]
        print(f"Модель User: {User(**user_dict)}")
        return User(**user_dict)

def fake_decode_token(token):
    # This doesn't provide any security at all
    # Check the next version
    user = get_user(fake_users_db, token)
    return user


def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    user = fake_decode_token(token)
    print(f"token: {token}")
    print(f"user: {user}")
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user

@router.post("/token")
async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    user_dict = fake_users_db.get(form_data.username)
    if not user_dict:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    user = User(**user_dict)
    hashed_password = fake_hash_password(form_data.password)
    if not hashed_password == user.hashed_password:
        raise HTTPException(status_code=400, detail="Incorrect username or password")

    return Token(access_token=user.username, token_type="bearer")

@router.get("/me")
def read_users_me(current_user: Annotated[User, Depends(get_current_user)]):
    return current_user

@router.post("/login")
def get_all(request: Request):
    return template_obj.TemplateResponse("login.html",
                                         {"request": request})
# @router.post("/login")
# async def read_users_me():
#     return "current_user"

# #отправка формы (войти в учетную запись)
# @router.post("/login")
# def login_post(request: Request):
#     pass




#страница регистрации
@router.get("/registration")
async def reg(request: Request):
    return template_obj.TemplateResponse("registration.html",
                                         {"request": request})
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