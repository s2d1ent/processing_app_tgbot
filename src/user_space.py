from config import *
from users_func import *

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
        if str(chat_id) in str(user_status.keys()):
# Создание заявки, ввод темы
            if user_status[chat_id] == 'wait_user_create_question_thema':
                user_status[chat_id] = ''
                date = datetime.now().strftime("%d-%m-%Y %H:%M")
                questions_status_create = False
                text = str(message.text).replace("'","`").replace('"',"`")
                db_execute(f"INSERT INTO Questions (date, finishDate, creater, receiver, status, createrComment, receiverComment, thema) "+
                           f"VALUES ('{date}','NULL','{chat_id}','NULL', 1, 'NONE', '', '{text}')")
                questions_status_create = is_exist_question(date, chat_id, text)
                if questions_status_create == -1:
                    send_message(chat_id, "Не удалось создать заявку")                        
                else:
                    user_status[f'{chat_id}_id_thema'] = questions_status_create
                    send_message(chat_id, "Опишите свою проблемы ***(не более 500 символов)***")
                    user_status[chat_id] = 'wait_user_create_question'
                return
# Создание заявки, ввод описания                
            if user_status[chat_id] == 'wait_user_create_question':
                user_status[chat_id] = ''
                text = str(message.text).replace("'","`").replace('"',"`")
                id = user_status[f'{chat_id}_id_thema']
                thema = ''
                db_execute(f"UPDATE Questions SET createrComment='{text}' WHERE id={id}")
                fetch = db_execute_fetch(f"SELECT thema FROM Questions WHERE id={id}")
                for row in fetch:
                    thema = row[0]
                send_message(chat_id, f"*Заявка №{id}*\n*Тема:* {thema}\n*Описание:*\n{text}")
                send_message(chat_id, "***Заявка успешно создана***. По закрытию Вашей заявки я пришлю уведомление")
                admins_alert(id) 
                return
# Интерфейс
        if message.text == "Создать заявку":
            send_message(chat_id, "Тема заявки")
            user_status[chat_id] = 'wait_user_create_question_thema'
        if message.text == "Отменить заявку":
            cancel_question(chat_id)
        if message.text == "Проверить статус открытых заявок":
            fetch = db_execute_fetch(f"SELECT date, thema, (SELECT name from Users WHERE tg_id=receiver), (SELECT text FROM Status WHERE id=status), id FROM Questions WHERE creater={chat_id} and status=1 or status=3;")
            output=""
            if len(fetch) != 0:
                for row in fetch:
                    if row[2]=="NULL":
                        output += f"*Заявка №{row[4]}*\n*Тема:* {row[1]}\n*Статус:* {row[3]}\n\n"
                    else:
                        output += f"*Заявка №{row[4]}*\n*Тема:* {row[1]}\n*Исполнитель:* {row[2]}\n*Статус:* {row[3]}\n\n"
                send_message(chat_id, output)
            else:
                send_message(chat_id, "Нет открытых заявок")
    except Exception as e:
        print(f"message_handler_user: {repr(e)}")