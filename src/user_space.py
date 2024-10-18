from config import *
from functions import *
from keyboards import change_keyboard
from datetime import datetime

def inline_handler_user(call, chat_id):
    if call.message:
# Отмена заявки(Пользователь)
        if f"{call.message.chat.id}_cancel_id:" in call.data:
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="Какая конкретно заявка тебя интересует ?")
            id = str(call.data).replace(f"{call.message.chat.id}_cancel_id:",'')
            db_execute(f"UPDATE Questions SET status=2 WHERE id={id}")
            send_message(call.message.chat.id, f"***Ваша заявка №{id} отменена***")
            question_alert(id, 0)
            return
# Выбор темы
        if f'{chat_id}_user_choice_thems:' in call.data:
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="Какая тема вашей заявки ?")
            id = str(call.data).replace(f"{call.message.chat.id}_user_choice_thems:",'')
            buffer[chat_id].question.thema = id
            fetch = db_execute_fetch(f"SELECT name FROM QuestionThems WHERE id={id}")
            if len(fetch) != 0:
                for row in fetch:
                    send_message(chat_id, f"Вы выбрали тему: ***{row[0]}***")
            return
        

def message_handler_user(message, chat_id):
    try:
# Обработка запросов
        if str(chat_id) in str(buffer.keys()):
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
                            item = types.InlineKeyboardButton(f"{row[1]}", callback_data=f'{chat_id}_user_choice_thems:{row[0]}')
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
                    #buffer[chat_id].status = 'user_mode_create_question_attachment'
                    #change_keyboard(message, chat_id)
                    return
                elif message.text == "Отменить":
                    change_keyboard(message, chat_id)
                    return
                elif message.text == "Закончить":
                    if buffer[chat_id].question.description == '' or buffer[chat_id].question.thema == -1:
                        send_message(chat_id, f"Вы не можете закончить написание заявки если у Вас нет описания проблемы и выбраннолй темы")
                        return
                    else:
                        date = datetime.now().strftime("%d.%m.%Y %H:%M")
                        comm = str(buffer[chat_id].question.description)
                        comm = comm.replace("'","`").replace("\"","`")
                        thema = buffer[chat_id].question.thema
                        db_execute(f"INSERT INTO Questions(date, creater, createrComment, thema) VALUES('{date}', '{chat_id}', '{comm}', {thema})")

                        fetch = db_execute_fetch(f"SELECT * FROM Questions WHERE date='{date}' and creater='{chat_id}' and thema={thema}")
                        if len(fetch) == 0:
                            send_message(chat_id, "Не удалось создать заявку")
                        else:
                            send_message(chat_id, "Заявка успешно создана")
                            buffer[chat_id].question.thema = -1
                            buffer[chat_id].question.description = ''
                            buffer[chat_id].question.files.clear()
                            #
                            # todo уведомление администратора предприятия
                            #
                        return
                buffer[chat_id].question.description += message.text + '\n'
                print(buffer[chat_id].question.description)
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
                    item = types.InlineKeyboardButton(f"{row[1]}", callback_data=f'{chat_id}_user_choice_thems:{row[0]}')
                    markup.add(item)
                bot.send_message(chat_id,text,reply_markup=markup, parse_mode="Markdown")
            else :
                send_message(chat_id, 'Не удалось подгрузить темы! Выставлено автоматическая тема: Неизвестная проблема')
                buffer[chat_id].question.thema = 'Неизвестная проблема'
            change_keyboard(message, chat_id)
                    
        elif message.text == "Отменить заявку":
            cancel_question(chat_id)
        if message.text == "Открытые заявки":
            fetch = db_execute_fetch(f"SELECT date, thema, (SELECT name from Users WHERE tg_id=receiver), (SELECT text FROM Status WHERE id=status), id, (SELECT emoji FROM Status WHERE id=status) FROM Questions WHERE creater={chat_id} and status=1 or status=3;")
            output=""
            if len(fetch) != 0:
                for row in fetch:
                    if row[2]== None:
                        output += f"*Заявка №{row[4]}*\n*Тема:* {row[1]}\n*Статус:* {row[3]}\n\n"
                    else:
                        output += f"*Заявка №{row[4]}*\n*Тема:* {row[1]}\n*Исполнитель:* {row[2]}\n*Статус:* {row[3]}\n\n"
                send_message(chat_id, output)
            else:
                send_message(chat_id, "Нет открытых заявок")
    except Exception as e:
        print(f"message_handler_user: {repr(e)}")