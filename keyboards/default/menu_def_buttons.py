from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


def always_stay_keyboard():
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    menu = KeyboardButton(text='🏠 Меню')
    # help_c = KeyboardButton(text='❓ Помощь')
    about = KeyboardButton(text='💻 О боте')
    markup.add(menu, about)
    return markup


def keyboard_send_phone_to_register_in_db():
    markup = ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    button_phone = KeyboardButton(text="☎ Отправить номер телефона", request_contact=True)
    markup.add(button_phone)
    return markup
