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
from db_functions import *

def inline_handler_admin(call, chat_id):
    if call.message:       
# Принятие заявки(админ)
        if f"admin_take_question:" in call.data:
            id = str(call.data).replace(f"admin_take_question:",'')
            fetch = db_execute_fetch(f"SELECT (SELECT name FROM Users WHERE tg_id=receiver) FROM Questions WHERE id={id}")
            if len(fetch) != 0:
                for row in fetch:
                    if row[0] != None:
                        send_message(call.message.chat.id, f"*Заявку №{id}* уже принял {row[0]}")
                    else:
                        db_execute(f"UPDATE Questions SET receiver='{call.message.chat.id}', status=3 WHERE id={id}")
                        send_message(call.message.chat.id, f"Вы ***приняли*** заявку №{id}")
                        question_alert(id, 1)
            return
# Просмотр вложений
        if f"admin_view_question_attachment:" in call.data:
            id = str(call.data).replace("admin_view_question_attachment:",'')
            send_message(chat_id, f"Вложения заявки №{id}")
            photos = []
            voices = []
            documents = []
            audios = []
            videos = []
            video_notes = []
            media = []
            files = db_execute_fetch(f"SELECT fl.file_id, fl.contentType FROM Files fl JOIN QuestionFiles ql ON ql.question_id={id} WHERE fl.id=ql.fileId;")
            if files == None:
                return
            for file in files:
                content_type = file[1]
                file_id = file[0]
                if content_type == 1:
                    photos.append(file_id)
                if content_type == 2:
                    voices.append(file_id)
                if content_type == 3:
                    documents.append(file_id)
                if content_type == 4:
                    audios.append(file_id)
                if content_type == 5:
                    videos.append(file_id)
                if content_type == 6:
                    video_notes.append(file_id)
            if len(file) != 0:
                for file in photos:
                    media.append(InputMediaPhoto(media=file))
                bot.send_media_group(chat_id=chat_id, media=media)
                media.clear()
            if len(voices) != 0:
                for file in voices:
                    media.append(InputMediaAudio(media=file))
                bot.send_media_group(chat_id=chat_id, media=media)
                media.clear()
            if len(documents) != 0:
                for file in documents:
                    media.append(InputMediaDocument(media=file))
                bot.send_media_group(chat_id=chat_id, media=media)
                media.clear()
            if len(audios) != 0:
                for file in audios:
                    media.append(InputMediaAudio(media=file))
                bot.send_media_group(chat_id=chat_id, media=media)
                media.clear()
            if len(videos) != 0:
                for file in videos:
                    media.append(InputMediaVideo(media=file))
                bot.send_media_group(chat_id=chat_id, media=media)
                media.clear()
            if len(video_notes) != 0:
                for file in video_notes:
                    media.append(InputMediaVideo(media=file, supports_streaming=True))
                bot.send_media_group(chat_id=chat_id, media=media)
                media.clear()

                
# Отмена заявки(админ)
        if f"admin_cancel_question:" in call.data:
            id = str(call.data).replace(f"admin_cancel_question:",'')
            fetch = db_execute_fetch(f"SELECT status, (SELECT name FROM Users WHERE tg_id=receiver) FROM Questions WHERE id={id}")
            if len(fetch) != 0:
                for row in fetch:
                    if row[0] == 2:
                        send_message(call.message.chat.id, f"*Заявка №{id}* уже отказана пользователем {row[1]}")
                        buffer[call.message.chat.id].status = ''
                        return
            buffer[call.message.chat.id].question.id = id
            send_message(call.message.chat.id, "Напишите причину отказа")
            buffer[call.message.chat.id].status = "wait_admin_cancel_request"
            return
# Закрытие заявки(выполнено админом), закрыть с комментарием или без
        if f"admin_done_question_id:" in call.data:
            id = str(call.data).replace(f"admin_done_question_id:",'')
            fetch = db_execute_fetch(f"SELECT status FROM Questions WHERE id={id}")
            if len(fetch) != 0:
                for row in fetch:
                    if row[0] == 4:
                        send_message(call.message.chat.id, f"*Заявка №{id}* уже закрыта")
                        buffer[call.message.chat.id].status = ''
                        return
            markup = types.InlineKeyboardMarkup(row_width=2)
            item = types.InlineKeyboardButton(f"Да", callback_data=f'admin_done_question_id_yes:{id}')
            item2 = types.InlineKeyboardButton(f"Нет", callback_data=f'admin_done_question_id_no:{id}')
            markup.add(item, item2)
            bot.send_message(call.message.chat.id,"Оставишь комментарий ?",reply_markup=markup)
            return
