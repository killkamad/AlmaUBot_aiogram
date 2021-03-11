from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from data.config import almaushop_def_buttons


def keyboard_almaushop():
    markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    markup.add(*[KeyboardButton(text=item) for item in almaushop_def_buttons])
    markup.row(KeyboardButton(text="⬅ В главное меню"))
    return markup
