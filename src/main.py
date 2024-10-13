from datetime import datetime
from db_functions import *
from config import *
from users_func import *

@bot.message_handler(commands=['start'])
def cmd_start(message):
    try:
        chat_id = message.chat.id
        user_exist = is_registered(message.chat.id)
        if user_exist == True:
            spawn_keyboard(chat_id)
            user_type = get_user_type(chat_id)
            if user_type == 0:
                bot.send_message(chat_id,"Продолжаем работать",reply_markup=user_keyboard)
            elif user_type == 1:
                bot.send_message(chat_id,"Продолжаем работать",reply_markup=admin_keyboard)
        else:
            markup = types.InlineKeyboardMarkup(row_width=2)
            item1 = types.InlineKeyboardButton("Администратор", callback_data='whois_cmd_admin')
            item2 = types.InlineKeyboardButton("Пользователь", callback_data='whois_cmd_user')
            markup.add(item1, item2)
            bot.send_message(chat_id, 
            f'Привет, {message.from_user.first_name}!. Для начала давай разберемся кто ты.\n'+
            '`Администратор` - тот кто будет обрабатывать поступающие заявки\n'+
            '`Пользователь` - тот кто будет отправлять заявки\n',
            reply_markup=markup)
    except Exception as e:
        print(repr(e))

@bot.callback_query_handler(func=lambda call: True)
def inline_handler(call):
    try:
        if call.message:
            if call.data == 'whois_cmd_admin':
                bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=f'Привет, {call.message.from_user.first_name}!. Для начала давай разберемся кто ты.\n'+
            '`Администратор` - тот кто будет обрабатывать поступающие заявки\n'+
            '`Пользователь` - тот кто будет отправлять заявки\n')
                bot.send_message(call.message.chat.id, 'Введите ключ администратора')
                bot.register_next_step_handler(call.message, check_admin_key)
            if call.data == 'whois_cmd_user':
                bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=f'Привет, {call.message.from_user.first_name}!. Для начала давай разберемся кто ты.\n'+
            '`Администратор` - тот кто будет обрабатывать поступающие заявки\n'+
            '`Пользователь` - тот кто будет отправлять заявки\n')
                bot.send_message(call.message.chat.id, 'Как тебя зовут ?')
                bot.register_next_step_handler(call.message, user_reg)

            if f"{call.message.chat.id}_cancel_id:" in call.data:
                bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="какая конкретно заявка тебя интересует ?")
                id = str(call.data).replace(f"{call.message.chat.id}_cancel_id:",'')
                db_execute(f"UPDATE Questions SET status=2 WHERE id={id}")
                send_message(call.message.chat.id, f"Ваша заявка ***отменена***")
                question_alert(id, 0)

            if f"{call.message.chat.id}_admin_take_question:" in call.data:
                id = str(call.data).replace(f"{call.message.chat.id}_admin_take_question:",'')
                fetch = db_execute_fetch(f"SELECT (SELECT name FROM Users WHERE tg_id=receiver) FROM Questions WHERE id={id}")
                if len(fetch) != 0:
                    for row in fetch:
                        if row[0] != None:
                            send_message(call.message.chat.id, f"*Заявку №{id}* уже принял {row[0]}")
                        else:
                            db_execute(f"UPDATE Questions SET receiver='{call.message.chat.id}', status=3 WHERE id={id}")
                            send_message(call.message.chat.id, f"Вы ***приняли*** заявку №{id}")
                            question_alert(id, 1)

            if f"{call.message.chat.id}_admin_cancel_question:" in call.data:
                id = str(call.data).replace(f"{call.message.chat.id}_admin_cancel_question:",'')
                fetch = db_execute_fetch(f"SELECT status, (SELECT name FROM Users WHERE tg_id=receiver) FROM Questions WHERE id={id}")
                if len(fetch) != 0:
                    for row in fetch:
                        if row[0] == 2:
                            send_message(call.message.chat.id, f"*Заявка №{id}* уже отказана пользователем {row[1]}")
                            user_status[call.message.chat.id] = ''
                            return
                user_status[f"{call.message.chat.id}_cancel_question_id"] = id
                send_message(call.message.chat.id, "Напишите причину отказа")
                user_status[call.message.chat.id] = "wait_admin_cancel_request"

            if f"{call.message.chat.id}_admin_done_question_id:" in call.data:
                id = str(call.data).replace(f"{call.message.chat.id}_admin_done_question_id:",'')
                fetch = db_execute_fetch(f"SELECT status FROM Questions WHERE id={id}")
                if len(fetch) != 0:
                    for row in fetch:
                        if row[0] == 4:
                            send_message(call.message.chat.id, f"*Заявка №{id}* уже закрыта")
                            user_status[call.message.chat.id] = ''
                            return
                markup = types.InlineKeyboardMarkup(row_width=2)
                item = types.InlineKeyboardButton(f"Да", callback_data=f'{call.message.chat.id}_admin_done_question_id_yes:{id}')
                item2 = types.InlineKeyboardButton(f"Нет", callback_data=f'{call.message.chat.id}_admin_done_question_id_no:{id}')
                markup.add(item, item2)
                bot.send_message(call.message.chat.id,"Оставишь комментарий ?",reply_markup=markup)
                
            if f"{call.message.chat.id}_admin_done_question_id_" in call.data:
                bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="Оставишь комментарий ?")
                id = str(call.data).replace(f"{call.message.chat.id}_admin_done_question_id_",'')
                if 'yes:' in id:
                    id = id.replace(f"yes:",'')
                    user_status[f"{call.message.chat.id}_done_question_id"] = id
                    user_status[call.message.chat.id] = "wait_admin_done_request"
                    send_message(call.message.chat.id, 'Напиши комментарий')
                    return
                else:
                    id = id.replace(f"no:",'')
                    fetch = db_execute_fetch(f"UPDATE Questions SET status=4, receiver='{call.message.chat.id}' WHERE id={id};")
                    question_alert(id, 3)
                    send_message(call.message.chat.id, f"Заявка №{id} выполнена")
                
    except Exception as e:
        print(repr(e))
    finally:
        spawn_keyboard(call.message.chat.id)

