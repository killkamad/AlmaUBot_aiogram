from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

from data.button_names.certificate_buttons import *
from data.button_names.main_menu_buttons import to_main_menu_button, send_phone_button


def keyboard_certificate_type():
    markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=1, one_time_keyboard=True)
    callback_button1 = KeyboardButton(text=military_button)
    callback_button2 = KeyboardButton(text=gcvp_button)
    callback_button3 = KeyboardButton(text=requirement_button)
    callback_button4 = KeyboardButton(text=to_main_menu_button)
    markup.add(callback_button1, callback_button2, callback_button3, callback_button4)
    return markup


def keyboard_request_send_phone():
    markup = ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    button_phone = KeyboardButton(text=send_phone_button, request_contact=True)
    markup.add(button_phone)
    return markup
