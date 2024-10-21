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
from functions import *
from keyboards import change_keyboard
from datetime import datetime

def inline_handler_user(call, chat_id):
    if call.message:
# Отмена заявки(Пользователь)
        if f"cancel_id:" in call.data:
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="Какая конкретно заявка тебя интересует ?")
            id = str(call.data).replace(f"cancel_id:",'')
            db_execute(f"UPDATE Questions SET status=2 WHERE id={id}")
            send_message(call.message.chat.id, f"***Ваша заявка №{id} отменена***")
            question_alert(id, 0)
            return
# Выбор темы
        if f'user_choice_thems:' in call.data:
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="Какая тема вашей заявки ?")
            id = str(call.data).replace(f"user_choice_thems:",'')
            buffer[chat_id].question.thema = id
            fetch = db_execute_fetch(f"SELECT name FROM QuestionThems WHERE id={id}")
            if len(fetch) != 0:
                for row in fetch:
                    send_message(chat_id, f"Вы выбрали тему: ***{row[0]}***")
            return
# Удаление фото из вложений к заявке
        if f'user_delete_photo:' in call.data:
            id = int(str(call.data).replace(f"user_delete_photo:",''))
            buffer[chat_id].question.files.remove(buffer[chat_id].question.files[id])
            send_message(chat_id, 'Вложение было удалено!')
# Отмена заявки через просмотр заявок
        if f'user_check_question_cancel:' in call.data:
            id = int(str(call.data).replace(f"user_check_question_cancel:",''))
            db_execute(f"UPDATE Questions SET status=2 WHERE id={id}")
            send_message(call.message.chat.id, f"***Ваша заявка №{id} отменена***")
            question_alert(id, 0)
            return            

def message_handler_user(message, chat_id):
    try:
        if str(chat_id) not in str(buffer.keys()):
            return
        else:
