import sqlite3
from model.explorer import Explorer
from errors import Missing, Duplicate
import os

# 1. Получаем путь к родительской папке (выше текущей)
parent_dir = os.path.dirname(os.getcwd())

# 2. Формируем полный путь к базе данных
db_path = os.path.join(parent_dir, 'cryptid.db')

#создание БД
def init_explorer():
    conn = sqlite3.connect(db_path)
    curs = conn.cursor()
    curs.execute("""create table if not exists explorer(
     name text primary key,
     country text,
     description text)""")
    # Сохраняем изменения и закрываем соединение
    conn.commit()
    conn.close()

#преобразует кортеж в обьект модели
def row_to_model(row: tuple) -> Explorer:
    return Explorer(name=row[0], country=row[1], description=row[2])

#преобразует обьект модели в словарь
def model_to_dict(explorer: Explorer) -> dict:
    return explorer.dict()

def get_one(name: str) -> Explorer:
    conn = sqlite3.connect(db_path)
    curs = conn.cursor()
    qry = "select * from explorer where name=:name"
    params = {"name": name}
    curs.execute(qry, params)
    row = curs.fetchone()
    conn.close()
    if row:  # если не пустой
        return row_to_model(row)
    else:
        raise Missing(msg=f"Explorer {name} not found")

def get_all() -> list[Explorer]:
    conn = sqlite3.connect(db_path)
    curs = conn.cursor()
    qry = "select * from explorer"
    curs.execute(qry)
    rows = list(curs.fetchall())
    conn.close()
    return [row_to_model(row) for row in rows]

def create(explorer: Explorer):
    if not explorer: return None
    conn = sqlite3.connect(db_path)
    curs = conn.cursor()
    qry = """insert into explorer values
    (:name, :country, :description)"""
    params = model_to_dict(explorer)
    try:
        curs.execute(qry, params)
    except sqlite3.IntegrityError:
        raise Duplicate(msg=
                        f"Explorer {explorer.name} already exists")
    # Сохраняем изменения и закрываем соединение
    conn.commit()
    conn.close()
    return get_one(explorer.name)

def modify(explorer: Explorer):
    conn = sqlite3.connect(db_path)
    curs = conn.cursor()
    qry = """update explorer
     set country=:country,
     name=:name,
     description=:description,
     where name=:name_orig"""
    params = model_to_dict(explorer)
    params["name_orig"] = explorer.name
    _ = curs.execute(qry, params)
    # Сохраняем изменения и закрываем соединение
    conn.commit()
    conn.close()
    return get_one(explorer.name)


def delete(name: str):
    if not name: return False
    conn = sqlite3.connect(db_path)
    curs = conn.cursor()
    qry = "delete from explorer where name = :name"
    params = {"name": name}
    res = curs.execute(qry, params)
    if curs.rowcount != 1:
        raise Missing(msg=f"Explorer {name} not found")
    # Сохраняем изменения и закрываем соединение
    conn.commit()
    conn.close()
    return bool(res)