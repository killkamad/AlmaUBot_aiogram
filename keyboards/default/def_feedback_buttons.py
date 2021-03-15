from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from data.button_names.feedback_buttons import feedback_advisor_button
from data.button_names.main_menu_buttons import to_main_menu_button, send_phone_button


def keyboard_feedback():
    markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=1, one_time_keyboard=True)
    callback_button1 = KeyboardButton(text=feedback_advisor_button)
    callback_button2 = KeyboardButton(text=to_main_menu_button)
    markup.add(callback_button1, callback_button2)
    return markup


def keyboard_feedback_send_phone():
    markup = ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    button_phone = KeyboardButton(text=send_phone_button, request_contact=True)
    markup.add(button_phone)
    return markup
