from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


def inline_keyboard_menu():
    markup = InlineKeyboardMarkup(row_width=2)
    schedule_button = InlineKeyboardButton(text="📅 Расписание", callback_data="/schedule")
    faq_button = InlineKeyboardButton(text="⁉ FAQ", callback_data="/faq")
    library_button = InlineKeyboardButton(text="📚 Библиотека", callback_data="/library")
    shop_button = InlineKeyboardButton(text="🌀 AlmaU Shop", callback_data="/almaushop")
    acalendar_button = InlineKeyboardButton(text="🗒 Академический календарь", callback_data="/academ_calendar")
    certificate_button = InlineKeyboardButton(text="🏢 Получить справку с места учебы", callback_data="/certificate")
    feedback_button = InlineKeyboardButton(text="📝 Обратная связь с ректором", callback_data="/feedback")
    navigation_button = InlineKeyboardButton(text="🗺️ Навигация по университету", callback_data="/nav_unifi")
    markup.add(schedule_button, faq_button, library_button, shop_button)
    markup.row(acalendar_button)
    markup.row(certificate_button)
    markup.row(feedback_button)
    markup.row(navigation_button)
    return markup
