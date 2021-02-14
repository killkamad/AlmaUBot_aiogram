from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from utils import db_api as db
import logging


def inline_keyboard_certificate_admin():
    markup = InlineKeyboardMarkup(row_width=1)
    callback_upload = InlineKeyboardButton(text="📤 Загрузить справку", callback_data='send_certificate_bot')
    callback_update = InlineKeyboardButton(text="♻ Обновить справку", callback_data='update_certificate_bot')
    callback_delete = InlineKeyboardButton(text="❌ Удалить справку", callback_data='delete_certificate_bot')
    callback_back = InlineKeyboardButton(text="⬅ Назад", callback_data='back_to_admin_menu')
    markup.add(callback_upload, callback_update, callback_delete, callback_back)
    return markup


def cancel_or_send_certificate():
    markup = InlineKeyboardMarkup()
    callback_button = InlineKeyboardButton(text="✅ Отправить", callback_data="send_certificate")
    callback_button2 = InlineKeyboardButton(text="❌ Отмена", callback_data="cancel_certificate")
    markup.add(callback_button, callback_button2)
    return markup


def cancel_or_update_certificate():
    markup = InlineKeyboardMarkup()
    callback_button = InlineKeyboardButton(text="✅ Изменить", callback_data="update_certificate_button")
    callback_button2 = InlineKeyboardButton(text="❌ Отмена", callback_data="cancel_update_certificate")
    markup.add(callback_button, callback_button2)
    return markup


def cancel_or_delete_certificate():
    markup = InlineKeyboardMarkup()
    callback_button = InlineKeyboardButton(text="✅ Удалить", callback_data="delete_certificate_button")
    callback_button2 = InlineKeyboardButton(text="❌ Отмена", callback_data="cancel_delete_certificate")
    markup.add(callback_button, callback_button2)
    return markup


async def inline_keyboard_upd_req_certificate():
    markup = InlineKeyboardMarkup(row_width=1)
    request = await db.select_data_request_certificate()
    call_list = []
    request_name = []
    for call_value in request:
        callback_data = "['upd_req_std', '" + call_value[2] + "']"
        request_name.append(call_value[2])
        call_list.append(callback_data)
    markup.add(*[InlineKeyboardButton(text=button, callback_data=call_data) for button, call_data in
                 zip(request_name, call_list)])
    markup.add(InlineKeyboardButton(text="⬅ Назад", callback_data="cancel_update_step"))
    return markup


async def inline_keyboard_update_certificate(user_id):
    markup = InlineKeyboardMarkup(row_width=1)
    request = await db.select_data_certificate(user_id)
    call_list = []
    request_name = []
    for call_value in request:
        callback_data = "['update_certificate', '" + call_value[4] + "']"
        print(callback_data)
        request_name.append(call_value[4])
        call_list.append(callback_data)
    markup.add(*[InlineKeyboardButton(text=button, callback_data=call_data) for button, call_data in
                 zip(request_name, call_list)])
    markup.add(InlineKeyboardButton(text="⬅ Назад", callback_data="cancel_update_step"))
    return markup


async def inline_keyboard_del_req_certificate():
    markup = InlineKeyboardMarkup(row_width=1)
    request = await db.select_data_request_certificate()
    call_list = []
    request_name = []
    for call_value in request:
        callback_data = "['del_req_std', '" + call_value[2] + "']"
        request_name.append(call_value[2])
        call_list.append(callback_data)
    markup.add(*[InlineKeyboardButton(text=button, callback_data=call_data) for button, call_data in
                 zip(request_name, call_list)])
    markup.add(InlineKeyboardButton(text="⬅ Назад", callback_data="cancel_update_step"))
    return markup


async def inline_keyboard_delete_certificate(user_id):
    markup = InlineKeyboardMarkup(row_width=1)
    certificate = await db.select_data_certificate(user_id)
    call_list = []
    certificate_name = []
    for call_value in certificate:
        callback_data = "['delete_certificate', '" + call_value[-1] + "']"
        certificate_name.append(call_value[-1])
        call_list.append(callback_data)
    markup.add(*[InlineKeyboardButton(text=button, callback_data=call_data) for button, call_data in
                 zip(certificate_name, call_list)])
    markup.add(InlineKeyboardButton(text="⬅ Назад", callback_data="cancel_delete_step"))
    return markup


async def inline_keyboard_get_request_certificate():
    markup = InlineKeyboardMarkup(row_width=1)
    request = await db.select_data_request_certificate()
    call_list = []
    request_name = []
    for call_value in request:
        callback_data = "['request_call', '" + call_value[2] + "']"
        request_name.append(call_value[2])
        call_list.append(callback_data)
    markup.add(*[InlineKeyboardButton(text=button, callback_data=call_data) for button, call_data in
                 zip(request_name, call_list)])
    markup.add(InlineKeyboardButton(text="⬅ Назад", callback_data="back_to_admin_menu"))
    return markup
