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

from db_functions import *
from config import *

def is_admin(chat_id):
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
# Этап регистрации
def insert_email(message):
    try:
        chat_id = message.chat.id
        email = str(message.text)
        email_list = email.split("@")
        if "@" not in email or len(email_list) != 2:
            send_message(message.chat.id, 'Вы указали не верный адрес электронной почты')
            bot.register_next_step_handler(message, insert_email)
            return
        buffer[chat_id].email = email
        user_registering(chat_id)
    except Exception as e:
        print(repr(e))
# Этап регистрации
def user_registering(chat_id):
    buffer[chat_id].status == ''
    db_execute(f"INSERT INTO Users(name, tg_id, company, departament, is_admin, email) VALUES('{buffer[chat_id].name}', '{chat_id}', {buffer[chat_id].company}, {buffer[chat_id].departament}, {buffer[chat_id].is_admin}, '{buffer[chat_id].email}')")
    fetch = db_execute_fetch(f"SELECT * FROM Users WHERE tg_id='{chat_id}'")
    if fetch == None:
        send_message(chat_id, "Пользователь не был зарегистрирован")
    else:
        if len(fetch) == 0:
            send_message(chat_id, "Пользователь не был зарегистрирован")
        else:
            send_message(chat_id, "Пользователь был успешно зарегистрирован! Для продолжение введите `/start`")
# Этап регистрации
def take_departament(message):
    try:
        chat_id = message.chat.id
        companys = db_execute_fetch(f"SELECT dp.id, dp.name FROM Departaments dp JOIN DepToCompanys dc ON dp.id=dc.departament WHERE dc.company={buffer[chat_id].company}")
        markup = types.InlineKeyboardMarkup(row_width=2)
        for item in companys:
            if item[0] == 0:
                continue
            item = types.InlineKeyboardButton(f"{item[1]}", callback_data=f'registering_take_departament:{item[0]}')
            markup.add(item)
        bot.send_message(chat_id,"Выберите Ваш отдел!",reply_markup=markup)
    except Exception as e:
        print(repr(e))
# Этап регистрации
def take_company(message):
    try:
        chat_id = message.chat.id
        companys = db_execute_fetch("SELECT id, name FROM Companys")
        markup = types.InlineKeyboardMarkup(row_width=2)
        for item in companys:
            if item[0] == 0:
                continue
            item = types.InlineKeyboardButton(f"{item[1]}", callback_data=f'registering_take_company:{item[0]}')
            markup.add(item)
        bot.send_message(chat_id,"Выберите Вашу компанию!",reply_markup=markup)
    except Exception as e:
        print(repr(e))
# Этап регистрации
def user_reg(message):
    try:
        chat_id = message.chat.id
        name = message.text
        name_split = str(name).split(' ')
        if len(name_split) < 3:
            send_message(message.chat.id, 'Укажите ФИО полность. Пример: Иванов Иван Иванович')
            bot.register_next_step_handler(message, user_reg)
            return
        buffer[chat_id].name = name
        take_company(message)
    except Exception as e:
        print(repr(e))
# Этап регистрации
def check_admin_key(message):
    try:
        if message.text == admin_key:
            send_message(message.chat.id, 'Валидный ключ!\nКак Вас зовут ? Напишите ФИО полностью')
            buffer[message.chat.id].is_admin = 1
            bot.register_next_step_handler(message, user_reg)
        else:
            bot.send_message(message.chat.id, 'Не валидный ключ. Напишите /start и попробуйте еще раз')
    except Exception as e:
        print(repr(e))
# Этап регистрации
def cancel_question(chat_id):
    fetch = db_execute_fetch(f"SELECT id, thema, date FROM Questions WHERE creater='{chat_id}' and status=1 or status=3;")
    markup = types.InlineKeyboardMarkup(row_width=2)
    if len(fetch) != 0:
        for row in fetch:
            item = types.InlineKeyboardButton(f"Заявка №{row[0]} - {row[1]}", callback_data=f'cancel_id:{row[0]}')
            markup.add(item)
        bot.send_message(chat_id,"Какую открытую заявку вы хотите отменить ?",reply_markup=markup)
    else:
        send_message(chat_id, f"Нет открытых заявок")

