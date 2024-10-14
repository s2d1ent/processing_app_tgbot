from config import *
from users_func import *
from db_functions import *

def inline_handler_admin(call, chat_id):
    if call.message:       
# Принятие заявки(админ)
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
            return
# Отмена заявки(админ)
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
            return
# Закрытие заявки(выполнено админом), закрыть с комментарием или без
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
            return
# Закрытие заявки(выполнено админом), проверка на выбор с комментарием или без                
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
            return

def message_handler_admin(message, chat_id):
    try:
# Обработка заявок
        if str(chat_id) in str(user_status.keys()):
# Работа с заявками в "Мои заявки"
# Регистрация администратора
            if user_status[chat_id] == 'wait_admin_name_insert':
                user_status[chat_id] = ''
                db_execute(f"UPDATE Users SET name='{message.text}' WHERE tg_id='{chat_id}'")
                if is_registered(chat_id) == True:
                    user_status[chat_id] = ''
                    send_message(message.chat.id, 'Регистрация администратора окончена. Напишите `/start` для продолжения.  Хорошего рабочего дня!')
                    return
                else:
                    send_message(message.chat.id, '*Ошибка регистрации*. Сообщите разработчику о неполадке.')
# Отмена заявки
            if user_status[chat_id] == 'wait_admin_cancel_request':
                id = user_status[f"{chat_id}_cancel_question_id"]
                user_status[chat_id] = ''
                text = message.text
                fetch = db_execute_fetch(f"UPDATE Questions SET status=2, receiver={chat_id}, receiverComment='{text}' WHERE id={id};")
                question_alert(id, 2)
                send_message(chat_id, f"***Заявка №{id} отказана***")
                return
# Закрытие заявки
            if user_status[chat_id] == 'wait_admin_done_request':
                id = user_status[f"{chat_id}_done_question_id"]
                user_status[chat_id] = ''
                text = message.text
                fetch = db_execute_fetch(f"UPDATE Questions SET status=4, receiver='{chat_id}, receiverComment=''{text}' WHERE id={id};")
                question_alert(id, 3)
                send_message(chat_id, f"Заявка №{id} выполнена")
                return
# Интерфейс
        if message.text == "Просмотр заявок":
                questions_view(chat_id)
        if message.text == "Мои заявки":
            questions_my_view(chat_id)
    except Exception as e:
        print(repr(e))