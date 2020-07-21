from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


def inline_keyboard_menu():
    markup = InlineKeyboardMarkup()
    callback_button = InlineKeyboardButton(text="📅 Расписание", callback_data="/schedule")
    callback_button1 = InlineKeyboardButton(text="❓ FAQ", callback_data="/faq")
    markup.add(callback_button, callback_button1)
    return markup
