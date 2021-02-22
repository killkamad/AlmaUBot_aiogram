import logging

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from utils import db_api as db
from .callback_datas import certificate_callback, certificate_update_callback, certificate_delete_callback, \
                            request_callback, request_type_callback, request_update_callback, request_delete_callback


def inline_keyboard_certificate_admin():
    markup = InlineKeyboardMarkup(row_width=1)
    callback_upload = InlineKeyboardButton(text="📤 Загрузить справку", callback_data='send_certificate_bot')
    callback_update = InlineKeyboardButton(text="♻ Обновить справку", callback_data='update_certificate_bot')
    callback_delete = InlineKeyboardButton(text="❌ Удалить справку", callback_data='delete_certificate_bot')
    callback_back = InlineKeyboardButton(text="⬅ Назад", callback_data='back_to_admin_menu')
    markup.add(callback_upload, callback_update, callback_delete, callback_back)
    return markup


def inline_keyboard_cancel_certificate():
    markup = InlineKeyboardMarkup()
    cancel_button = InlineKeyboardButton(text="❌ Отмена отправки справки", callback_data="cancel_step_certificate")
    markup.add(cancel_button)
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
    markup.add(*[InlineKeyboardButton(text=item['full_name'],
                                      callback_data=request_update_callback.new(request_name=item["full_name"])) for item in request])
    markup.add(InlineKeyboardButton(text="⬅ Назад", callback_data="cancel_update_step"))
    return markup


async def inline_keyboard_update_certificate(user_id):
    markup = InlineKeyboardMarkup(row_width=1)
    certificate = await db.select_data_certificate(user_id)
    markup.add(*[InlineKeyboardButton(text=f"{item['name_certif']} {item['date_time'].strftime('%d.%m.%y')}",
                                      callback_data=certificate_update_callback.new(id=item['id_request'])) for item in certificate])
    markup.add(InlineKeyboardButton(text="⬅ Назад", callback_data="update_certificate_bot"))
    return markup


async def inline_keyboard_del_req_certificate():
    markup = InlineKeyboardMarkup(row_width=1)
    request = await db.select_data_request_certificate()
    markup.add(*[InlineKeyboardButton(text=item['full_name'],
                                      callback_data=request_delete_callback.new(request_name=item["full_name"])) for item in request])
    markup.add(InlineKeyboardButton(text="⬅ Назад", callback_data="cancel_delete_step"))
    return markup


async def inline_keyboard_delete_certificate(user_id):
    markup = InlineKeyboardMarkup(row_width=1)
    certificate = await db.select_data_certificate(user_id)
    markup.add(*[InlineKeyboardButton(text=f"{item['name_certif']} {item['date_time'].strftime('%d.%m.%y')}",
                                      callback_data=certificate_delete_callback.new(id=item['id_request'])) for item in certificate])
    markup.add(InlineKeyboardButton(text="⬅ Назад", callback_data="delete_certificate_bot"))
    return markup


async def inline_keyboard_get_request_certificate():
    markup = InlineKeyboardMarkup(row_width=1)
    request = await db.select_data_request_certificate()
    markup.add(*[InlineKeyboardButton(text=item['full_name'],
                                      callback_data=request_callback.new(request_name=item["full_name"])) for item in request])
    markup.add(InlineKeyboardButton(text="⬅ Назад", callback_data="cancel_load_step"))
    return markup


async def inline_keyboard_on_send_request_certificate():
    markup = InlineKeyboardMarkup(row_width=1)
    request = await db.select_data_on_send_request_certificate()
    markup.add(*[InlineKeyboardButton(text=item['full_name'],
                                      callback_data=request_callback.new(request_name=item["full_name"])) for item in request])
    markup.add(InlineKeyboardButton(text="⬅ Назад", callback_data="cancel_load_step"))
    return markup


async def inline_keyboard_get_certificate_type(user_id):
    markup = InlineKeyboardMarkup(row_width=1)
    request = await db.select_data_certificate_type(user_id)
    markup.add(*[InlineKeyboardButton(text=item['certif_type'],
                                      callback_data=request_type_callback.new(request_name=item["certif_type"])) for item in request])
    markup.add(InlineKeyboardButton(text="⬅ Назад", callback_data="send_certificate_bot"))
    return markup
