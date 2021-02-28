from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


def always_stay_keyboard():
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    menu = KeyboardButton(text='🏠 Меню')
    # help_c = KeyboardButton(text='❓ Помощь')
    about = KeyboardButton(text='💻 О боте')
    markup.add(menu, about)
    return markup


def always_stay_menu_keyboard():
    markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    schedule_button = KeyboardButton(text="📅 Расписание", callback_data="/schedule")
    faq_button = KeyboardButton(text="⁉ FAQ", callback_data="/faq")
    library_button = KeyboardButton(text="📚 Библиотека", callback_data="/library")
    shop_button = KeyboardButton(text="🌀 AlmaU Shop", callback_data="/almaushop")
    calendar_button = KeyboardButton(text="🗒 Академический календарь", callback_data="/academ_calendar")
    certificate_button = KeyboardButton(text="🏢 Получить справку", callback_data="/certificate")
    feedback_button = KeyboardButton(text="📝 Связь с ректором", callback_data="/feedback")
    navigation_button = KeyboardButton(text="🗺️ Навигация по университету", callback_data="/nav_unifi")
    markup.add(schedule_button, faq_button, library_button, shop_button, calendar_button, certificate_button,
               feedback_button, navigation_button)
    return markup


def keyboard_send_phone_to_register_in_db():
    markup = ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    button_phone = KeyboardButton(text="☎ Отправить номер телефона", request_contact=True)
    button_cancel = KeyboardButton(text="❌ Отмена регистрации")
    markup.add(button_phone, button_cancel)
    return markup
