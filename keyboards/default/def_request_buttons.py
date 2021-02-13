from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


def keyboard_certificate_type():
    markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    callback_button1 = KeyboardButton(text="Справка в военкомат")
    callback_button2 = KeyboardButton(text="Справка ГЦВП")
    callback_button3 = KeyboardButton(text="Справка по месту требования")
    callback_button4 = KeyboardButton(text="⬅ В главное меню")
    markup.add(callback_button1, callback_button2, callback_button3)
    return markup


def keyboard_request_send_phone():
    markup = ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    button_phone = KeyboardButton(text="☎ Отправить номер телефона", request_contact=True)
    markup.add(button_phone)
    return markup
