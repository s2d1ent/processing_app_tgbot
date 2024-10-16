import sqlite3
from config import db_name
db_conn = None
cursor = None
is_open = False

def db_start():
    try:
        global db_conn
        global cursor
        global is_open
        db_conn = sqlite3.connect(db_name)
        cursor = db_conn.cursor()
        is_open = True
    except Exception as e:
        print('db_start '+repr(e))

def db_close():
    try:
        global is_open
        cursor.close()
        db_conn.close()
        is_open = False
    except Exception as e:
        print('db_close '+repr(e))

def db_execute(command):
    try:
        db_start()
        cursor.execute(command)
        db_conn.commit()
    except Exception as e:
        print(repr(e))
    finally:
        cursor.close()
        db_conn.close()
        is_open = False

def db_execute_fetch(command):
    db_conn = None
    cursor = None
    try:
        db_conn = sqlite3.connect(db_name)
        cursor = db_conn.cursor()
        cursor.execute(command)
        db_conn.commit()
        return cursor.fetchall()
    except Exception as e:
        print(repr(e))
    finally:
        cursor.close()
        db_conn.close()

def is_registered(chat_id):
    db_conn = None
    cursor = None
    try:
        db_conn = sqlite3.connect(db_name)
        cursor = db_conn.cursor()
        is_open = True
        cursor.execute(f"select * from Users where tg_id='{chat_id}'")
        db_conn.commit()
        request = cursor.fetchall()
        if len(request) != 0:
            return True
        return False
    except Exception as e:
        print('is_registered '+repr(e))
    finally:
        cursor.close()
        db_conn.close()
        
def clone_buffer():
    None

def push_buffer():
    None

def is_exist_question(date, chat_id, thema):
    fetch = db_execute_fetch(f"SELECT * FROM Questions WHERE date='{date}' and creater='{chat_id}' and thema='{thema}'")
    if len(fetch) != 0:
        for row in fetch:
            return row[0]
    return -1