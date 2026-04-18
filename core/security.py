from pwdlib import PasswordHash
from datetime import datetime, timedelta, timezone
import jwt
from core.settings import ALGORITHM, SECRET_KEY

#настройка хэширования пароля
password_hash = PasswordHash.recommended()
DUMMY_HASH = password_hash.hash("dummypassword")

#Проверяет, совпадает ли введённый пароль с хешем в базе
def verify_password(plain_password, hashed_password):
    return password_hash.verify(plain_password, hashed_password)

#Хеширует пароль для сохранения в базу
def get_password_hash(password):
    return password_hash.hash(password)

#Создаёт JWT токен с данными из data
def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    print("encoded_jwt", encoded_jwt)
    return encoded_jwt

