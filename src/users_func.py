from db_functions import *
from config import *

def get_user_type(chat_id):
    user_type = -1
    # 0 - user
    # 1 - admin
    request = db_execute_fetch(f"select * from Users where tg_id='{chat_id}'")
    if len(request) != 0:
        for row in request:
            if row[3] == 0:
                user_type = 0
            else:
                user_type = 1
    return user_type

def user_reg(message):
    try:
        db_execute(f"INSERT INTO Users (name, tg_id) VALUES ('{message.text}','{message.chat.id}')") 
        if is_registered(message.chat.id):
           send_message(message.chat.id, "Регистрация пользователя прошла успешно! Напишите `/start` для продолжения. Хорошего рабочего дня!")
        else:
           send_message(message.chat.id, "Пользователь не был зарегистрирован! Сообщите об ошибке разработчику!")
    except Exception as e:
        print(repr(e))

def check_admin_key(message):
    try:
        if message.text == admin_key:
            send_message(message.chat.id, 'Валидный ключ.\nДалее нам нужно записать информацию о тебе.\nКак тебя зовут ?')
            db_execute(f"INSERT INTO Users (name, tg_id, is_admin) VALUES ('NONE','{message.chat.id}', 1)")
            user_status[message.chat.id] = 'wait_admin_name_insert'
        else:
            bot.send_message(message.chat.id, 'Не валидный ключ. Напишите /start и попробуйте еще раз')
    except Exception as e:
        print(repr(e))

def cancel_question(chat_id):
    fetch = db_execute_fetch(f"SELECT id, thema, date FROM Questions WHERE creater='{chat_id}' and status=1 or status=3;")
    markup = types.InlineKeyboardMarkup(row_width=2)
    if len(fetch) != 0:
        for row in fetch:
            item = types.InlineKeyboardButton(f"Заявка №{row[0]} - {row[1]}", callback_data=f'{chat_id}_cancel_id:{row[0]}')
            markup.add(item)
        bot.send_message(chat_id,"какая конкретно заявка тебя интересует ?",reply_markup=markup)
    else:
        send_message(chat_id, f"Нет открытых заявок")

# 0 - user cancel the question
# 1 - admin take the question
# 2 - admin cancel the question
# 3 - admin finish the question
def question_alert(question_id, alert):
    request = str()
    if alert == 0:
        request = f"SELECT date, receiver, (SELECT name FROM Users WHERE tg_id=creater), thema, createrComment FROM Questions WHERE id={question_id}"
    elif alert == 1:
        request = f"SELECT date, creater, (SELECT name FROM Users WHERE tg_id=receiver), thema FROM Questions WHERE id={question_id}"
    elif alert == 2 or alert == 3:
        request = f"SELECT date, creater, (SELECT name FROM Users WHERE tg_id=receiver), thema, receiverComment FROM Questions WHERE id={question_id}"
    fetch = db_execute_fetch(request)
    for row in fetch:
        if row[1] == 'NULL':
            return
        else:
            if alert == 0:
                # send to adnib what user cancel the question
                send_message(row[1], f"*Пользователь* {row[2]} отменил заявку *№{question_id}* от *{row[0]}*\n*Тема:* {row[3]}\n*Описание:* \n{row[4]}")
            elif alert == 1:
                # send to creater what admin take the question
                send_message(row[1], f"*Пользователь* {row[2]} принял заявку *№{question_id}* от *{row[0]}*\n*Тема:* {row[3]}")
            elif alert == 2:
                # send to creater what admin cancel the question
                send_message(row[1], f"*Пользователь* {row[2]} отменил заявку *№{question_id}* от *{row[0]}*\n*Тема:*{row[3]}\n*Комментарий:* \n{row[4]}")
            elif alert == 3:
                # send to creater what admin cancel the question
                send_message(row[1], f"*Пользователь* {row[2]} выполнил заявку *№{question_id}* от *{row[0]}*\n*Тема:*{row[3]}\n*Комментарий:* \n{row[4]}")

def questions_view(chat_id):
    fetch = db_execute_fetch("SELECT id, date, thema, createrComment, (SELECT name from Users WHERE tg_id=creater), (SELECT text FROM Status WHERE id=status) FROM Questions WHERE status=1")
    if len(fetch) != 0:
        for row in fetch:
            markup = types.InlineKeyboardMarkup(row_width=2)
            text = f"*Заявка №{row[0]}*\n*Тема:* {row[2]}\n*Время создания:* {row[1]}\n*Создатель:* {row[4]}\n*Описание:*\n{row[3]}\n\n"
            item = types.InlineKeyboardButton(f"Принять", callback_data=f'{chat_id}_admin_take_question:{row[0]}')
            item2 = types.InlineKeyboardButton(f"Отказать", callback_data=f'{chat_id}_admin_cancel_question:{row[0]}')
            markup.add(item, item2)
            bot.send_message(chat_id,text,reply_markup=markup, parse_mode="Markdown")
        
    else:
        send_message(chat_id, "Нет открытых заявок")

def questions_my_view(chat_id):
    fetch = db_execute_fetch(f"SELECT id, date, thema, createrComment, (SELECT name from Users WHERE tg_id=creater) FROM Questions WHERE status=3 AND receiver={chat_id}")
    if len(fetch) != 0:
        send_message(chat_id, "Список принятых тобой заявок")
        for row in fetch:
            markup = types.InlineKeyboardMarkup(row_width=2)
            text = f"*Заявка №{row[0]}*\n*Тема:* {row[2]}\n*Время создания:* {row[1]}\n*Создатель:* {row[4]}\n*Описание:*\n{row[3]}\n\n"
            item = types.InlineKeyboardButton(f"Закрыть заявку", callback_data=f'{chat_id}_admin_done_question_id:{row[0]}')
            item2 = types.InlineKeyboardButton(f"Отказать", callback_data=f'{chat_id}_admin_cancel_question:{row[0]}')
            markup.add(item, item2)
            bot.send_message(chat_id,text,reply_markup=markup, parse_mode="Markdown")
        
    else:
        send_message(chat_id, "Нет открытых заявок")

def admins_alert(question_id):
    fetch = db_execute_fetch(f"SELECT date, createrComment, thema, (SELECT name FROM Users WHERE tg_id=creater) FROM Questions WHERE id={question_id}")
    admins = db_execute_fetch("SELECT name, tg_id FROM Users WHERE is_admin=1")
    text = str()
    if len(fetch) == 0:
        return
    if len(admins) == 0:
        return
    for row in fetch:
        text = f" поступила заявка №{question_id} от {row[3]}\nДата создания: {row[0]}\nТема: {row[2]}\nОписание:\n{row[1]}"
    for row in admins:
        markup = types.InlineKeyboardMarkup(row_width=2)
        item = types.InlineKeyboardButton(f"Принять", callback_data=f'{row[1]}_admin_take_question:{question_id}')
        item2 = types.InlineKeyboardButton(f"Отказать", callback_data=f'{row[1]}_admin_cancel_question:{question_id}')
        markup.add(item, item2)
        bot.send_message(row[1],f"Привет {row[0]}, {text}",reply_markup=markup)

def send_message (id, text):
    bot.send_message(id, text, parse_mode="Markdown")