from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from datetime import timedelta
from model.user import User
from service import user as service
from errors import Missing, Duplicate
from data.user import init_user

ACCESS_TOKEN_EXPIRE_MINUTES = 30
router = APIRouter(prefix="/user")

#создание таблицы БД
init_user()

# --- Новые данные auth
# Эта зависимость создает сообщение в каталоге
# "/user/token" (из формы с именем пользователя и паролем)
# и возвращает токен доступа.
oauth2_dep = OAuth2PasswordBearer(tokenUrl="token")

#некорректный ввод
def unauthed():
    raise HTTPException(
    status_code=401,
    detail="Incorrect username or password",
    headers={"WWW-Authenticate": "Bearer"},
    )

# К этой конечной точке направляется любой вызов,
# содержащий зависимость oauth2_dep():
@router.post("/token")
async def create_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    #Получение имени пользователя и пароля
    #из формы OAuth, возврат токена доступа
    user = service.auth_user(form_data.username, form_data.password)
    if not user:
        unauthed()
    expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = service.create_access_token(
    data={"sub": user.username}, expires=expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

#Возврат текущего токена доступа
@router.get("/token")
def get_access_token(token: str = Depends(oauth2_dep)) -> dict:
    return {"token": token}

#получение всех пользователей
@router.get("/")
def get_all() -> list[User]:
    return service.get_all()

#получение одного пользователя
@router.get("/{name}")
def get_one(name) -> User:
    try:
        return service.get_one(name)
    except Missing as exc:
        raise HTTPException(status_code=404, detail=exc.msg)

#создание пользователя
@router.post("/", status_code=201)
def create(user: User) -> User:
    try:
        return service.create(user)
    except Duplicate as exc:
        raise HTTPException(status_code=409, detail=exc.msg)

#изменение данных пользователя
# @router.patch("/")
# def modify(name: str, user: User) -> User:
#     try:
#         return service.modify(name, user)
#     except Missing as exc:
#         raise HTTPException(status_code=404, detail=exc.msg)

#удалить пользователя (переместить в другую таблицу)
@router.delete("/{name}")
def delete(name: str) -> None:
    try:
        return service.delete(name)
    except Missing as exc:
        raise HTTPException(status_code=404, detail=exc.msg)