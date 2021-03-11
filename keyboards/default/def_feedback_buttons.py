from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from data.config import feedback_advisor_button


def keyboard_feedback():
    markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=1, one_time_keyboard=True)
    callback_button1 = KeyboardButton(text=feedback_advisor_button)
    callback_button2 = KeyboardButton(text="⬅ В главное меню")
    markup.add(callback_button1, callback_button2)
    return markup


def keyboard_feedback_send_phone():
    markup = ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    button_phone = KeyboardButton(text="☎ Отправить номер телефона", request_contact=True)
    markup.add(button_phone)
    return markup
