from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from data.button_names.main_menu_buttons import main_menu_def_buttons, send_phone_button, cancel_reg_button


def always_stay_menu_keyboard():
    markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    markup.add(*[KeyboardButton(text=item) for item in main_menu_def_buttons])
    return markup


def keyboard_send_phone_to_register_in_db():
    markup = ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    button_phone = KeyboardButton(text=send_phone_button, request_contact=True)
    button_cancel = KeyboardButton(text=cancel_reg_button)
    markup.add(button_phone, button_cancel)
    return markup
