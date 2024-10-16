from config import *
from users_func import *
from keyboard import change_keyboard

def inline_handler_user(call, chat_id):
    if call.message:
# Отмена заявки(Пользователь)
        if f"{call.message.chat.id}_cancel_id:" in call.data:
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="какая конкретно заявка тебя интересует ?")
            id = str(call.data).replace(f"{call.message.chat.id}_cancel_id:",'')
            db_execute(f"UPDATE Questions SET status=2 WHERE id={id}")
            send_message(call.message.chat.id, f"***Ваша заявка №{id} отменена***")
            question_alert(id, 0)
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
            if buffer[chat_id].status == 'user_mode_create_question_comment':
                buffer[chat_id].status = 'user_mode_create_question'
                send_message(chat_id, f"ВРЕМЕННО НЕ РАБОТАЕТ")
                return
            if buffer[chat_id].status == 'user_mode_create_question':

                if message.text == "Изменить тему":
                    buffer[chat_id].status = 'user_mode_create_question_thema'
                    send_message(chat_id, f"Введите тему")
                    return
                if message.text == "Изменить комменатрий":
                    buffer[chat_id].status = 'user_mode_create_question_comment'
                    return
                if message.text == "Вложения":
                    buffer[chat_id].status = 'user_mode_create_question_attachment'
                    change_keyboard(message, chat_id)
                    return

                buffer[chat_id].question.description += message.text
                return
# Создание заявки, ввод описания                
            #if buffer[chat_id].status == 'wait_user_create_question':
            #    buffer[chat_id].status = ''
            #    text = str(message.text).replace("'","`").replace('"',"`")
            #    id = user_status[f'{chat_id}_id_thema']
            #    thema = ''
            #    db_execute(f"UPDATE Questions SET createrComment='{text}' WHERE id={id}")
            #    fetch = db_execute_fetch(f"SELECT thema, (SELECT emoji from Status WHERE id=status) FROM Questions WHERE id={id}")
            #    for row in fetch:
            #        thema = row[0]
            #    send_message(chat_id, f"*Заявка №{id}*\n*Тема:* {thema}\n*Описание:*\n{text}")
            #    send_message(chat_id, "***Заявка успешно создана***. По закрытию Вашей заявки я пришлю уведомление")
            #    admins_alert(id) 
            #    return
# Интерфейс
        #if message.text == "Создать заявку":
        #    send_message(chat_id, "Тема заявки")
        #    buffer[chat_id].status = 'wait_user_create_question_thema'
        if message.text == "Отменить заявку":
            cancel_question(chat_id)
        if message.text == "Проверить статус открытых заявок":
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