import sqlite3
from model.creature import Creature
from errors import Missing, Duplicate

DB_NAME = "cryptid.db"

#создание БД
def init_creature():
    conn = sqlite3.connect(DB_NAME)
    curs = conn.cursor()
    curs.execute("""create table if not exists creature(
     name text primary key,
     description text,
     country text,
     area text,
     aka text)""")
    # Сохраняем изменения и закрываем соединение
    conn.commit()
    conn.close()

#преобразует кортеж в обьект модели
def row_to_model(row: tuple) -> Creature:
    name, description, country, area, aka = row
    return Creature(name=name, description=description,
                    country=country, area=area, aka=aka)

#преобразует обьект модели в словарь
def model_to_dict(creature: Creature) -> dict:
    return creature.dict()

def get_one(name: str) -> Creature:
    conn = sqlite3.connect(DB_NAME)
    curs = conn.cursor()
    qry = "select * from creature where name=:name"
    params = {"name": name}
    curs.execute(qry, params)
    row = curs.fetchone()
    conn.close()
    if row: #если не пустой
        return row_to_model(row)
    else:
        raise Missing(msg=f"Creature {name} not found")

def get_all() -> list[Creature]:
    conn = sqlite3.connect(DB_NAME)
    curs = conn.cursor()
    qry = "select * from creature"
    curs.execute(qry)
    rows = list(curs.fetchall())
    conn.close()
    return [row_to_model(row) for row in rows]

def create(creature: Creature):
    if not creature: return None
    conn = sqlite3.connect(DB_NAME)
    curs = conn.cursor()
    qry = """insert into creature values
        (:name, :description, :country, :area, :aka)"""
    params = model_to_dict(creature)
    try:
        curs.execute(qry, params)
    except sqlite3.IntegrityError:
        raise Duplicate(msg=
                        f"Creature {creature.name} already exists")
    # Сохраняем изменения и закрываем соединение
    conn.commit()
    conn.close()
    return get_one(creature.name)

def modify(creature: Creature):
    if not (creature): return None
    conn = sqlite3.connect(DB_NAME)
    curs = conn.cursor()
    qry = """update creature
     set country=:country,
     name=:name,
     description=:description,
     area=:area,
     aka=:aka
     where name=:name_orig"""
    params = model_to_dict(creature)
    params["name_orig"] = creature.name
    _ = curs.execute(qry, params)
    # Сохраняем изменения и закрываем соединение
    conn.commit()
    conn.close()
    return get_one(creature.name)


def delete(name: str):
    if not name: return False
    conn = sqlite3.connect(DB_NAME)
    curs = conn.cursor()
    qry = "delete from creature where name = :name"
    params = {"name": name}
    res = curs.execute(qry, params)
    if curs.rowcount != 1:
        raise Missing(msg=f"Creature {name} not found")
    # Сохраняем изменения и закрываем соединение
    conn.commit()
    conn.close()
    return bool(res)