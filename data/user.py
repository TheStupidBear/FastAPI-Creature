import sqlite3
from model.user import User
from errors import Missing, Duplicate
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
                name text primary key,
                hash text)""")
    curs.execute("""create table if not exists xuser(
                name text primary key,
                hash text)""")
    # Сохраняем изменения и закрываем соединение
    conn.commit()
    conn.close()

def row_to_model(row: tuple) -> User:
    name, hash = row
    return User(name=name, hash=hash)

def model_to_dict(user: User) -> dict:
    return user.dict()

def get_one(name: str) -> User:
    conn = sqlite3.connect(db_path)
    curs = conn.cursor()
    qry = "select * from user where name=:name"
    params = {"name": name}
    curs.execute(qry, params)
    row = curs.fetchone()
    if row:
        return row_to_model(row)
    else:
        raise Missing(msg=f"User {name} not found")

def get_all() -> list[User]:
    conn = sqlite3.connect(db_path)
    curs = conn.cursor()
    qry = "select * from user"
    curs.execute(qry)
    return [row_to_model(row) for row in curs.fetchall()]

#добавление пользователя в таблицу user или xuser
def create(user: User, table:str = "user"):
    if not user: return None
    conn = sqlite3.connect(db_path)
    curs = conn.cursor()
    qry = f"""insert into {table}
        (name, hash)
        values
        (:name, :hash)"""
    params = model_to_dict(user)
    try:
        curs.execute(qry, params)
    except sqlite3.IntegrityError:
        raise Duplicate(msg=
            f"{table}: user {user.name} already exists")
    # Сохраняем изменения и закрываем соединение
    conn.commit()
    conn.close()
    return get_one(user.name)

def modify(name: str,user: User) -> User:
    if not (user): return None
    conn = sqlite3.connect(db_path)
    curs = conn.cursor()
    qry = """update user set
    name=:name, hash=:hash
    where name=:name0"""
    params = {
        "name": user.name,
        "hash": user.hash,
        "name0": name}
    curs.execute(qry, params)
    if curs.rowcount == 1:
        return get_one(user.name)
        # Сохраняем изменения и закрываем соединение
        conn.commit()
        conn.close()
    else:
        raise Missing(msg=f"User {name} not found")

#переводим пользователя в таблицу xuser
def delete(name: str) -> None:
    if not name: return False
    conn = sqlite3.connect(db_path)
    curs = conn.cursor()
    user = get_one(name)
    qry = "delete from user where name = :name"
    params = {"name": name}
    curs.execute(qry, params)
    if curs.rowcount != 1:
        raise Missing(msg=f"User {name} not found")
    create(user, table="xuser")

