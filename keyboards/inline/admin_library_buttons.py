import logging

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from utils import db_api as db
from .callback_datas import lib_res_delete_callback

from data.button_names.lib_buttons import lib_admin_website_button, lib_admin_contacts_button, \
    lib_admin_work_hours_button, \
    lib_admin_courses_button, lib_admin_idcard_button, lib_admin_rules_button, \
    lib_admin_rights_button, lib_admin_unallowed_button, lib_admin_responsibility_button, \
    lib_admin_booking_button, lib_admin_resources_button, lib_cancel_edit_button, lib_next, \
    lib_prev, lib_reg_db_button, lib_free_kz_button, lib_free_foreign_button, lib_free_online_button, \
    add_lib_resource_button, del_lib_resource_button
from data.button_names.admin_menu_buttons import back_to_admin_menu_button, add_admin_button, edit_admin_button, \
    delete_admin_button, cancel_admin_button


def inline_keyboard_library_first_page_admin():
    markup = InlineKeyboardMarkup(row_width=1)
    callback_edit_website_button = InlineKeyboardButton(text=lib_admin_website_button, callback_data='edit_lib_website')
    callback_edit_contacts_button = InlineKeyboardButton(text=lib_admin_contacts_button,
                                                         callback_data='edit_lib_contacts')
    callback_edit_work_hours_button = InlineKeyboardButton(text=lib_admin_work_hours_button,
                                                           callback_data='edit_lib_work_hours')
    callback_edit_courses_button = InlineKeyboardButton(text=lib_admin_courses_button,
                                                        callback_data='edit_lib_courses')
    callback_edit_idcard_button = InlineKeyboardButton(text=lib_admin_idcard_button,
                                                       callback_data='edit_lib_idcard')
    callback_next_page = InlineKeyboardButton(text=lib_next, callback_data='lib_next_page')
    callback_prev_page = InlineKeyboardButton(text=lib_prev, callback_data='library_admin_menu')
    callback_back = InlineKeyboardButton(text=back_to_admin_menu_button, callback_data='back_to_admin_menu')
    markup.add(callback_edit_website_button, callback_edit_contacts_button, \
               callback_edit_work_hours_button, callback_edit_courses_button, callback_edit_idcard_button)
    markup.row(callback_prev_page, callback_next_page)
    markup.row(callback_back)
    return markup


def inline_keyboard_library_second_page_admin():
    markup = InlineKeyboardMarkup(row_width=1)
    callback_edit_rules_button = InlineKeyboardButton(text=lib_admin_rules_button, callback_data='edit_lib_rules')
    callback_edit_rights_button = InlineKeyboardButton(text=lib_admin_rights_button,
                                                       callback_data='edit_lib_rights')
    callback_edit_resources_button = InlineKeyboardButton(text=lib_admin_resources_button,
                                                          callback_data='edit_lib_resource')
    callback_edit_unallowed_button = InlineKeyboardButton(text=lib_admin_unallowed_button,
                                                          callback_data='edit_lib_unallow')
    callback_edit_booking_button = InlineKeyboardButton(text=lib_admin_booking_button,
                                                        callback_data='edit_lib_booking')
    callback_edit_responsibility_button = InlineKeyboardButton(text=lib_admin_responsibility_button,
                                                               callback_data='edit_lib_respons')
    callback_next_page = InlineKeyboardButton(text=lib_next, callback_data='lib_next_page')
    callback_prev_page = InlineKeyboardButton(text=lib_prev, callback_data='library_admin_menu')
    callback_back = InlineKeyboardButton(text=back_to_admin_menu_button, callback_data='back_to_admin_menu')
    markup.add(callback_edit_rules_button, callback_edit_rights_button, \
               callback_edit_resources_button, callback_edit_unallowed_button, \
               callback_edit_booking_button, callback_edit_responsibility_button)
    markup.row(callback_prev_page, callback_next_page)
    markup.row(callback_back)
    return markup


