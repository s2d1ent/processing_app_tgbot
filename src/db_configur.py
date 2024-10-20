import sqlite3
from config import db_name
import sys

db = './db_dump.sql'
triggers = './db_dump_triggers.sql'
data = './db_dump_data.sql'
arg = sys.argv[1]

def execute(database):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    file = str()
    
    try:
        with open(database, 'r', encoding='utf-8') as file:
            #file = file.read()
            #sql_commands = file.split(";")
            #for cmd in sql_commands:
            #    cmd = cmd.strip()
            #    if cmd:
            #        print(cmd)
            #        cursor.execute(cmd)
            with open(arg, 'r') as f:
                sql_script = f.read()
                cursor.executescript(sql_script)
        print(f"The dump {database} import done!")
    #except Exception as e:
    #    print(f"{database} "+repr(e))
    except sqlite3.Error as e:
        print(f"An error occurred: {e}")

    conn.commit()
    conn.close()

execute(arg)