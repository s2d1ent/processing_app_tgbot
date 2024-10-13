import sqlite3
from config import db_name

conn = sqlite3.connect(db_name)
cursor = conn.cursor()
file = str()

try:
    with open('./db_dump.sql', 'r', encoding='utf-8') as file:
        file = file.read()
        sql_commands = file.split(";")
        for cmd in sql_commands:
            cmd = cmd.strip()
            if cmd:
                cursor.execute(cmd)
except Exception as e:
    print(repr(e))

conn.commit()
conn.close()
