import logging

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from utils import db_api as db


def inline_keyboard_library_first_page_admin():
    markup = InlineKeyboardMarkup(row_width=1)
    callback_edit_website_button = InlineKeyboardButton(text="🌐 Изменить вебсайт", callback_data='edit_lib_website')
    callback_edit_contacts_button = InlineKeyboardButton(text="☎ Изменить контакты", callback_data='edit_lib_contacts')
    callback_edit_work_hours_button = InlineKeyboardButton(text="🕐 Изменить время работы", callback_data='edit_lib_work_hours')
    callback_edit_courses_button = InlineKeyboardButton(text="🎓 Изменить онлайн курсы", callback_data='edit_lib_courses')
    callback_edit_idcard_button = InlineKeyboardButton(text="💳 Изменить \"Потерял(a) ID-карту\"", callback_data='edit_lib_idcard')
    callback_next_page = InlineKeyboardButton(text="⏩", callback_data='lib_next_page')
    callback_prev_page = InlineKeyboardButton(text="⏪", callback_data='library_admin_menu')
    callback_back = InlineKeyboardButton(text="⬅ Назад", callback_data='back_to_admin_menu')
    markup.add(callback_edit_website_button, callback_edit_contacts_button, \
               callback_edit_work_hours_button, callback_edit_courses_button, callback_edit_idcard_button)
    markup.row(callback_prev_page, callback_next_page)
    markup.row(callback_back)
    return markup


def inline_keyboard_library_second_page_admin():
    markup = InlineKeyboardMarkup(row_width=1)
    callback_edit_rules_button = InlineKeyboardButton(text="⚠ Изменить правила", callback_data='edit_lib_rules')
    callback_edit_rights_button = InlineKeyboardButton(text="📰 Изменить права читателя", callback_data='edit_lib_rights')
    callback_edit_unallowed_button = InlineKeyboardButton(text="🚫 Изменить \"Что не разрешается\"", callback_data='edit_lib_unallow')
    callback_edit_responsibility_button = InlineKeyboardButton(text="⛔ Изменить ответственность за нарушения", callback_data='edit_lib_respons')
    callback_next_page = InlineKeyboardButton(text="⏩", callback_data='lib_next_page')
    callback_prev_page = InlineKeyboardButton(text="⏪", callback_data='library_admin_menu')
    callback_back = InlineKeyboardButton(text="⬅ Назад", callback_data='back_to_admin_menu')
    markup.add(callback_edit_rules_button, callback_edit_rights_button, \
               callback_edit_unallowed_button, callback_edit_responsibility_button)
    markup.row(callback_prev_page, callback_next_page)
    markup.row(callback_back)
    return markup


def inline_keyboard_edit_button_content_library_or_cancel():
    markup = InlineKeyboardMarkup()
    callback_button = InlineKeyboardButton(text="✅ Изменить", callback_data="edit_lib_button")
    callback_button2 = InlineKeyboardButton(text="❌ Отмена", callback_data="cancel_edit_lib_button")
    markup.add(callback_button, callback_button2)
    return markup
