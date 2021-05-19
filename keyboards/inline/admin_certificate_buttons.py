import logging

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from utils import db_api as db
from .callback_datas import instruction_update_callback, instruction_delete_callback, instruction_add_doc_callback

from data.button_names.certificate_buttons import add_certificate_button, edit_certificate_button, \
    delete_certificate_button, cancel_certificate_button, add_doc_certificate_button
from data.button_names.admin_menu_buttons import back_to_admin_menu_button, send_admin_button, edit_admin_button, \
    delete_admin_button, cancel_admin_button, add_file_button


def inline_keyboard_certificate_admin():
    markup = InlineKeyboardMarkup(row_width=1)
    callback_upload = InlineKeyboardButton(text=add_certificate_button, callback_data='send_instruction_bot')
    callback_update = InlineKeyboardButton(text=edit_certificate_button, callback_data='update_instruction_bot')
    callback_add_doc = InlineKeyboardButton(text=add_doc_certificate_button, callback_data='add_doc_instruction_bot')
    callback_delete = InlineKeyboardButton(text=delete_certificate_button, callback_data='delete_instruction_bot')
    callback_back = InlineKeyboardButton(text=back_to_admin_menu_button, callback_data='back_to_admin_menu')
    markup.add(callback_upload, callback_update, callback_add_doc, callback_delete, callback_back)
    return markup


async def inline_keyboard_upd_instruction():
    markup = InlineKeyboardMarkup(row_width=1)
    instructions = await db.select_data_on_edit_instruction()
    markup.add(*[InlineKeyboardButton(text=item['button_name'],
                                      callback_data=instruction_update_callback.new(id=item['id'])) for item in
                 instructions])
    markup.add(InlineKeyboardButton(text=back_to_admin_menu_button, callback_data="cancel_update_step_cert"))
    return markup


async def inline_keyboard_add_doc_instruction():
    markup = InlineKeyboardMarkup(row_width=1)
    instructions = await db.select_instruction_without_file()
    markup.add(*[InlineKeyboardButton(text=item['button_name'],
                                      callback_data=instruction_add_doc_callback.new(id=item['id'])) for item in
                 instructions])
    markup.add(InlineKeyboardButton(text=back_to_admin_menu_button, callback_data="cancel_update_step_cert"))
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


def cancel_edit_instruction():
    markup = InlineKeyboardMarkup()
    callback_button = InlineKeyboardButton(text=cancel_admin_button, callback_data="cancel_edit_instruction")
    markup.add(callback_button)
    return markup


def cancel_add_doc_instruction():
    markup = InlineKeyboardMarkup()
    callback_button = InlineKeyboardButton(text=cancel_admin_button, callback_data="cancel_add_doc_instruction")
    markup.add(callback_button)
    return markup


def cancel_add_instruction_or_add_file():
    markup = InlineKeyboardMarkup(row_width=1)
    callback_button = InlineKeyboardButton(text=send_admin_button, callback_data="send_instruction")
    callback_button2 = InlineKeyboardButton(text=add_file_button, callback_data="add_document_certificate")
    callback_button3 = InlineKeyboardButton(text=cancel_admin_button, callback_data="cancel_instruction")
    markup.add(callback_button, callback_button2, callback_button3)
    return markup


def cancel_or_add_instruction():
    markup = InlineKeyboardMarkup(row_width=1)
    callback_button = InlineKeyboardButton(text=send_admin_button, callback_data="send_instruction")
    callback_button3 = InlineKeyboardButton(text=cancel_admin_button, callback_data="cancel_instruction")
    markup.add(callback_button, callback_button3)
    return markup


def cancel_or_add_doc_instruction():
    markup = InlineKeyboardMarkup(row_width=1)
    callback_button = InlineKeyboardButton(text=send_admin_button, callback_data="add_doc_instruction")
    callback_button3 = InlineKeyboardButton(text=cancel_admin_button, callback_data="cancel_instruction")
    markup.add(callback_button, callback_button3)
    return markup


def cancel_or_update_instruction():
    markup = InlineKeyboardMarkup()
    callback_button = InlineKeyboardButton(text=edit_admin_button, callback_data="update_instruction_button")
    callback_button2 = InlineKeyboardButton(text=cancel_admin_button, callback_data="cancel_update_instruction")
    markup.add(callback_button, callback_button2)
    return markup


def cancel_or_delete_instruction():
    markup = InlineKeyboardMarkup()
    callback_button = InlineKeyboardButton(text=delete_admin_button, callback_data="delete_instruction_button")
    callback_button2 = InlineKeyboardButton(text=cancel_admin_button, callback_data="cancel_delete_instruction")
    markup.add(callback_button, callback_button2)
    return markup
