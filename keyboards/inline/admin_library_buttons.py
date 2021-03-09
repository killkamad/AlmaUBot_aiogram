import logging

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from utils import db_api as db
from .callback_datas import lib_res_delete_callback


def inline_keyboard_library_first_page_admin():
    markup = InlineKeyboardMarkup(row_width=1)
    callback_edit_website_button = InlineKeyboardButton(text="🌐 Изменить вебсайт", callback_data='edit_lib_website')
    callback_edit_contacts_button = InlineKeyboardButton(text="☎ Изменить контакты", callback_data='edit_lib_contacts')
    callback_edit_work_hours_button = InlineKeyboardButton(text="🕐 Изменить время работы",
                                                           callback_data='edit_lib_work_hours')
    callback_edit_courses_button = InlineKeyboardButton(text="🎓 Изменить онлайн курсы",
                                                        callback_data='edit_lib_courses')
    callback_edit_idcard_button = InlineKeyboardButton(text="💳 Изменить \"Потерял(a) ID-карту\"",
                                                       callback_data='edit_lib_idcard')
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
    callback_edit_rights_button = InlineKeyboardButton(text="📰 Изменить права читателя",
                                                       callback_data='edit_lib_rights')
    callback_edit_resources_button = InlineKeyboardButton(text="⚡ Изменить электронные ресурсы",
                                                          callback_data='edit_lib_resource')
    callback_edit_unallowed_button = InlineKeyboardButton(text="🚫 Изменить \"Что не разрешается\"",
                                                          callback_data='edit_lib_unallow')
    callback_edit_responsibility_button = InlineKeyboardButton(text="⛔ Изменить ответственность за нарушения",
                                                               callback_data='edit_lib_respons')
    callback_next_page = InlineKeyboardButton(text="⏩", callback_data='lib_next_page')
    callback_prev_page = InlineKeyboardButton(text="⏪", callback_data='library_admin_menu')
    callback_back = InlineKeyboardButton(text="⬅ Назад", callback_data='back_to_admin_menu')
    markup.add(callback_edit_rules_button, callback_edit_rights_button, \
               callback_edit_resources_button, callback_edit_unallowed_button, callback_edit_responsibility_button)
    markup.row(callback_prev_page, callback_next_page)
    markup.row(callback_back)
    return markup


def inline_keyboard_edit_button_content_library_or_cancel():
    markup = InlineKeyboardMarkup()
    callback_button = InlineKeyboardButton(text="✅ Изменить", callback_data="edit_lib_content")
    callback_button2 = InlineKeyboardButton(text="❌ Отмена", callback_data="cancel_edit_lib_content")
    markup.add(callback_button, callback_button2)
    return markup


def inline_keyboard_cancel_edit_library_button():
    markup = InlineKeyboardMarkup()
    callback_button = InlineKeyboardButton(text="❌ Отмена изменения", callback_data="cancel_edit_lib_button")
    markup.add(callback_button)
    return markup


def inline_keyboard_library_res_admin():
    markup = InlineKeyboardMarkup(row_width=1)
    callback_button1 = InlineKeyboardButton(text="📕 Лицензионные Базы Данных",
                                            callback_data='edit_library_registration')
    callback_button2 = InlineKeyboardButton(text="📗 Базы данных свободного доступа(Казахстанские)",
                                            callback_data='edit_library_free_kz')
    callback_button3 = InlineKeyboardButton(text="📗 Базы данных свободного доступа(Зарубежные)",
                                            callback_data='edit_library_free_foreign')
    callback_button4 = InlineKeyboardButton(text="📗 Онлайн библиотеки", callback_data='edit_library_online_libs')
    callback_back = InlineKeyboardButton(text="⬅ Назад", callback_data='lib_next_page')
    markup.add(callback_button1, callback_button2, callback_button3, callback_button4, callback_back)
    return markup


def inline_keyboard_library_del_res_admin():
    markup = InlineKeyboardMarkup(row_width=1)
    callback_button1 = InlineKeyboardButton(text="📕 Лицензионные Базы Данных",
                                            callback_data='del_library_registration')
    callback_button2 = InlineKeyboardButton(text="📗 Базы данных свободного доступа(Казахстанские)",
                                            callback_data='del_library_free_kz')
    callback_button3 = InlineKeyboardButton(text="📗 Базы данных свободного доступа(Зарубежные)",
                                            callback_data='del_library_free_foreign')
    callback_button4 = InlineKeyboardButton(text="📗 Онлайн библиотеки", callback_data='del_library_online_libs')
    callback_back = InlineKeyboardButton(text="⬅ Назад", callback_data='lib_next_page')
    markup.add(callback_button1, callback_button2, callback_button3, callback_button4, callback_back)
    return markup


def inline_keyboard_library_res_edit_admin():
    markup = InlineKeyboardMarkup(row_width=1)
    callback_lib_add = InlineKeyboardButton(text="➕ Добавить ресурс", callback_data='add_resource')
    # callback_lib_edit = InlineKeyboardButton(text="♻ Изменить ресурс", callback_data='edit_res_free_kz')
    callback_lib_delete = InlineKeyboardButton(text="❌ Удалить ресурс", callback_data='delete_resource')
    callback_back = InlineKeyboardButton(text="⬅ Назад", callback_data='edit_lib_resource')
    markup.add(callback_lib_add, callback_lib_delete, callback_back)
    return markup


def cancel_or_add_lib_resource():
    markup = InlineKeyboardMarkup()
    callback_button = InlineKeyboardButton(text="✅ Добавить", callback_data="add_lib_resource")
    callback_button2 = InlineKeyboardButton(text="❌ Отмена", callback_data="cancel_add_lib_resource")
    markup.add(callback_button, callback_button2)
    return markup


async def inline_keyboard_del_lib_res(lib_type):
    markup = InlineKeyboardMarkup(row_width=1)
    resource = await db.select_data_lib_resource(lib_type)
    markup.add(*[InlineKeyboardButton(text=f"{item['button_name']}",
                                      callback_data=lib_res_delete_callback.new(id=item['id'])) for item in resource])
    markup.add(InlineKeyboardButton(text="⬅ Назад", callback_data="back_del_lib_resource"))
    return markup


def cancel_or_delete_lib_resource():
    markup = InlineKeyboardMarkup()
    callback_button = InlineKeyboardButton(text="✅ Удалить", callback_data="del_lib_resource")
    callback_button2 = InlineKeyboardButton(text="❌ Отмена", callback_data="cancel_del_lib_resource")
    markup.add(callback_button, callback_button2)
    return markup


def cancel_edit_lib_res():
    markup = InlineKeyboardMarkup()
    callback_button = InlineKeyboardButton(text="❌ Отмена", callback_data="cancel_edit_lib_resource")
    markup.add(callback_button)
    return markup
