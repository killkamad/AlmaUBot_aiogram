from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from data.button_names.main_menu_buttons import schedule_button_text, faq_button_text, library_button_text, shop_button_text, \
                                                calendar_button_text, certificate_button_text, feedback_button_text, navigation_button_text

def inline_keyboard_menu():
    markup = InlineKeyboardMarkup(row_width=2)
    schedule_button = InlineKeyboardButton(text=schedule_button_text, callback_data="/schedule")
    faq_button = InlineKeyboardButton(text=faq_button_text, callback_data="/faq")
    library_button = InlineKeyboardButton(text=library_button_text, callback_data="/library")
    shop_button = InlineKeyboardButton(text=shop_button_text, callback_data="/almaushop")
    acalendar_button = InlineKeyboardButton(text=calendar_button_text, callback_data="/academ_calendar")
    certificate_button = InlineKeyboardButton(text=certificate_button_text, callback_data="/certificate")
    feedback_button = InlineKeyboardButton(text=feedback_button_text, callback_data="/feedback")
    navigation_button = InlineKeyboardButton(text=navigation_button_text, callback_data="/nav_unifi")
    markup.add(schedule_button, faq_button, library_button, shop_button)
    markup.row(acalendar_button)
    markup.row(certificate_button)
    markup.row(feedback_button)
    markup.row(navigation_button)
    return markup
