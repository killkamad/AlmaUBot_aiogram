from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


# Главное Админ меню
def inline_keyboard_admin():
    markup = InlineKeyboardMarkup(row_width=2)
    callback_sending = InlineKeyboardButton(text="📣 Рассылка", callback_data='send_all')
    callback_schedule = InlineKeyboardButton(text="📅 Расписание", callback_data='schedule_admin_menu')
    callback_certificate = InlineKeyboardButton(text="🏢 Справки", callback_data="certificate_admin_menu")
    callback_faq = InlineKeyboardButton(text="⁉ FAQ", callback_data='faq_admin_menu')
    callback_library = InlineKeyboardButton(text="📚 Библиотека", callback_data='library_admin_menu')
    callback_almaushop = InlineKeyboardButton(text="🌀 AlmaU Shop", callback_data='almaushop_admin_menu')
    callback_calendar = InlineKeyboardButton(text="🗒 Обновить Академический Календарь",
                                             callback_data='send_academic_calendar')
    callback_navigation = InlineKeyboardButton(text="🗺️ Меню Навигации", callback_data='nav_university_admin_menu')
    callback_users = InlineKeyboardButton(text="👥 Пользователи", callback_data='users_admin')
    markup.add(callback_schedule, callback_faq, callback_library, callback_almaushop)
    markup.row(callback_calendar)
    markup.row(callback_certificate)
    markup.row(callback_navigation)
    markup.row(callback_sending)
    markup.row(callback_users)
    return markup


# Админ меню для роли library_admin
def inline_keyboard_library_admin():
    markup = InlineKeyboardMarkup(row_width=2)
    callback_sending = InlineKeyboardButton(text="📣 Рассылка", callback_data='send_all')
    callback_library = InlineKeyboardButton(text="📚 Библиотека", callback_data='library_admin_menu')
    markup.add(callback_library, callback_sending)
    return markup


# Админ меню для роли marketing_admin
def inline_keyboard_marketing_admin():
    markup = InlineKeyboardMarkup(row_width=2)
    callback_sending = InlineKeyboardButton(text="📣 Рассылка", callback_data='send_all')
    callback_schedule = InlineKeyboardButton(text="📅 Расписание", callback_data='schedule_admin_menu')
    callback_certificate = InlineKeyboardButton(text="🏢 Справки", callback_data="certificate_admin_menu")
    callback_faq = InlineKeyboardButton(text="⁉ FAQ", callback_data='faq_admin_menu')
    callback_almaushop = InlineKeyboardButton(text="🌀 AlmaU Shop", callback_data='almaushop_admin_menu')
    callback_calendar = InlineKeyboardButton(text="🗒 Обновить Академический Календарь",
                                             callback_data='send_academic_calendar')
    callback_navigation = InlineKeyboardButton(text="🗺️ Меню Навигации", callback_data='nav_university_admin_menu')
    markup.add(callback_schedule, callback_faq, callback_almaushop)
    markup.row(callback_calendar)
    markup.row(callback_certificate)
    markup.row(callback_navigation)
    markup.row(callback_sending)
    return markup
