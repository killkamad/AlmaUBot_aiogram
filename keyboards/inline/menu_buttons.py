from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


def inline_keyboard_menu():
    markup = InlineKeyboardMarkup(row_width=2)
    callback_button = InlineKeyboardButton(text="📅 Расписание", callback_data="/schedule")
    callback_button1 = InlineKeyboardButton(text="⁉ FAQ", callback_data="/faq")
    callback_button2 = InlineKeyboardButton(text="📚 Библиотека", callback_data="/library")
    callback_button3 = InlineKeyboardButton(text="🌀 AlmaU Shop", callback_data="/almaushop")
    markup.add(callback_button, callback_button1, callback_button2, callback_button3)
    return markup
