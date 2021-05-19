from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from data.button_names.admin_menu_buttons import mailing_button_text, schedule_button_text, certificate_button_text, \
    faq_button_text, \
    library_button_text, almaushop_button_text, calendar_button_text, navigation_button_text, \
    users_button_text


# Главное Админ меню
def inline_keyboard_admin():
    markup = InlineKeyboardMarkup(row_width=2)
    callback_sending = InlineKeyboardButton(text=mailing_button_text, callback_data='send_all')
    callback_schedule = InlineKeyboardButton(text=schedule_button_text, callback_data='schedule_admin_menu')
    callback_certificate = InlineKeyboardButton(text=certificate_button_text, callback_data="certificate_admin_menu")
    callback_faq = InlineKeyboardButton(text=faq_button_text, callback_data='faq_admin_menu')
    callback_library = InlineKeyboardButton(text=library_button_text, callback_data='library_admin_menu')
    callback_almaushop = InlineKeyboardButton(text=almaushop_button_text, callback_data='almaushop_admin_menu')
    callback_calendar = InlineKeyboardButton(text=calendar_button_text,
                                             callback_data='send_academic_calendar')
    callback_navigation = InlineKeyboardButton(text=navigation_button_text, callback_data='nav_university_admin_menu')
    callback_users = InlineKeyboardButton(text=users_button_text, callback_data='users_admin')
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
    callback_sending = InlineKeyboardButton(text=mailing_button_text, callback_data='send_all')
    callback_library = InlineKeyboardButton(text=library_button_text, callback_data='library_admin_menu')
    markup.add(callback_library, callback_sending)
    return markup


# Админ меню для роли marketing_admin
def inline_keyboard_marketing_admin():
    markup = InlineKeyboardMarkup(row_width=2)
    callback_sending = InlineKeyboardButton(text=mailing_button_text, callback_data='send_all')
    callback_faq = InlineKeyboardButton(text=faq_button_text, callback_data='faq_admin_menu')
    callback_almaushop = InlineKeyboardButton(text=almaushop_button_text, callback_data='almaushop_admin_menu')
    markup.add(callback_faq, callback_almaushop)
    markup.row(callback_sending)
    return markup


# Админ меню для роли advisor_admin
def inline_keyboard_advisor_admin():
    markup = InlineKeyboardMarkup(row_width=2)
    callback_sending = InlineKeyboardButton(text=mailing_button_text, callback_data='send_all')
    callback_schedule = InlineKeyboardButton(text=schedule_button_text, callback_data='schedule_admin_menu')
    callback_faq = InlineKeyboardButton(text=faq_button_text, callback_data='faq_admin_menu')
    callback_calendar = InlineKeyboardButton(text=calendar_button_text, callback_data='send_academic_calendar')
    callback_navigation = InlineKeyboardButton(text=navigation_button_text, callback_data='nav_university_admin_menu')
    markup.add(callback_schedule, callback_faq)
    markup.row(callback_calendar)
    markup.row(callback_navigation)
    markup.row(callback_sending)
    return markup