# 0 - user cancel the question
# 1 - admin take the question
# 2 - admin cancel the question
# 3 - admin finish the question
def question_alert(question_id, alert):
    request = str()
    emoji = str()
    if alert == 0:
        request = f"SELECT date, receiver, (SELECT name FROM Users WHERE tg_id=creater), (SELECT name FROM QuestionThems WHERE id=thema), createrComment, (SELECT emoji FROM Status WHERE id=status)FROM Questions WHERE id={question_id}"
    elif alert == 1:
        request = f"SELECT date, creater, (SELECT name FROM Users WHERE tg_id=receiver), (SELECT name FROM QuestionThems WHERE id=thema), (SELECT emoji FROM Status WHERE id=status) FROM Questions WHERE id={question_id}"
    elif alert == 2 or alert == 3:
        request = f"SELECT date, creater, (SELECT name FROM Users WHERE tg_id=receiver), (SELECT name FROM QuestionThems WHERE id=thema), receiverComment, (SELECT emoji FROM Status WHERE id=status) FROM Questions WHERE id={question_id}"
    fetch = db_execute_fetch(request)
    for row in fetch:
        if row[1] == 'NULL':
            return
        else:
            if alert == 0:
                # Сообщение администратору что пользователь отменил заявку
                if row[1] != None:
                    emoji = f"{chr(int(str(row[5]).replace('U+', '0x'), 16))}"
                    send_message(row[1], f"{emoji}{emoji}{emoji}\n*Пользователь* {row[2]} отменил заявку *№{question_id}* от *{row[0]}*\n*Тема:* {row[3]}\n*Описание:* \n{row[4]}")
            elif alert == 1:
                # Сообщение пользователю кто из администраторов принял заявку
                emoji = f"{chr(int(str(row[4]).replace('U+', '0x'), 16))}"
                send_message(row[1], f"{emoji}{emoji}{emoji}\n*Пользователь* {row[2]} принял заявку *№{question_id}* от *{row[0]}*\n*Тема:* {row[3]}")
            elif alert == 2:
                # Сообщение пользователю что администратор отклонил заявку
                emoji = f"{chr(int(str(row[5]).replace('U+', '0x'), 16))}"
                send_message(row[1], f"{emoji}{emoji}{emoji}\n*Пользователь* {row[2]} отменил заявку *№{question_id}* от *{row[0]}*\n*Тема:*{row[3]}\n*Комментарий:* \n{row[4]}")
            elif alert == 3:
                # Сообщение пользователю что администратор завершил заявку
                emoji = f"{chr(int(str(row[5]).replace('U+', '0x'), 16))}"
                send_message(row[1], f"{emoji}{emoji}{emoji}\n*Пользователь* {row[2]} выполнил заявку *№{question_id}* от *{row[0]}*\n*Тема:*{row[3]}\n*Комментарий:* \n{row[4]}")
    

def questions_my_view(chat_id):
    fetch = db_execute_fetch(f"SELECT id, date, thema, createrComment, (SELECT name from Users WHERE tg_id=creater), (SELECT emoji FROM Status WHERE id=status) FROM Questions WHERE status=3 AND receiver={chat_id}")
    if len(fetch) != 0:
        send_message(chat_id, "Список принятых тобой заявок")
        for row in fetch:
            emoji = f"{chr(int(str(row[5]).replace('U+', '0x'), 16))}"
            markup = types.InlineKeyboardMarkup(row_width=2)
            text = f"{emoji}{emoji}{emoji}\n*Заявка №{row[0]}*\n*Тема:* {row[2]}\n*Время создания:* {row[1]}\n*Создатель:* {row[4]}\n*Описание:*\n{row[3]}\n\n"
            item = types.InlineKeyboardButton(f"Закрыть заявку", callback_data=f'admin_done_question_id:{row[0]}')
            item2 = types.InlineKeyboardButton(f"Отказать", callback_data=f'admin_cancel_question:{row[0]}')
            markup.add(item, item2)
            bot.send_message(chat_id,text,reply_markup=markup, parse_mode="Markdown")
        
    else:
        send_message(chat_id, "Нет открытых заявок")

def admins_alert(question_id):
    fetch = db_execute_fetch(f"SELECT date, createrComment, (SELECT name FROM QuestionThems WHERE id=thema), (SELECT name FROM Users WHERE tg_id=creater), (SELECT emoji FROM Status WHERE id=status) FROM Questions WHERE id={question_id}")
    text = str()
    admin_tag = str()
    emoji = str()
    attachment = None
    if len(fetch) == 0:
        return
    for row in fetch:
        attachment = db_execute_fetch(f"SELECT * FROM QuestionFiles WHERE question_id={question_id}")
        if attachment != None:
            if len(attachment) == 0:
                attachment = 0
            else:
                attachment = len(attachment)
        else:
            attachment = 0
        emoji = f"{chr(int(str(row[4]).replace('U+', '0x'), 16))}"
        text = f" поступила заявка №{question_id} от {row[3]}\nДата создания: {row[0]}\nТема: {row[2]}\nОписание:\n{row[1]}"
        fetch2 = db_execute_fetch(f'SELECT name FROM Companys WHERE id=(SELECT company FROM Users WHERE tg_id=(SELECT creater FROM Questions WHERE id=3))')
        if len(fetch2) != 0:
            for item in fetch2:
                admin_tag = item[0]
            admin_tag +="_IT"
    if len(admin_tag) == 0:
        admin_tag == "ALL_ADMINS"

    admins = db_execute_fetch(f"SELECT u.name, u.tg_id FROM Users u JOIN MaillingUsers mu ON u.id = mu.uid  JOIN MaillingGroups mg ON mg.id = mu.group_id WHERE u.is_admin = 1 AND mg.name='{admin_tag}'")
    if len(admins) == 0:
        return
    for row in admins:
        markup = types.InlineKeyboardMarkup(row_width=2)
        item = types.InlineKeyboardButton(f"Принять", callback_data=f'admin_take_question:{question_id}')
        item2 = types.InlineKeyboardButton(f"Отказать", callback_data=f'admin_cancel_question:{question_id}')
        item3 = types.InlineKeyboardButton(f"Вложения", callback_data=f'admin_view_question_attachment:{question_id}')
        if attachment == 0:
            markup.add(item, item2)
        else:
            markup.add(item, item3, item2)
        bot.send_message(row[1],f"{emoji}{emoji}{emoji}\nПривет {row[0]}, {text}",reply_markup=markup)

def send_message (id, text):
    bot.send_message(id, text, parse_mode="Markdown")