# Закрытие заявки(выполнено админом), проверка на выбор с комментарием или без                
        if f"admin_done_question_id_" in call.data:
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="Оставишь комментарий ?")
            id = str(call.data).replace(f"admin_done_question_id_",'')
            if 'yes:' in id:
                id = id.replace(f"yes:",'')
                buffer[call.message.chat.id].question.id = id
                buffer[call.message.chat.id].status = "wait_admin_done_request"
                send_message(call.message.chat.id, 'Напиши комментарий')
                return
            else:
                id = id.replace(f"no:",'')
                fetch = db_execute_fetch(f"UPDATE Questions SET status=4, receiver='{call.message.chat.id}' WHERE id={id};")
                question_alert(id, 3)
                send_message(call.message.chat.id, f"Заявка №{id} выполнена")
            return

def message_handler_admin(message, chat_id):
    try:
        if str(chat_id) not in str(buffer.keys()):
            return
# Работа с заявками в "Мои заявки"
# Регистрация администратора
        if buffer[chat_id].status == 'wait_admin_name_insert':
            buffer[chat_id].status = ''
            db_execute(f"UPDATE Users SET name='{message.text}' WHERE tg_id='{chat_id}'")
            if is_registered(chat_id) == True:
                buffer[chat_id].status = ''
                send_message(message.chat.id, 'Регистрация администратора окончена. Напишите `/start` для продолжения.  Хорошего рабочего дня!')
                return
            else:
                send_message(message.chat.id, '*Ошибка регистрации*. Сообщите разработчику о неполадке.')
# Отмена заявки
        if buffer[chat_id].status == 'wait_admin_cancel_request':
            id = buffer[chat_id].question.id
            buffer[chat_id].status = ''
            text = message.text
            fetch = db_execute_fetch(f"UPDATE Questions SET status=2, receiver={chat_id}, receiverComment='{text}' WHERE id={id};")
            buffer[chat_id].question.id = 0
            question_alert(id, 2)
            send_message(chat_id, f"***Заявка №{id} отказана***")
            return
# Закрытие заявки
        if buffer[chat_id].status == 'wait_admin_done_request':
            id = buffer[chat_id].question.id
            buffer[chat_id].status = ''
            text = message.text
            fetch = db_execute_fetch(f"UPDATE Questions SET status=4, receiver='{chat_id}', receiverComment='{text}' WHERE id={id};")
            buffer[chat_id].question.id = 0
            question_alert(id, 3)
            send_message(chat_id, f"Заявка №{id} выполнена")
            return
# Интерфейс
        if message.text == "Просмотр заявок":
                fetch = db_execute_fetch(f"SELECT que.id, que.date, (SELECT name FROM QuestionThems WHERE id=que.thema), que.createrComment, (SELECT name from Users WHERE tg_id=creater), (SELECT text FROM Status WHERE id=status), (SELECT emoji FROM Status WHERE id=status)  FROM Questions que JOIN Users u ON company=(SELECT company FROM Users WHERE tg_id='{chat_id}') WHERE que.status=1;")
                if len(fetch) != 0:
                    for row in fetch:
                        attachment = db_execute_fetch(f"SELECT * FROM QuestionFiles WHERE question_id={row[0]}")
                        if attachment != None:
                            if len(attachment) == 0:
                                attachment = 0
                            else:
                                attachment = len(attachment)
                        else:
                            attachment = 0
                        emoji = f"{chr(int(str(row[6]).replace('U+', '0x'), 16))}"
                        markup = types.InlineKeyboardMarkup(row_width=2)
                        text = f"{emoji}{emoji}{emoji}\n*Заявка №{row[0]}*\n*Тема:* {row[2]}\n*Время создания:* {row[1]}\n*Создатель:* {row[4]}\n*Описание:*\n{row[3]}\n\n"
                        item = types.InlineKeyboardButton(f"Принять", callback_data=f'admin_take_question:{row[0]}')
                        item2 = types.InlineKeyboardButton(f"Отказать", callback_data=f'admin_cancel_question:{row[0]}')
                        item3 = types.InlineKeyboardButton(f"Вложения", callback_data=f'admin_view_question_attachment:{row[0]}')
                        if attachment == 0:
                            markup.add(item, item2)
                        else:
                            markup.add(item, item3, item2)
                        bot.send_message(chat_id,text,reply_markup=markup, parse_mode="Markdown")
                else:
                    send_message(chat_id, "Нет открытых заявок")
        if message.text == "Мои заявки":
            questions_my_view(chat_id)
    except Exception as e:
        print(repr(e))