from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from data.button_names.almaushop_buttons import almaushop_def_buttons
from data.button_names.main_menu_buttons import to_main_menu_button


def keyboard_almaushop():
    markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    markup.add(*[KeyboardButton(text=item) for item in almaushop_def_buttons])
    markup.row(KeyboardButton(text=to_main_menu_button))
    return markup
