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

import telebot
from telebot import types
from telebot.types import InputMediaPhoto, InputMediaVideo, InputMediaAudio, InputMediaDocument
from datetime import datetime
db_name = 'DATABASE_NAME'
dmin_key = 'ADMIN_KEY'
suadmin_key = 'DONT_WORK_NOW'
token = "TELEGRAM_BOT_TOKEN"
buffer = {}
user_status = {}
user_questions_buf = {}
bot = telebot.TeleBot(token)

emojis = {
    'ok'        : 'U+2705',
    'crosshair' : 'U+274C',
    'gball'     : 'U+1F7E2',
    'rball'     : 'U+1F534',
    'left'      : 'U+2B05',
    'right'     : 'U+27A1',
    're'        : 'U+1F501',
    'readdr'    : 'U+1F503',
    'new'       : 'U+1F525'
}

class UserBuffer:
    def __init__(self, chat_id):
        self.id = chat_id
        self.name = str()
        self.question = QuestionBuffer()
        self.status = ''
        self.keyboard = ''
        self.variables = {}
        self.is_admin = 0
        self.company = 0
        self.departament = 0
        self.email = str()


class QuestionBuffer:
    def __init__(self):
        self.id = 0
        self.thema = -1
        self.description = ''
        self.files = []

class FileBuffer:
    def __init__(self):
        self.file_id = 0
        self.contentType = 0
        self.date = 0
