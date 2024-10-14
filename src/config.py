import telebot
from telebot import types
from datetime import datetime
#db_name = 'DATABASE_NEMA'
#dmin_key = 'ADMIN_KEY'
#token = "TELEGRAM_BOT_TOKEN"
db_name = 'mponn_it_test'
admin_key = 'Qwerty!'
suadmin_key = 'DONT_WORK_NOW'
token = "7734632816:AAFdTBHB2BkTpsh4l9zd7vchvLJCvrBWqF4"
user_status = {}
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
