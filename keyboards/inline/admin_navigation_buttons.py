from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from utils import db_api as db
import logging
from .callback_datas import cabinet_callback_update

def inline_keyboard_nav_university_admin_menu():
    markup = InlineKeyboardMarkup(row_width=1)
    callback_button = InlineKeyboardButton(text="Карта-навигация по университету ", callback_data='map_nav_admin')
    callback_button1 = InlineKeyboardButton(text="Контакты ключевых центров", callback_data='contacts_center_admin')
    callback_button2 = InlineKeyboardButton(text="Профессорско-преподавательский состав",
                                            callback_data='tutors_university_admin')
    callback_button3 = InlineKeyboardButton(text="Назад", callback_data="back_to_admin_menu")
    markup.add(callback_button, callback_button1, callback_button2, callback_button3)
    return markup


def inline_keyboard_contact_center_admin():
    markup = InlineKeyboardMarkup(row_width=1)
    callback_button = InlineKeyboardButton(text="📤 Добавить ключевой центер",
                                           callback_data='send_contact_center_admin')
    callback_button1 = InlineKeyboardButton(text="♻ Обновить ключевой центер",
                                            callback_data='update_contact_center_admin')
    callback_button2 = InlineKeyboardButton(text="❌ Удалить ключевой центер",
                                            callback_data='delete_contact_center_admin')
    callback_back = InlineKeyboardButton(text="⬅ Назад", callback_data='nav_university_admin_menu')
    markup.add(callback_button, callback_button1, callback_button2, callback_back)
    return markup


def cancel_or_send_contact_center_admin():
    markup = InlineKeyboardMarkup()
    callback_button = InlineKeyboardButton(text="✅ Отправить", callback_data="send_contact_center")
    callback_button2 = InlineKeyboardButton(text="❌ Отмена", callback_data="cancel_step_contact_center_admin")
    markup.add(callback_button, callback_button2)
    return markup


async def inline_keyboard_contacts_center_update():
    markup = InlineKeyboardMarkup(row_width=1)
    contacts_center = await db.select_data_contact_centers()
    call_list = []
    name = []
    for call_value in contacts_center:
        callback_data = "['updade_contact_center', '" + call_value[-1] + "']"
        name.append(call_value[3])
        call_list.append(callback_data)
    markup.add(*[InlineKeyboardButton(text=button, callback_data=call_data) for button, call_data in
                 zip(name, call_list)])
    markup.add(InlineKeyboardButton(text="❌ Отмена", callback_data="cancel_step_contact_center_admin"))
    return markup


def cancel_or_update_contact_center_admin():
    markup = InlineKeyboardMarkup()
    callback_button = InlineKeyboardButton(text="✅ Изменить", callback_data="update_info_contact_center_admin")
    callback_button2 = InlineKeyboardButton(text="❌ Отмена", callback_data="cancel_step_contact_center_admin")
    markup.add(callback_button, callback_button2)
    return markup


async def inline_keyboard_contacts_center_delete():
    markup = InlineKeyboardMarkup(row_width=1)
    contacts_center = await db.select_data_contact_centers()
    call_list = []
    name = []
    for call_value in contacts_center:
        callback_data = "['delete_contact_center', '" + call_value[-1] + "']"
        name.append(call_value[3])
        call_list.append(callback_data)
    markup.add(*[InlineKeyboardButton(text=button, callback_data=call_data) for button, call_data in
                 zip(name, call_list)])
    markup.add(InlineKeyboardButton(text="❌ Отмена", callback_data="cancel_step_contact_center_admin"))
    return markup


def cancel_or_delete_contact_center_admin():
    markup = InlineKeyboardMarkup()
    callback_button = InlineKeyboardButton(text="✅ Удалить", callback_data="delete_info_contact_center_admin")
    callback_button2 = InlineKeyboardButton(text="❌ Отмена", callback_data="cancel_step_contact_center_admin")
    markup.add(callback_button, callback_button2)
    return markup


def inline_keyboard_cancel_contact_center_admin():
    markup = InlineKeyboardMarkup()
    cancel_button = InlineKeyboardButton(text="❌ Отмена ", callback_data="cancel_step_contact_center_admin")
    markup.add(cancel_button)
    return markup


def cancel_or_send_tutors_management():
    markup = InlineKeyboardMarkup()
    callback_button = InlineKeyboardButton(text="✅ Отправить", callback_data="send_tutors_management")
    callback_button2 = InlineKeyboardButton(text="❌ Отмена", callback_data="cancel_step_contact_center_admin")
    markup.add(callback_button, callback_button2)
    return markup


def inline_keyboard_map_nav_admin_menu():
    markup = InlineKeyboardMarkup(row_width=1)
    callback_button = InlineKeyboardButton(text="📤 Добавить кабинет",
                                           callback_data='send_cabinet_admin')
    callback_button1 = InlineKeyboardButton(text="♻ Обновить кабинет",
                                            callback_data='update_cabinet_admin')
    callback_button2 = InlineKeyboardButton(text="❌ Удалить кабинет",
                                            callback_data='delete_cabinet_admin')
    callback_back = InlineKeyboardButton(text="⬅ Назад", callback_data='nav_university_admin_menu')
    markup.add(callback_button, callback_button1, callback_button2, callback_back)
    return markup
    

def cancel_or_send_map_nav_admin():
    markup = InlineKeyboardMarkup()
    callback_button = InlineKeyboardButton(text="✅ Отправить", callback_data="send_map_navigation_admin")
    callback_button2 = InlineKeyboardButton(text="❌ Отмена", callback_data="cancel_step_contact_center_admin")
    markup.add(callback_button, callback_button2)
    return markup


async def inline_keyboard_cabinets_admin(building, floor):
    markup = InlineKeyboardMarkup(row_width=2)
    mapnav = await db.map_nav_description(building, floor)
    markup.add(*[InlineKeyboardButton(text=item['cabinet'], callback_data=cabinet_callback_update.new(cabinet=item["cabinet"])) for item in mapnav])
    return markup


def cancel_or_update_map_nav_admin():
    markup = InlineKeyboardMarkup()
    callback_button = InlineKeyboardButton(text="✅ Изменить", callback_data="update_map_navigation_admin")
    callback_button2 = InlineKeyboardButton(text="❌ Отмена", callback_data="cancel_step_contact_center_admin")
    markup.add(callback_button, callback_button2)
    return markup


def cancel_or_delete_map_nav_admin():
    markup = InlineKeyboardMarkup()
    callback_button = InlineKeyboardButton(text="✅ Удалить", callback_data="delete_map_navigation_admin")
    callback_button2 = InlineKeyboardButton(text="❌ Отмена", callback_data="cancel_step_contact_center_admin")
    markup.add(callback_button, callback_button2)
    return markup