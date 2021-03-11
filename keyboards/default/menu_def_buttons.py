from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from data.config import *


def always_stay_menu_keyboard():
    markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    markup.add(*[KeyboardButton(text=item) for item in main_menu_def_buttons])
    return markup


def keyboard_send_phone_to_register_in_db():
    markup = ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    button_phone = KeyboardButton(text="☎ Отправить номер телефона", request_contact=True)
    button_cancel = KeyboardButton(text="❌ Отмена регистрации")
    markup.add(button_phone, button_cancel)
    return markup
