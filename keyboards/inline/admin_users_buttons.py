import logging

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from keyboards.inline.callback_datas import last_ten_users_callback
from data.button_names.admin_menu_buttons import back_to_admin_menu_button, edit_admin_button, cancel_admin_button
from data.button_names.users_buttons import *
from utils import db_api as db



# Админ меню Пользователей
def inline_keyboard_users_admin():
    markup = InlineKeyboardMarkup(row_width=1)
    callback_edit_users_role = InlineKeyboardButton(text=change_role_button_text, callback_data='edit_users_role')
    # callback_delete_users_role = InlineKeyboardButton(
    #     text="❌ Удалить роль пользователю",
    #     callback_data='delete_users_role')
    callback_show_ten_last_users = InlineKeyboardButton(text=last_ten_button_text, callback_data='show_ten_last_users')
    callback_back = InlineKeyboardButton(text=back_to_admin_menu_button, callback_data='back_to_admin_menu')
    markup.add(callback_edit_users_role, callback_show_ten_last_users, callback_back)
    return markup


# Админ меню выбора роли для пользователя
def inline_keyboard_users_admin_roles():
    markup = InlineKeyboardMarkup(row_width=1)
    callback_admin = InlineKeyboardButton(text=admin_button_text, callback_data='admin_role')
    callback_library_admin = InlineKeyboardButton(text=lib_admin_button_text, callback_data='library_admin_role')
    callback_marketing_admin = InlineKeyboardButton(text=mark_admin_button_text, callback_data='marketing_admin_role')
    callback_advisor = InlineKeyboardButton(text=advisor_button_text, callback_data='advisor_role')
    callback_cancel = InlineKeyboardButton(text=cancel_admin_button, callback_data='cancel_role_choice')
    markup.add(callback_admin, callback_library_admin, callback_marketing_admin, callback_advisor, callback_cancel)
    return markup


# Админ меню подтвержение изменения роли для пользователя
def inline_keyboard_users_admin_roles_accept_decline():
    markup = InlineKeyboardMarkup(row_width=1)
    callback_accept = InlineKeyboardButton(text=edit_admin_button, callback_data='admin_role_edit_accept')
    callback_decline = InlineKeyboardButton(text=cancel_admin_button, callback_data='admin_role_edit_decline')
    markup.add(callback_accept, callback_decline)
    return markup


# Админ 10 последних пользователей в базе данных
async def inline_keyboard_select_last_ten_users():
    markup = InlineKeyboardMarkup(row_width=1)
    users_list = await db.select_last_ten_users()
    markup.add(
        *[InlineKeyboardButton(text=f'{i}. {user["idt"]}',
                               callback_data=last_ten_users_callback.new(telegram_id=user["idt"]))
          for i, user in enumerate(users_list, 1)])
    markup.add(InlineKeyboardButton(text=back_to_admin_menu_button, callback_data="back_to_users_admin"))
    return markup


# Админ 10 последних пользователей в базе данных
def back_to_last_ten_users():
    markup = InlineKeyboardMarkup(row_width=1)
    markup.add(InlineKeyboardButton(text=back_to_admin_menu_button, callback_data="back_to_last_ten_users"))
    return markup


# Изменение роли для пользователя Отмена
def inline_keyboard_cancel_users_role_change():
    markup = InlineKeyboardMarkup()
    cancel_button = InlineKeyboardButton(text=cancel_admin_button, callback_data="admin_role_edit_decline")
    markup.add(cancel_button)
    return markup
