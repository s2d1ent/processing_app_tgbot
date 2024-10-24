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

from config import *
from functions import is_admin
# user
user_std_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True,one_time_keyboard=False)
user_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True,one_time_keyboard=False)
user_config_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True,one_time_keyboard=False)
user_write_question = types.ReplyKeyboardMarkup(resize_keyboard=True,one_time_keyboard=False)
user_write_atachment = types.ReplyKeyboardMarkup(resize_keyboard=True,one_time_keyboard=False)
# admin
admin_std_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True,one_time_keyboard=False)
admin_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True,one_time_keyboard=False)
admin_config_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True,one_time_keyboard=False)
admin_mailling_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True,one_time_keyboard=False)


def start_keyboard(chat_id):
    user_type = is_admin(chat_id)
    if user_type == 0:
        buffer[chat_id].keyboard = 'user_std_keyboard'
        bot.send_message(chat_id,"Обновление клавиатуры",reply_markup=user_std_keyboard)
    elif user_type == 1:
        buffer[chat_id].keyboard  = 'admin_std_keyboard'
        bot.send_message(chat_id,"Обновление клавиатуры",reply_markup=admin_std_keyboard)

def change_keyboard(message, chat_id):
    try:
        result = False
        user_privelegies = is_admin(chat_id)
        buf_value = None
        if str(chat_id) not in str(buffer.keys()):
            text = 'Бот был перезагружен, напишите `/start`'
            bot.send_message(chat_id, text, parse_mode="Markdown")
            return
        buf_value = buffer[chat_id].keyboard             
      
        if message.text == 'Отменить':
            if buffer[chat_id].status == 'user_mode_create_question':
                if buf_value == 'user_write_question':
                    buffer[chat_id].status = ''
                    bot.send_message(chat_id,'Создание заявки отменено!',reply_markup=user_keyboard)
                    buffer[chat_id].keyboard  = 'user_keyboard'
                    result = True

        elif message.text == 'Закончить':
            if buf_value == 'user_write_question':
                text = "Заявка успешно создана"
                bot.send_message(chat_id,text,reply_markup=user_keyboard)
                buffer[chat_id].keyboard  = 'user_keyboard'
                result = True

        elif message.text == 'Назад':
            text = "Назад!"
            if user_privelegies  == 0:
                if buf_value == 'user_std_keyboard':
                    bot.send_message(chat_id,text,reply_markup=user_std_keyboard)
                    buffer[chat_id].keyboard  = 'user_std_keyboard'
                    result = True
                if buf_value == 'user_keyboard':
                    bot.send_message(chat_id,text,reply_markup=user_std_keyboard)
                    buffer[chat_id].keyboard  = 'user_std_keyboard'
                    result = True
                if buf_value == 'user_config_keyboard':
                    bot.send_message(chat_id,text,reply_markup=user_std_keyboard)
                    buffer[chat_id].keyboard  = 'user_std_keyboard'
                    result = True
                if buf_value == 'user_write_question':
                    text = "Заявка успешно создана"
                    bot.send_message(chat_id,text,reply_markup=user_keyboard)
                    buffer[chat_id].keyboard  = 'user_keyboard'
                    result = True
            elif user_privelegies == 1:
                if buf_value == 'admin_std_keyboard':
                    bot.send_message(chat_id,text,reply_markup=admin_std_keyboard)
                    buffer[chat_id].keyboard  = 'admin_std_keyboard'
                    result = True
                if buf_value == 'admin_keyboard':
                    bot.send_message(chat_id,text,reply_markup=admin_std_keyboard)
                    buffer[chat_id].keyboard  = 'admin_std_keyboard'
                    result = True
                if buf_value == 'admin_config_keyboard':
                    bot.send_message(chat_id,text,reply_markup=admin_std_keyboard)
                    buffer[chat_id].keyboard  = 'admin_std_keyboard'
                    result = True
                if buf_value == 'admin_mailling_keyboard':
                    bot.send_message(chat_id,text,reply_markup=admin_std_keyboard)
                    buffer[chat_id].keyboard  = 'admin_std_keyboard'
                    result = True
                if buf_value == 'user_write_question':
                    bot.send_message(chat_id,text,reply_markup=admin_std_keyboard)
                    buffer[chat_id].keyboard  = 'user_keyboard'
                    result = True
                if buf_value == 'user_write_atachment':
                    bot.send_message(chat_id,text,reply_markup=admin_std_keyboard)
                    buffer[chat_id].keyboard  = 'user_write_question'
                    result = True
        
        elif message.text == 'Заявки':
            if user_privelegies  == 0:
                if buf_value == 'user_std_keyboard':
                    bot.send_message(chat_id,"***Вы попали в меню для работы с заявками.***\nДля того чтобы создать заявку нажмите на кнопку ***'Создать заявку'***",
                                     reply_markup=user_keyboard, parse_mode="Markdown")
                    buffer[chat_id].keyboard  = 'user_keyboard'
                    result = True
            elif user_privelegies == 1:
                if buf_value == 'admin_std_keyboard':
                    bot.send_message(chat_id,"Заявки!",reply_markup=admin_keyboard)
                    buffer[chat_id].keyboard  = 'admin_keyboard'
                    result = True

        elif message.text == 'Настройки':
            if user_privelegies  == 0:
                if buf_value == 'user_std_keyboard':
                    bot.send_message(chat_id,"Заявки!",reply_markup=user_config_keyboard)
                    buffer[chat_id].keyboard  = 'user_config_keyboard'
                    buffer[chat_id].status  = 'settings_menu'
                    result = True
            elif user_privelegies == 1:
                if buf_value == 'admin_std_keyboard':
                    bot.send_message(chat_id,"Заявки!",reply_markup=admin_config_keyboard)
                    buffer[chat_id].status  = 'settings_menu'
                    result = True

        elif message.text == 'Рассылка':
            if user_privelegies == 1:
                if buf_value == 'admin_std_keyboard':
                    bot.send_message(chat_id,"Заявки!",reply_markup=admin_mailling_keyboard)
                    buffer[chat_id].keyboard  = 'admin_mailling_keyboard'
                    result = True

        return result
    except Exception as e:
        print("change_keyboard "+repr(e))

