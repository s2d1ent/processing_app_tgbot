from config import *
from users_func import is_admin
user_keyboard_buf = {}
# user
user_std_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True,one_time_keyboard=False)
user_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True,one_time_keyboard=False)
user_config_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True,one_time_keyboard=False)
# admin
admin_std_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True,one_time_keyboard=False)
admin_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True,one_time_keyboard=False)
admin_config_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True,one_time_keyboard=False)
admin_mailling_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True,one_time_keyboard=False)


def start_keyboard(chat_id):
    user_type = is_admin(chat_id)
    if user_type == 0:
        user_keyboard_buf[chat_id] = 'user_std_keyboard'
        bot.send_message(chat_id,"Продолжаем работать",reply_markup=user_std_keyboard)
    elif user_type == 1:
        user_keyboard_buf[chat_id] = 'admin_std_keyboard'
        bot.send_message(chat_id,"Продолжаем работать",reply_markup=admin_std_keyboard)

def change_keyboard(message, chat_id):
    try:
        result = False
        user_privelegies = is_admin(chat_id)
        buf_value = None
        if str(chat_id) not in str(user_keyboard_buf.keys()):
            print('Not user key in distinct')
            return
        buf_value = user_keyboard_buf[chat_id]
        if message.text == 'Назад':
            if user_privelegies  == 0:
                if buf_value == 'user_std_keyboard':
                    bot.send_message(chat_id,"Назад!",reply_markup=user_std_keyboard)
                    user_keyboard_buf[chat_id] = 'user_std_keyboard'
                    result = True
                if buf_value == 'user_keyboard':
                    bot.send_message(chat_id,"Назад!",reply_markup=user_std_keyboard)
                    user_keyboard_buf[chat_id] = 'user_std_keyboard'
                    result = True
                if buf_value == 'user_config_keyboard':
                    bot.send_message(chat_id,"Назад!",reply_markup=user_std_keyboard)
                    user_keyboard_buf[chat_id] = 'user_std_keyboard'
                    result = True
            elif user_privelegies == 1:
                if buf_value == 'admin_std_keyboard':
                    bot.send_message(chat_id,"Назад!",reply_markup=admin_std_keyboard)
                    user_keyboard_buf[chat_id] = 'admin_std_keyboard'
                    result = True
                if buf_value == 'admin_keyboard':
                    bot.send_message(chat_id,"Назад!",reply_markup=admin_std_keyboard)
                    user_keyboard_buf[chat_id] = 'admin_std_keyboard'
                    result = True
                if buf_value == 'admin_config_keyboard':
                    bot.send_message(chat_id,"Назад!",reply_markup=admin_std_keyboard)
                    user_keyboard_buf[chat_id] = 'admin_std_keyboard'
                    result = True
                if buf_value == 'admin_mailling_keyboard':
                    bot.send_message(chat_id,"Назад!",reply_markup=admin_std_keyboard)
                    user_keyboard_buf[chat_id] = 'admin_std_keyboard'
                    result = True
                    
        elif message.text == 'Заявки':
            if user_privelegies  == 0:
                if buf_value == 'user_std_keyboard':
                    bot.send_message(chat_id,"Заявки!",reply_markup=user_keyboard)
                    user_keyboard_buf[chat_id] = 'user_keyboard'
                    result = True
            elif user_privelegies == 1:
                if buf_value == 'admin_std_keyboard':
                    bot.send_message(chat_id,"Заявки!",reply_markup=admin_keyboard)
                    user_keyboard_buf[chat_id] = 'admin_keyboard'
                    result = True
        elif message.text == 'Настройки':
            if user_privelegies  == 0:
                if buf_value == 'user_std_keyboard':
                    bot.send_message(chat_id,"Заявки!",reply_markup=user_config_keyboard)
                    user_keyboard_buf[chat_id] = 'user_config_keyboard'
                    result = True
            elif user_privelegies == 1:
                if buf_value == 'admin_std_keyboard':
                    bot.send_message(chat_id,"Заявки!",reply_markup=admin_config_keyboard)
                    user_keyboard_buf[chat_id] = 'admin_config_keyboard'
                    result = True
        elif message.text == 'Рассылка':
            if user_privelegies == 1:
                if buf_value == 'admin_std_keyboard':
                    bot.send_message(chat_id,"Заявки!",reply_markup=admin_mailling_keyboard)
                    user_keyboard_buf[chat_id] = 'admin_mailling_keyboard'
                    result = True

        return result
    except Exception as e:
        print(repr(e))

def init_keyboards():
    # Открывает user_keyboard
    ustd_btn1 = types.KeyboardButton("Заявки")
    # user_config_keyboard
    ustd_btn2 = types.KeyboardButton("Настройки")
    user_std_keyboard.add(ustd_btn1, ustd_btn2)
    
    # Открывает admin_keyboard
    astd_btn1 = types.KeyboardButton("Заявки")
    # admin_mailling_keyboard
    astd_btn2 = types.KeyboardButton("Рассылка")
    # admin_config_keyboard
    astd_btn3 = types.KeyboardButton("Настройки")
    admin_std_keyboard.add(astd_btn1, astd_btn2, astd_btn3)

    # Рассылка
    amaill_btn1 = types.KeyboardButton("Разослать уведомление")
    amaill_btn2 = types.KeyboardButton("Назад")
    admin_mailling_keyboard.add(amaill_btn1, amaill_btn2)
    # Конец рассылка

    # настройки
    ucfg_btn1 = types.KeyboardButton("Сменить имя пользователя")
    ucfg_btn2 = types.KeyboardButton("Сменить предприятие")
    ucfg_btn3 = types.KeyboardButton("Назад")
    user_config_keyboard.add(ucfg_btn1, ucfg_btn2, ucfg_btn3)

    acfg_btn1 = types.KeyboardButton("Сменить имя пользователя")
    acfg_btn2 = types.KeyboardButton("Сменить предприятие")
    acfg_btn2 = types.KeyboardButton("Управление БД")
    acfg_btn3 = types.KeyboardButton("Назад")
    admin_config_keyboard.add(acfg_btn1, acfg_btn2, acfg_btn3)
    # Конец настройки

    # Заявки
    user_btn1 = types.KeyboardButton("Создать заявку")
    user_btn2 = types.KeyboardButton("Проверить статус открытых заявок")
    user_btn3 = types.KeyboardButton("Отменить заявку")
    user_btn4 = types.KeyboardButton("Назад")
    user_keyboard.add(user_btn1, user_btn3, user_btn2, user_btn4)

    admin_btn1 = types.KeyboardButton("Просмотр заявок")
    admin_btn2 = types.KeyboardButton("Мои заявки")
    admin_btn3 = types.KeyboardButton("Назад")
    admin_keyboard.add(admin_btn1, admin_btn2, admin_btn3)
    # Конец заявки
    print("Keybord initialized")