# MIT License
# 
# Copyright (c) 2024 Viktor Tyumenev
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
# 

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
    db_conn = None
    cursor = None
    try:
        db_conn = sqlite3.connect(db_name)
        cursor = db_conn.cursor()
        cursor.execute(command)
        db_conn.commit()
    except Exception as e:
        print(repr(e))
    finally:
        cursor.close()
        db_conn.close()

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