import sqlite3
from model.user import User
from errors import Missing, Duplicate
import secrets
import os

# 1. Получаем путь к родительской папке (выше текущей)
parent_dir = os.path.dirname(os.getcwd())

# 2. Формируем полный путь к базе данных
db_path = os.path.join(parent_dir, 'cryptid.db')

#создание БД
def init_user():
    conn = sqlite3.connect(db_path)
    curs = conn.cursor()
    curs.execute("""create table if not exists user(
                username text primary key,
                password text,
                is_superuser integer)""")
    # Сохраняем изменения и закрываем соединение
    conn.commit()
    conn.close()

def row_to_model(row: tuple) -> User:
    username, password, is_superuser = row
    return User(username=username, password=password, is_superuser=is_superuser)

def model_to_dict(user: User) -> dict:
    return user.dict()

#добавление пользователя в таблицу user
def create(user: User) -> None:
    conn = sqlite3.connect(db_path)
    curs = conn.cursor()
    qry = f"""insert into user
        (username, password, is_superuser)
        values
        (:username, :password, :is_superuser)"""
    params = model_to_dict(user)
    try:
        curs.execute(qry, params)
    except sqlite3.IntegrityError:
        raise Duplicate(msg=
            f"Пользователь {user.name} уже существует")
    # Сохраняем изменения и закрываем соединение
    conn.commit()
    conn.close()


#если есть такой пользователь в БД возвращает True
def check_user(username: str) -> bool:
    conn = sqlite3.connect(db_path)
    curs = conn.cursor()
    qry = "select * from user where username=:username"
    params = {"username": username}
    curs.execute(qry, params)
    row = curs.fetchone()
    #если нашел совпадение
    if row:
        return True
    else:
        return False

def login_user(username: str, password: str) -> bool:
    conn = sqlite3.connect(db_path)
    curs = conn.cursor()
    qry = "select * from user where username=:username"
    params = {"username": username}
    curs.execute(qry, params)
    row = curs.fetchone()
    if row: #если нашел совпадение по имени
        current_password_bytes = password.encode("utf8")
        correct_password_bytes = row[1].encode("utf8")
        is_correct_password = secrets.compare_digest(
            current_password_bytes, correct_password_bytes
        )
        if is_correct_password: #если пароли совпадают
            return True
        else:
            return False
    else:
        return False






def get_one(username: str) -> User:
    conn = sqlite3.connect(db_path)
    curs = conn.cursor()
    qry = "select * from user where username=:username"
    params = {"username": username}
    curs.execute(qry, params)
    row = curs.fetchone()
    if row:
        return row_to_model(row)
    else:
        raise Missing(msg=f"User {username} not found")

def get_all() -> list[User]:
    conn = sqlite3.connect(db_path)
    curs = conn.cursor()
    qry = "select * from user"
    curs.execute(qry)
    return [row_to_model(row) for row in curs.fetchall()]

# def modify(name: str,user: User) -> User:
#     if not user: return None
#     conn = sqlite3.connect(db_path)
#     curs = conn.cursor()
#     qry = """update user set
#     name=:name, password=:password
#     where name=:name0"""
#     params = {
#         "name": user.name,
#         "password": user.password,
#         "name0": name}
#     curs.execute(qry, params)
#     if curs.rowcount == 1:
#         return get_one(user.name)
#         # Сохраняем изменения и закрываем соединение
#         conn.commit()
#         conn.close()
#     else:
#         raise Missing(msg=f"User {name} not found")

#удаляем пользователя
# def delete(username: str) -> None:
#     if not username: return False
#     conn = sqlite3.connect(db_path)
#     curs = conn.cursor()
#     user = get_one(username)
#     qry = "delete from user where username = :username"
#     params = {"username": username}
#     curs.execute(qry, params)
#     if curs.rowcount != 1:
#         raise Missing(msg=f"User {username} not found")



