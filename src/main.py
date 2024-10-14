from datetime import datetime
from db_functions import *
from config import *
from users_func import *
from user_space import inline_handler_user, message_handler_user
from admin_space import inline_handler_admin, message_handler_admin
from keyboards import init_keyboards, start_keyboard, change_keyboard

@bot.message_handler(commands=['start'])
def cmd_start(message):
    try:
        chat_id = message.chat.id
        user_exist = is_registered(message.chat.id)
        if user_exist == True:
            start_keyboard(chat_id)
        else:
            markup = types.InlineKeyboardMarkup(row_width=2)
            item1 = types.InlineKeyboardButton("Администратор", callback_data='whois_cmd_admin')
            item2 = types.InlineKeyboardButton("Пользователь", callback_data='whois_cmd_user')
            markup.add(item1, item2)
            bot.send_message(chat_id, 
            f'Привет, {message.from_user.first_name}!. Для начала давай разберемся кто ты.\n'+
            '`Администратор` - тот кто будет обрабатывать поступающие заявки\n'+
            '`Пользователь` - тот кто будет отправлять заявки\n',
            reply_markup=markup, parse_mode="Markdown")
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
# Проверка пользователя при регистрации(админ)
            if call.data == 'whois_cmd_admin':
                bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=f'Привет, {call.message.from_user.first_name}!. Для начала давай разберемся кто ты.\n'+
            '`Администратор` - тот кто будет обрабатывать поступающие заявки\n'+
            '`Пользователь` - тот кто будет отправлять заявки\n')
                bot.send_message(call.message.chat.id, 'Введите ключ администратора')
                bot.register_next_step_handler(call.message, check_admin_key)
# Проверка пользователя при регистрации(пользователь)
            if call.data == 'whois_cmd_user':
                bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=f'Привет, {call.message.from_user.first_name}!. Для начала давай разберемся кто ты.\n'+
            '`Администратор` - тот кто будет обрабатывать поступающие заявки\n'+
            '`Пользователь` - тот кто будет отправлять заявки\n')
                bot.send_message(call.message.chat.id, 'Как тебя зовут ?')
                bot.register_next_step_handler(call.message, user_reg)
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

            keyboard_changed = change_keyboard(message, chat_id)
            if keyboard_changed == True:
                return
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

# TODO
@bot.message_handler(content_types=['photo'])
def photo_handler(message):
    #for photo in message.photo:
    #    bot.send_photo(message.chat.id, photo.file_id)
    #    break
    None

        


if __name__ == '__main__':
    init_keyboards()
    try:
        bot.polling(none_stop=True)
    except Exception as e:
        bot.polling(none_stop=True)