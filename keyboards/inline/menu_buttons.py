from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


def inline_keyboard_menu():
    markup = InlineKeyboardMarkup(row_width=2)
    callback_button = InlineKeyboardButton(text="📅 Расписание", callback_data="/schedule")
    callback_button1 = InlineKeyboardButton(text="⁉ FAQ", callback_data="/faq")
    callback_button2 = InlineKeyboardButton(text="📚 Библиотека", callback_data="/library")
    callback_button3 = InlineKeyboardButton(text="🌀 AlmaU Shop", callback_data="/almaushop")
    callback_button4 = InlineKeyboardButton(text="🗒 Академический календарь", callback_data="/academ_calendar")
    callback_button5 = InlineKeyboardButton(text="🏢 Получить справку с места учебы", callback_data="/certificate")
    callback_button6 = InlineKeyboardButton(text="📝 Обратная связь с ректором", callback_data="/feedback")
    callback_button7 = InlineKeyboardButton(text="🗺️ Навигация по университету", callback_data="/nav_unifi")
    markup.add(callback_button, callback_button1, callback_button2, callback_button3, callback_button4, callback_button5, callback_button6, callback_button7)
    return markup
