import sqlite3
import os

# 1. Получаем путь к родительской папке (выше текущей)
parent_dir = os.path.dirname(os.getcwd())
# 2. Формируем полный путь к базе данных
db_path = os.path.join(parent_dir, 'cryptid.db')

def get_word() -> str:
    conn = sqlite3.connect(db_path)
    curs = conn.cursor()
    qry = "select name from creature order by random() limit 1"
    curs.execute(qry)
    row = curs.fetchone()
    if row: #если есть одно существо
        name = row[0]
    else:
        name = "bigfoot"
    conn.close()
    return name