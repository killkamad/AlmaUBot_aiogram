from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


def keyboard_feedback():
    markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    callback_button1 = KeyboardButton(text="Написать письмо ректору")
    callback_button2 = KeyboardButton(text="⬅ В главное меню")
    markup.add(callback_button1, callback_button2)
    return markup

def keyboard_feedback_send_phone():
    markup = ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    button_phone = KeyboardButton(text="☎ Отправить номер телефона", request_contact=True)
    markup.add(button_phone)
    return markup
