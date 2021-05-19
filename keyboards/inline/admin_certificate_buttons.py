import logging

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from utils import db_api as db
from .callback_datas import certificate_update_callback, certificate_delete_callback, \
    request_callback, request_type_callback, instruction_update_callback, instruction_delete_callback

from data.button_names.certificate_buttons import add_certificate_button, edit_certificate_button, \
    delete_certificate_button, cancel_certificate_button
from data.button_names.admin_menu_buttons import back_to_admin_menu_button, send_admin_button, edit_admin_button, \
    delete_admin_button, cancel_admin_button


def cancel_edit_instruction():
    markup = InlineKeyboardMarkup()
    callback_button = InlineKeyboardButton(text=cancel_admin_button, callback_data="cancel_edit_instruction")
    markup.add(callback_button)
    return markup


def cancel_or_add_instruction():
    markup = InlineKeyboardMarkup()
    callback_button = InlineKeyboardButton(text=send_admin_button, callback_data="send_instruction")
    callback_button2 = InlineKeyboardButton(text=cancel_admin_button, callback_data="cancel_instruction")
    markup.add(callback_button, callback_button2)
    return markup


def cancel_or_update_instruction():
    markup = InlineKeyboardMarkup()
    callback_button = InlineKeyboardButton(text=edit_admin_button, callback_data="update_instruction_button")
    callback_button2 = InlineKeyboardButton(text=cancel_admin_button, callback_data="cancel_update_instruction")
    markup.add(callback_button, callback_button2)
    return markup


def inline_keyboard_certificate_admin():
    markup = InlineKeyboardMarkup(row_width=1)
    callback_upload = InlineKeyboardButton(text=add_certificate_button, callback_data='send_instruction_bot')
    callback_update = InlineKeyboardButton(text=edit_certificate_button, callback_data='update_instruction_bot')
    callback_delete = InlineKeyboardButton(text=delete_certificate_button, callback_data='delete_instruction_bot')
    callback_back = InlineKeyboardButton(text=back_to_admin_menu_button, callback_data='back_to_admin_menu')
    markup.add(callback_upload, callback_update, callback_delete, callback_back)
    return markup


def inline_keyboard_cancel_certificate():
    markup = InlineKeyboardMarkup()
    cancel_button = InlineKeyboardButton(text=cancel_certificate_button, callback_data="cancel_step_certificate")
    markup.add(cancel_button)
    return markup


def cancel_or_send_certificate():
    markup = InlineKeyboardMarkup()
    callback_button = InlineKeyboardButton(text=send_admin_button, callback_data="send_certificate")
    callback_button2 = InlineKeyboardButton(text=cancel_admin_button, callback_data="cancel_certificate")
    markup.add(callback_button, callback_button2)
    return markup


def cancel_or_update_certificate():
    markup = InlineKeyboardMarkup()
    callback_button = InlineKeyboardButton(text=edit_admin_button, callback_data="update_certificate_button")
    callback_button2 = InlineKeyboardButton(text=cancel_admin_button, callback_data="cancel_update_certificate")
    markup.add(callback_button, callback_button2)
    return markup


def cancel_or_delete_instruction():
    markup = InlineKeyboardMarkup()
    callback_button = InlineKeyboardButton(text=delete_admin_button, callback_data="delete_instruction_button")
    callback_button2 = InlineKeyboardButton(text=cancel_admin_button, callback_data="cancel_delete_instruction")
    markup.add(callback_button, callback_button2)
    return markup


async def inline_keyboard_upd_instruction():
    markup = InlineKeyboardMarkup(row_width=1)
    instructions = await db.select_data_on_edit_instruction()
    markup.add(*[InlineKeyboardButton(text=item['button_name'],
                                      callback_data=instruction_update_callback.new(id=item['id'])) for item in instructions])
    markup.add(InlineKeyboardButton(text=back_to_admin_menu_button, callback_data="cancel_update_step_cert"))
    return markup


async def inline_keyboard_update_certificate(user_id):
    markup = InlineKeyboardMarkup(row_width=1)
    certificate = await db.select_data_certificate(user_id)
    markup.add(*[InlineKeyboardButton(text=f"{item['certif_type']} {item['date_time'].strftime('%d.%m.%y')}",
                                      callback_data=certificate_update_callback.new(id=item['id'])) for item in
                 certificate])
    markup.add(InlineKeyboardButton(text=back_to_admin_menu_button, callback_data="update_certificate_bot"))
    return markup


async def inline_keyboard_del_instruction():
    markup = InlineKeyboardMarkup(row_width=1)
    instructions = await db.select_data_on_edit_instruction()
    markup.add(*[InlineKeyboardButton(text=item['button_name'],
                                      callback_data=instruction_delete_callback.new(id=item['id'])) for
                 item in instructions])
    markup.add(InlineKeyboardButton(text=back_to_admin_menu_button,
                                    callback_data="cancel_delete_step_cert"))
    return markup


async def inline_keyboard_delete_certificate(user_id):
    markup = InlineKeyboardMarkup(row_width=1)
    certificate = await db.select_data_certificate(user_id)
    markup.add(*[InlineKeyboardButton(text=f"{item['certif_type']} {item['date_time'].strftime('%d.%m.%y')}",
                                      callback_data=certificate_delete_callback.new(id=item['id'])) for item in
                 certificate])
    markup.add(InlineKeyboardButton(text=back_to_admin_menu_button, callback_data="delete_certificate_bot"))
    return markup


async def inline_keyboard_on_send_request_certificate():
    markup = InlineKeyboardMarkup(row_width=1)
    request = await db.select_data_on_send_request_certificate()
    markup.add(*[InlineKeyboardButton(text=item['full_name'],
                                      callback_data=request_callback.new(id=item['id'])) for item in
                 request])
    markup.add(InlineKeyboardButton(text=back_to_admin_menu_button, callback_data="cancel_load_step"))
    return markup


async def inline_keyboard_get_certificate_type(user_id):
    markup = InlineKeyboardMarkup(row_width=1)
    request = await db.select_data_certificate_type(user_id)
    markup.add(*[InlineKeyboardButton(text=item['certif_type'],
                                      callback_data=request_type_callback.new(id=item['id'])) for
                 item in request])
    markup.add(InlineKeyboardButton(text=back_to_admin_menu_button, callback_data="send_certificate_bot"))
    return markup