@bot.message_handler(func=lambda message: True)
def message_handler(message):
    try:
        if message.chat.type == 'private':
            chat_id = message.chat.id
            if str(chat_id) in str(user_status.keys()):
                if user_status[chat_id] == 'wait_admin_name_insert':
                    user_status[chat_id] = ''
                    db_execute(f"UPDATE Users SET name='{message.text}' WHERE tg_id='{chat_id}'")
                    if is_registered(chat_id) == True:
                        user_status[chat_id] = ''
                        send_message(message.chat.id, 'Регистрация администратора окончена. Напишите `/start` для продолжения.  Хорошего рабочего дня!')
                        return
                    else:
                        send_message(message.chat.id, '*Ошибка регистрации*. Сообщите разработчику о неполадке.')
               
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
                        send_message(chat_id, "Опишите свою проблемы***(не более 500 символов)***")
                        user_status[chat_id] = 'wait_user_create_question'
                    return
                
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

                if user_status[chat_id] == 'wait_admin_cancel_request':
                    id = user_status[f"{chat_id}_cancel_question_id"]
                    user_status[chat_id] = ''
                    text = message.text
                    fetch = db_execute_fetch(f"UPDATE Questions SET status=2, receiver={chat_id}, receiverComment='{text}' WHERE id={id};")
                    question_alert(id, 2)
                    send_message(chat_id, f"***Заявка №{id} отказана***")
                
                if user_status[chat_id] == 'wait_admin_done_request':
                    id = user_status[f"{chat_id}_done_question_id"]
                    user_status[chat_id] = ''
                    text = message.text
                    fetch = db_execute_fetch(f"UPDATE Questions SET status=4, receiver='{chat_id}, receiverComment=''{text}' WHERE id={id};")
                    question_alert(id, 3)
                    send_message(chat_id, f"Заявка №{id} выполнена")

            if message.text == "Просмотр заявок":
                questions_view(chat_id)
            if message.text == "Мои заявки":
                questions_my_view(chat_id)
            if message.text == "Создать заявку":
                send_message(chat_id, "Тема заявки")
                user_status[chat_id] = 'wait_user_create_question_thema'
            if message.text == "Отменить заявку":
                send_message(chat_id, "Какую открытую заявку вы хотите отменить ?")
                cancel_question(chat_id)
            if message.text == "Проверить статус открытых заявок":
                fetch = db_execute_fetch(f"SELECT date, thema, (SELECT name from Users WHERE tg_id=receiver), (SELECT text FROM Status WHERE id=status), id FROM Questions WHERE creater={chat_id} and status=1 or status=3;")
                output=""
                if len(fetch) != 0:
                    for row in fetch:
                        if row[2]=="NULL":
                            output += f"*Заявка №{row[4]}*\n*Тема:* {row[1]}\n*Статус:* {row[3]}\n\n"
                        else:
                            output += f"*Заявка №{row[4]}*\n*Тема:* {row[1]}\n*Исполнитель:* {row[2]} *Статус:* {row[3]}\n\n"
                    send_message(chat_id, output)
                else:
                    send_message(chat_id, "Нет открытых заявок")
        else:
            send_message(message.chat.id, 'Do not work')
    except Exception as e:
        print("message_handler " + repr(e))
    finally:
        spawn_keyboard(message.chat.id)

def spawn_keyboard(chat_id):
    None

if __name__ == '__main__':
    user_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True,one_time_keyboard=False)
    user_btn1 = types.KeyboardButton("Создать заявку")
    user_btn2 = types.KeyboardButton("Проверить статус открытых заявок")
    user_btn3 = types.KeyboardButton("Отменить заявку")
    user_keyboard.add(user_btn1, user_btn3, user_btn2)

    admin_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True,one_time_keyboard=False)
    admin_btn1 = types.KeyboardButton("Просмотр заявок")
    admin_btn2 = types.KeyboardButton("Мои заявки")
    admin_keyboard.add(admin_btn1, admin_btn2)
    try:
        bot.polling(none_stop=True)
    except Exception as e:
        bot.polling(none_stop=True)