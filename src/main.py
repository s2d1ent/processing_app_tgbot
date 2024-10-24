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
import time
import os
import buffering
import threading
from datetime import datetime
from db_functions import *
from config import bot, buffer
from functions import *
from user_space import inline_handler_user, message_handler_user
from admin_space import inline_handler_admin, message_handler_admin
from keyboards import init_keyboards, start_keyboard, change_keyboard, init_keyboards_buffer


@bot.message_handler(commands=['start'])
def cmd_start(message):
    try:
        chat_id = message.chat.id
        user_exist = is_registered(message.chat.id)
        if user_exist == True:
            if str(chat_id) not in str(buffer.keys()):
                buffer[chat_id] = buffering.UserBuffer(chat_id)
                print("User has not buffered data")
            start_keyboard(chat_id)
        else:
            if str(chat_id) not in str(buffer.keys()):
                buffer[chat_id] = buffering.UserBuffer(chat_id)
            bot.send_message(chat_id, 'Укажите ФИО полность. Пример: Иванов Иван Иванович', parse_mode="Markdown")
            buffer[chat_id].status = 'user_registering'               
            bot.register_next_step_handler(message, user_reg)
    except Exception as e:
        print(repr(e))

@bot.callback_query_handler(func=lambda call: True)
def inline_handler(call):
    try:
# share_space
        chat_id = call.message.chat.id
        message = call.message
        user_privelegies = is_admin(chat_id)  
        if message.chat.type != 'private':
            send_message(chat_id, "Вам не доступна данная функция")
            return
        if call.message:
            if call.data == 'start_after_reg':
                buffer[chat_id].status = ''
                bot.edit_message_text(chat_id=message.chat.id, message_id=message.message_id, text="Выберите Вашу компанию!")
                start_keyboard(chat_id)
                send_message(chat_id, "***БОТ НАХОДИТСЯ НА СТАДИИ РАЗРАБОТКИ.***\nПри любом странном поведени бота пропишите: `/start`")
                return
            if buffer[chat_id].status == 'user_registering' or buffer[chat_id].status == 'admin_registering':
                if "registering_take_company:" in call.data:
                    id = str(call.data).replace('registering_take_company:','')
                    buffer[chat_id].company = id
                    bot.edit_message_text(chat_id=message.chat.id, message_id=message.message_id, text="Выберите Вашу компанию!")
                    take_departament(message)
                elif "registering_take_departament:" in call.data:
                    id = str(call.data).replace('registering_take_departament:','')
                    buffer[chat_id].departament = id
                    bot.edit_message_text(chat_id=message.chat.id, message_id=message.message_id, text="Выберите Ваш отдел!")
                    if buffer[chat_id].status == 'admin_registering':
                        send_message(message.chat.id, 'Укажите адрес электронной почты!')
                        time.sleep(1)
                        bot.register_next_step_handler(call.message, insert_email)
                    else:
                        user_registering(chat_id)
                return
        if user_privelegies  == 0:
            inline_handler_user(call, chat_id)
        elif user_privelegies == 1:
            inline_handler_admin(call, chat_id)
        else:
            print("Недостаточно прав")  
    except Exception as e:
        print(repr(e))

@bot.message_handler(func=lambda message: True)
def message_handler(message):
    try:
# share_space
        if message.chat.type == 'private':
            chat_id = message.chat.id
            user_privelegies = is_admin(chat_id)

            change_keyboard(message, chat_id)
            if user_privelegies  == 0:
                message_handler_user(message, chat_id)
            elif user_privelegies == 1:
                message_handler_admin(message, chat_id)
            else:
                print("Недостаточно прав") 

        else:
            send_message(message.chat.id, 'Бот работает только в личной переписке')
    except Exception as e:
        print("message_handler " + repr(e))

@bot.message_handler(content_types=['photo', 'voice', 'audio', 'video', 'video_note', 'document'])
def media_handler(message):
    try:
        if message.chat.type == 'private':
            chat_id = message.chat.id
            user_privelegies = is_admin(chat_id)
            file = None
            if user_privelegies == -1:
                return
            
            file = buffering.FileBuffer()
            file.date = datetime.now().strftime("%d.%m.%Y %H:%M")
            if message.photo:
                file.contentType = 1
                for photo in message.photo:
                    file.file_id = photo.file_id
                    break
            elif message.voice:
                file.contentType = 2
                file.file_id = message.voice.file_id
            elif message.document:
                file.contentType = 3
                file.file_id = message.document.file_id
            elif message.audio:
                file.contentType = 4
                file.file_id = message.audio.file_id
            elif message.video:
                file.contentType = 5
                file.file_id = message.video.file_id
            elif message.video_note:
                file.contentType = 6
                file.file_id = message.video_note.file_id
            if buffer[chat_id].status == 'user_mode_create_question':
                buffer[chat_id].question.files.append(file)
                db_execute(f"INSERT INTO Files (file_id, contentType, owner_id, date) VALUES('{file.file_id}', {file.contentType}, {chat_id}, '{file.date}')")

                    
    except Exception as e:
        print(repr(e))

#TODO
if __name__ == '__main__':
    try:
# Сохранение PID процесса
        with open('./PID', 'w') as file:
            file.write(f'{os.getpid()}\n')
        print("Initialize: PID write")
        buffering.get_buffer()
        print("Initialize: copy buffer done")
# Инициализация клавиатур
        init_keyboards()
        print("Initialize: Keybord initialized")
# Инициализация клавиатуры из буффера
        if ~buffering.isCleanBuffer:
            init_keyboards_buffer()
            print("Initialize: user old keyboard write")
# Запуск буферизации
        threading.Thread(target=buffering.run).start()
        print("Initialize: buffering start")
# Запуск бота
        bot.polling(none_stop=True,timeout=30)
    except Exception as e:
        time.sleep(30)