def init_keyboards():
    # Открывает user_keyboard
    ustd_btn1 = types.KeyboardButton("Заявки")
    # user_config_keyboard
    ustd_btn2 = types.KeyboardButton("Настройки")
    user_std_keyboard.add(ustd_btn1, ustd_btn2)
    
    # Открывает admin_keyboard
    astd_btn1 = types.KeyboardButton("Заявки")
    # admin_mailling_keyboard
    astd_btn2 = types.KeyboardButton("Рассылка")
    # admin_config_keyboard
    astd_btn3 = types.KeyboardButton("Настройки")
    admin_std_keyboard.add(astd_btn1, astd_btn2, astd_btn3)

    # Рассылка
    amaill_btn1 = types.KeyboardButton("Разослать уведомление")
    amaill_btn2 = types.KeyboardButton("Назад")
    admin_mailling_keyboard.add(amaill_btn1, amaill_btn2)
    # Конец рассылка

    # настройки
    ucfg_btn1 = types.KeyboardButton("Сменить имя пользователя")
    ucfg_btn2 = types.KeyboardButton("Сменить предприятие")
    ucfg_btn3 = types.KeyboardButton("Назад")
    ucfg_btn4 = types.KeyboardButton("Обо мне")
    user_config_keyboard.add(ucfg_btn1, ucfg_btn4, ucfg_btn2, ucfg_btn3)

    acfg_btn1 = types.KeyboardButton("Сменить имя пользователя")
    acfg_btn2 = types.KeyboardButton("Сменить предприятие")
    acfg_btn3 = types.KeyboardButton("Управление БД")
    acfg_btn4 = types.KeyboardButton("Обо мне")
    acfg_btn5 = types.KeyboardButton("Назад")
    admin_config_keyboard.add(acfg_btn1, acfg_btn2, acfg_btn3, acfg_btn4, acfg_btn5)
    # Конец настройки

    # Заявки
    admin_btn1 = types.KeyboardButton("Просмотр заявок")
    admin_btn2 = types.KeyboardButton("Мои заявки")
    admin_btn3 = types.KeyboardButton("Назад")
    admin_keyboard.add(admin_btn1, admin_btn2, admin_btn3)

    user_btn1 = types.KeyboardButton("Создать заявку")
    user_btn2 = types.KeyboardButton("Открытые заявки")
    user_btn4 = types.KeyboardButton("Назад")
    user_keyboard.add(user_btn1, user_btn2, user_btn4)
# Режим создания заявки
    uwq_btn1 = types.KeyboardButton("Закончить")
    uwq_btn2 = types.KeyboardButton("Изменить тему")
    uwq_btn3 = types.KeyboardButton("Изменить комменатрий")
    uwq_btn4 = types.KeyboardButton("Вложения")
    uwq_btn5 = types.KeyboardButton("Отменить")
    user_write_question.add(uwq_btn1, uwq_btn2, uwq_btn3, uwq_btn4, uwq_btn5)
# Вложения  
    uwa_btn1 = types.KeyboardButton("Просмотр вложений")
    uwa_btn2 = types.KeyboardButton("Изменить вложения")
    uwa_btn3 = types.KeyboardButton("Отменить все")
    uwa_btn4 = types.KeyboardButton("Назад")
    user_write_atachment.add(uwa_btn1, uwa_btn2, uwa_btn3, uwa_btn4)
    # Конец заявки
    

def init_keyboards_buffer():
    for user in buffer.values():
        text = 'Бот был перезагружен!'
        isAdmin = is_admin(user.id)
        markup = user_std_keyboard
        keyboard = user.keyboard
        
        if isAdmin == 0:
            if keyboard == "user_std_keyboard":
                markup = user_std_keyboard
            if keyboard == "user_keyboard":
                markup = user_keyboard
            if keyboard == "user_config_keyboard":
                markup = user_config_keyboard
            if keyboard == "user_write_question":
                markup = user_write_question
            if keyboard == "user_write_atachment":
                markup = user_write_atachment
        elif isAdmin == 1:
            if keyboard == "admin_std_keyboard":
                markup = admin_std_keyboard
            if keyboard == "admin_keyboard":
                markup = admin_keyboard
            if keyboard == "admin_config_keyboard":
                markup = admin_config_keyboard
            if keyboard == "admin_mailling_keyboard":
                markup = admin_mailling_keyboard
        bot.send_message(user.id, text,reply_markup=markup, parse_mode="Markdown")
