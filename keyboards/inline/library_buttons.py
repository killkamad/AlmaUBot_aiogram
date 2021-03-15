from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from utils import db_api as db
from .callback_datas import lib_res_callback
from data.button_names.lib_buttons import lib_send_reg_data_button, lib_cancel_reg_button, lib_reg_db_button, lib_free_kz_button, \
                                          lib_free_foreign_button, lib_free_online_button, lib_reg_button
from data.button_names.main_menu_buttons import to_back_button, cancel_menu_button

# def inline_keyboard_library():
#     markup = InlineKeyboardMarkup(row_width=1)
#     callback_button1 = InlineKeyboardButton(text="📕 Вебсайт", callback_data='library_site')
#     callback_button2 = InlineKeyboardButton(text="💡 Электронные ресурсы", callback_data='library_el_res')
#     callback_button3 = InlineKeyboardButton(text="☎ Контакты", callback_data='lib_contacts')
#     callback_button4 = InlineKeyboardButton(text="🕐 Время работы", callback_data='lib_work_time')
#     callback_button7 = InlineKeyboardButton(text="💻 Онлайн курсы", callback_data='lib_online_courses')
#     callback_button8 = InlineKeyboardButton(text="💳 Потерял ID-карту", callback_data='lib_lost_card')
#     callback_button9 = InlineKeyboardButton(text="📛 Правила", callback_data='lib_laws')
#     callback_button10 = InlineKeyboardButton(text="📰 Права читателя", callback_data='lib_rights')
#     callback_button11 = InlineKeyboardButton(text="❌ Что не разрешается", callback_data='lib_not_allow')
#     callback_button12 = InlineKeyboardButton(text="⛔ Ответственность за нарушения", callback_data='lib_responsible')
#     callback_button13 = InlineKeyboardButton(text="⬅ Назад", callback_data="go_back")
#     markup.add(callback_button1, callback_button2, callback_button3, callback_button4,
#                callback_button7, callback_button8, callback_button9, callback_button10,
#                callback_button11, callback_button12, callback_button13)
#     return markup

async def inline_keyboard_library_choice_db():
        markup = InlineKeyboardMarkup(row_width=3)
        resource = await db.select_data_lib_resource_reg()
        markup.add(*[InlineKeyboardButton(text=f"{item['button_name']}",
                                          callback_data=lib_res_callback.new(id=item['id'])) for item in resource])
        markup.add(InlineKeyboardButton(text=to_back_button, callback_data="back_to_library_el_res"))
        return markup


def inline_keyboard_cancel_lic_db_reg():
    markup = InlineKeyboardMarkup(row_width=1)
    cancel = InlineKeyboardButton(text=lib_cancel_reg_button, callback_data="SendDataCancel")
    markup.add(cancel)
    return markup


def inline_keyboard_library_registration():
    markup = InlineKeyboardMarkup(row_width=1)
    callback_button = InlineKeyboardButton(text=lib_reg_button, callback_data='library_registration_button')
    callback_back = InlineKeyboardButton(text=to_back_button, callback_data="back_to_library_el_res")
    markup.add(callback_button, callback_back)
    return markup


def inline_keyboard_send_reg_data():
    markup = InlineKeyboardMarkup(row_width=1)
    callback_button = InlineKeyboardButton(text=lib_send_reg_data_button, callback_data='SendEmailToLibrary')
    callback_back = InlineKeyboardButton(text=cancel_menu_button, callback_data="SendDataCancel")
    markup.add(callback_button, callback_back)
    return markup


def inline_keyboard_back_to_library():
    markup = InlineKeyboardMarkup(row_width=1)
    callback_back = InlineKeyboardButton(text=to_back_button, callback_data="go_back_library")
    markup.add(callback_back)
    return markup


def inline_keyboard_library_el_res():
    markup = InlineKeyboardMarkup(row_width=1)
    callback_button1 = InlineKeyboardButton(text=lib_reg_db_button, callback_data='library_registration')
    callback_button2 = InlineKeyboardButton(text=lib_free_kz_button,
                                            callback_data='library_free_kaz')
    callback_button3 = InlineKeyboardButton(text=lib_free_foreign_button,
                                            callback_data='library_free_zarub')
    callback_button4 = InlineKeyboardButton(text= lib_free_online_button, callback_data='library_online_librares')
    # callback_back = InlineKeyboardButton(text="⬅ Назад", callback_data="go_back_library")
    markup.add(callback_button1, callback_button2, callback_button3, callback_button4)
    return markup


# Базы данных свободного доступа (Казахстанские)
async def inline_keyboard_library_base_kaz():
    markup = InlineKeyboardMarkup(row_width=1)
    resource = await db.select_data_lib_resource_kz()
    markup.add(*[InlineKeyboardButton(text=f"{item['button_name']}", url=item['lib_url'],
                                      callback_data=lib_res_callback.new(id=item['id'])) for item in resource])
    markup.add(InlineKeyboardButton(text=to_back_button, callback_data="back_to_library_el_res"))
    return markup


# Базы данных свободного доступа (Зарубежные)
async def inline_keyboard_library_base_zarub():
    markup = InlineKeyboardMarkup(row_width=2)
    resource = await db.select_data_lib_resource_frgn()
    markup.add(*[InlineKeyboardButton(text=f"{item['button_name']}", url=item['lib_url'],
                                      callback_data=lib_res_callback.new(id=item['id'])) for item in resource])
    markup.add(InlineKeyboardButton(text=to_back_button, callback_data="back_to_library_el_res"))
    return markup


# Онлайн Библиотеки
async def inline_keyboard_library_online_bib():
    markup = InlineKeyboardMarkup(row_width=1)
    resource = await db.select_data_lib_resource_online()
    markup.add(*[InlineKeyboardButton(text=f"{item['button_name']}", url=item['lib_url'],
                                      callback_data=lib_res_callback.new(id=item['id'])) for item in resource])
    markup.add(InlineKeyboardButton(text=to_back_button, callback_data="back_to_library_el_res"))
    return markup