def inline_keyboard_edit_button_content_library_or_cancel():
    markup = InlineKeyboardMarkup()
    callback_button = InlineKeyboardButton(text=edit_admin_button, callback_data="edit_lib_content")
    callback_button2 = InlineKeyboardButton(text=cancel_admin_button, callback_data="cancel_edit_lib_content")
    markup.add(callback_button, callback_button2)
    return markup


def inline_keyboard_cancel_edit_library_button():
    markup = InlineKeyboardMarkup()
    callback_button = InlineKeyboardButton(text=lib_cancel_edit_button, callback_data="cancel_edit_lib_button")
    markup.add(callback_button)
    return markup


def inline_keyboard_library_res_admin():
    markup = InlineKeyboardMarkup(row_width=1)
    callback_button1 = InlineKeyboardButton(text=lib_reg_db_button,
                                            callback_data='edit_library_registration')
    callback_button2 = InlineKeyboardButton(text=lib_free_kz_button,
                                            callback_data='edit_library_free_kz')
    callback_button3 = InlineKeyboardButton(text=lib_free_foreign_button,
                                            callback_data='edit_library_free_foreign')
    callback_button4 = InlineKeyboardButton(text=lib_free_online_button, callback_data='edit_library_online_libs')
    callback_back = InlineKeyboardButton(text=back_to_admin_menu_button, callback_data='lib_next_page')
    markup.add(callback_button1, callback_button2, callback_button3, callback_button4, callback_back)
    return markup


def inline_keyboard_library_del_res_admin():
    markup = InlineKeyboardMarkup(row_width=1)
    callback_button1 = InlineKeyboardButton(text=lib_reg_db_button,
                                            callback_data='del_library_registration')
    callback_button2 = InlineKeyboardButton(text=lib_free_kz_button,
                                            callback_data='del_library_free_kz')
    callback_button3 = InlineKeyboardButton(text=lib_free_foreign_button,
                                            callback_data='del_library_free_foreign')
    callback_button4 = InlineKeyboardButton(text=lib_free_online_button, callback_data='del_library_online_libs')
    callback_back = InlineKeyboardButton(text=back_to_admin_menu_button, callback_data='lib_next_page')
    markup.add(callback_button1, callback_button2, callback_button3, callback_button4, callback_back)
    return markup


def inline_keyboard_library_res_edit_admin():
    markup = InlineKeyboardMarkup(row_width=1)
    callback_lib_add = InlineKeyboardButton(text=add_lib_resource_button, callback_data='add_resource')
    callback_lib_delete = InlineKeyboardButton(text=del_lib_resource_button, callback_data='delete_resource')
    callback_back = InlineKeyboardButton(text=back_to_admin_menu_button, callback_data='edit_lib_resource')
    markup.add(callback_lib_add, callback_lib_delete, callback_back)
    return markup


def cancel_or_add_lib_resource():
    markup = InlineKeyboardMarkup()
    callback_button = InlineKeyboardButton(text=add_admin_button, callback_data="add_lib_resource")
    callback_button2 = InlineKeyboardButton(text=cancel_admin_button, callback_data="cancel_add_lib_resource")
    markup.add(callback_button, callback_button2)
    return markup


async def inline_keyboard_del_lib_res(lib_type):
    markup = InlineKeyboardMarkup(row_width=1)
    resource = await db.select_data_lib_resource(lib_type)
    markup.add(*[InlineKeyboardButton(text=f"{item['button_name']}",
                                      callback_data=lib_res_delete_callback.new(id=item['id'])) for item in resource])
    markup.add(InlineKeyboardButton(text=back_to_admin_menu_button, callback_data="back_del_lib_resource"))
    return markup


def cancel_or_delete_lib_resource():
    markup = InlineKeyboardMarkup()
    callback_button = InlineKeyboardButton(text=delete_admin_button, callback_data="del_lib_resource")
    callback_button2 = InlineKeyboardButton(text=cancel_admin_button, callback_data="cancel_del_lib_resource")
    markup.add(callback_button, callback_button2)
    return markup


def cancel_edit_lib_res():
    markup = InlineKeyboardMarkup()
    callback_button = InlineKeyboardButton(text=cancel_admin_button, callback_data="cancel_edit_lib_resource")
    markup.add(callback_button)
    return markup