# Создание заявки d ht;bvt cjplfybz pfzdrb
            if buffer[chat_id].status == 'user_mode_create_question_thema':
                buffer[chat_id].status = 'user_mode_create_question'
                buffer[chat_id].question.thema = message.text
                send_message(chat_id, f"Вы изменили тему заявки на: {message.text}")
                return
            elif buffer[chat_id].status == 'user_mode_create_question_comment':
                buffer[chat_id].status = 'user_mode_create_question'
                send_message(chat_id, f"ВРЕМЕННО НЕ РАБОТАЕТ")
                return
            elif buffer[chat_id].status == 'user_mode_create_question':
                if message.text == "Изменить тему":
                    fetch = db_execute_fetch("SELECT id, name FROM QuestionThems")
                    text = "Какая тема вашей заявки ?"
                    if len(fetch) != 0:
                        markup = types.InlineKeyboardMarkup(row_width=2)
                        for row in fetch:
                            item = types.InlineKeyboardButton(f"{row[1]}", callback_data=f'user_choice_thems:{row[0]}')
                            markup.add(item)
                        bot.send_message(chat_id,text,reply_markup=markup, parse_mode="Markdown")
                    else :
                        send_message(chat_id, 'Не удалось подгрузить темы! Выставлено автоматическая тема: Неизвестная проблема')
                        buffer[chat_id].question.thema = 'Неизвестная проблема'
                    return
                elif message.text == "Изменить комменатрий":
                    #buffer[chat_id].status = 'user_mode_create_question_comment'
                    return
                elif message.text == "Вложения":
                    if len(buffer[chat_id].question.files) == 0:
                        send_message(chat_id, 'Вложения отсутствуют')
                        return
                    for file in buffer[chat_id].question.files:
                        markup = types.InlineKeyboardMarkup(row_width=2)
                        arr_index = 0
                        content_type = file.contentType
                        for arr_index in range(0,len(buffer[chat_id].question.files)):
                            if buffer[chat_id].question.files[arr_index].file_id == file.file_id:
                                break
                        
                        item = types.InlineKeyboardButton(f"Удалить", callback_data=f'user_delete_photo:{arr_index}')
                        markup.add(item)
                        if content_type == 1:
                            bot.send_photo(chat_id, file.file_id, reply_markup=markup)       
                        elif content_type == 2:
                            bot.send_voice(chat_id, file.file_id, reply_markup=markup)
                        elif content_type == 3:
                            bot.send_document(chat_id, file.file_id, reply_markup=markup)
                        elif content_type == 4:
                            bot.send_audio(chat_id, file.file_id, reply_markup=markup)
                        elif content_type == 5:
                            bot.send_video(chat_id, file.file_id, reply_markup=markup)
                        elif content_type == 6:
                            bot.send_video_note(chat_id, file.file_id, reply_markup=markup)
                    return
                elif message.text == "Отменить":
                    change_keyboard(message, chat_id)
                    return
                elif message.text == "Закончить":
                    if buffer[chat_id].question.thema == -1 or (buffer[chat_id].question.description == '' and len(buffer[chat_id].question.files) == 0):
                        send_message(chat_id, f"Вы не можете закончить написание заявки если у Вас нет описания проблемы и выбраннолй темы")
                        return
                    else:
                        date = datetime.now().strftime("%d.%m.%Y %H:%M")
                        comm = str(buffer[chat_id].question.description)
                        comm = comm.replace("'","`").replace("\"","`")
                        thema = buffer[chat_id].question.thema
                        question_id = -1
                        db_execute(f"INSERT INTO Questions(date, creater, createrComment, thema, status) VALUES('{date}', '{chat_id}', '{comm}', {thema}, 1)")

                        fetch = db_execute_fetch(f"SELECT id FROM Questions WHERE date='{date}' and creater='{chat_id}' and thema={thema}")
                        if len(fetch) == 0:
                            send_message(chat_id, "Не удалось создать заявку")
                            change_keyboard(message, chat_id)
                        else:
                            for row in fetch:
                                question_id = row[0]
                            for file in buffer[chat_id].question.files:
                                file_fetch = db_execute_fetch(f"SELECT id FROM Files WHERE file_id='{file.file_id}' and date='{file.date}'")
                                for files in file_fetch:
                                    db_execute(f"INSERT INTO QuestionFiles (question_id, fileId) VALUES({question_id}, '{files[0]}')")
                            admins_alert(question_id)
                            buffer[chat_id].question.thema = -1
                            buffer[chat_id].question.description = ''
                            buffer[chat_id].question.files.clear()
                            buffer[chat_id].status = ''
                            change_keyboard(message, chat_id)
                            
                        return
                buffer[chat_id].question.description += message.text + '\n'
                return
        if message.text == 'Создать заявку':
            buffer[chat_id].status = 'user_mode_create_question'
            text = "Вы перешли в режим создания заявок.\n"
            text += "Все что вы будете писать будет записано в поле комментарий, поэтому для того чтобы написать тему запроса нужно нажать ***Изменить тему***\n"
            text += "*Все файлы что будут отправлены в этом режиме будут считаться вложением к заявке.*\n"
            bot.send_message(chat_id,text,parse_mode="Markdown")
            
            text = f"Какая тема вашей заявки ?"
            fetch = db_execute_fetch("SELECT id, name FROM QuestionThems")
            if len(fetch) != 0:
                markup = types.InlineKeyboardMarkup(row_width=2)
                for row in fetch:
                    item = types.InlineKeyboardButton(f"{row[1]}", callback_data=f'user_choice_thems:{row[0]}')
                    markup.add(item)
                bot.send_message(chat_id,text,reply_markup=markup, parse_mode="Markdown")
            else :
                send_message(chat_id, 'Не удалось подгрузить темы! Выставлено автоматическая тема: Неизвестная проблема')
                buffer[chat_id].question.thema = 'Неизвестная проблема'
            change_keyboard(message, chat_id)
                    
        #elif message.text == "Отменить заявку":
        #    cancel_question(chat_id)
        if message.text == "Открытые заявки":
            fetch = db_execute_fetch(f"SELECT date, thema, (SELECT name from Users WHERE tg_id=receiver), (SELECT text FROM Status WHERE id=status), id, (SELECT emoji FROM Status WHERE id=status) FROM Questions WHERE creater={chat_id} and status=1 or status=3;")
            output=""
            emoji = str()
            if len(fetch) != 0:
                for row in fetch:
                    emoji = f"{chr(int(str(row[5]).replace('U+', '0x'), 16))}"
                    markup = types.InlineKeyboardMarkup(row_width=2)
                    if row[2]== None:
                        output = f"{emoji}{emoji}{emoji}\n*Заявка №{row[4]}*\n*Тема:* {row[1]}\n*Статус:* {row[3]}\n\n"
                    else:
                        output = f"{emoji}{emoji}{emoji}\n*Заявка №{row[4]}*\n*Тема:* {row[1]}\n*Исполнитель:* {row[2]}\n*Статус:* {row[3]}\n\n"
                    item = types.InlineKeyboardButton(f"Отменить", callback_data=f'user_check_question_cancel:{row[4]}')
                    markup.add(item)
                bot.send_message(chat_id,output,reply_markup=markup, parse_mode="Markdown")
            else:
                send_message(chat_id, "Нет открытых заявок")
    except Exception as e:
        print(f"message_handler_user: {repr(e)}")