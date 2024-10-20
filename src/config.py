import telebot
from telebot import types
from telebot.types import InputMediaPhoto, InputMediaVideo, InputMediaAudio, InputMediaDocument
from datetime import datetime
#db_name = 'DATABASE_NAME'
#dmin_key = 'ADMIN_KEY'
#suadmin_key = 'DONT_WORK_NOW'
#token = "TELEGRAM_BOT_TOKEN"
db_name = 'mponn_it_test'
admin_key = 'Qwerty'
token = "7734632816:AAFdTBHB2BkTpsh4l9zd7vchvLJCvrBWqF4"
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