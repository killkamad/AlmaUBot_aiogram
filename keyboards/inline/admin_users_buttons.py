from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from keyboards.inline.callback_datas import last_ten_users_callback
from utils import db_api as db
import logging


# Админ меню Пользователей
def inline_keyboard_users_admin():
    markup = InlineKeyboardMarkup(row_width=1)
    callback_edit_users_role = InlineKeyboardButton(
        text="♻ Изменить роль пользователю",
        callback_data='edit_users_role')
    # callback_delete_users_role = InlineKeyboardButton(
    #     text="❌ Удалить роль пользователю",
    #     callback_data='delete_users_role')
    callback_show_ten_last_users = InlineKeyboardButton(
        text="🔟 Показать 10 последних",
        callback_data='show_ten_last_users')
    callback_back = InlineKeyboardButton(
        text="⬅ Назад",
        callback_data='back_to_admin_menu')
    markup.add(callback_edit_users_role, callback_show_ten_last_users, callback_back)
    return markup


# Админ меню выбора роли для пользователя
def inline_keyboard_users_admin_roles():
    markup = InlineKeyboardMarkup(row_width=1)
    callback_admin = InlineKeyboardButton(text="Администратор", callback_data='admin_role')
    callback_library_admin = InlineKeyboardButton(text="Отдел Библиотеки", callback_data='library_admin_role')
    callback_marketing_admin = InlineKeyboardButton(text="Отдел Маркетинга", callback_data='marketing_admin_role')
    callback_advisor = InlineKeyboardButton(text="Адвайзер", callback_data='advisor_role')
    callback_cancel = InlineKeyboardButton(text="❌ Отмена", callback_data='cancel_role_choice')
    markup.add(callback_admin, callback_library_admin, callback_marketing_admin, callback_advisor, callback_cancel)
    return markup


# Админ меню подтвержение изменения роли для пользователя
def inline_keyboard_users_admin_roles_accept_decline():
    markup = InlineKeyboardMarkup(row_width=1)
    callback_accept = InlineKeyboardButton(text="✅ Изменить", callback_data='admin_role_edit_accept')
    callback_decline = InlineKeyboardButton(text="❌ Отмена", callback_data='admin_role_edit_decline')
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
    markup.add(InlineKeyboardButton(text="⬅ Назад", callback_data="back_to_users_admin"))
    return markup


# Админ 10 последних пользователей в базе данных
def back_to_last_ten_users():
    markup = InlineKeyboardMarkup(row_width=1)
    markup.add(InlineKeyboardButton(text="⬅ Назад", callback_data="back_to_last_ten_users"))
    return markup


# Изменение роли для пользователя Отмена
def inline_keyboard_cancel_users_role_change():
    markup = InlineKeyboardMarkup()
    cancel_button = InlineKeyboardButton(text="❌ Отмена", callback_data="admin_role_edit_decline")
    markup.add(cancel_button)
    return markup
