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
            with open(arg, 'r') as f:
                sql_script = f.read()
                cursor.executescript(sql_script)
        print(f"The dump {database} import done!")
    except sqlite3.Error as e:
        print(f"An error occurred: {e}")

    conn.commit()
    conn.close()

execute(arg)