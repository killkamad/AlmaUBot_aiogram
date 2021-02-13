from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from utils import db_api as db


def inline_keyboard_nav_unifi():
    markup = InlineKeyboardMarkup(row_width=1)
    callback_button = InlineKeyboardButton(text="Карта-навигация по университету ", callback_data='map_nav')
    callback_button1 = InlineKeyboardButton(text="Контакты ключевых центров", callback_data='contacts_center')
    callback_button2 = InlineKeyboardButton(text="Профессорско-преподавательский состав",
                                            callback_data='tutors_university')
    callback_button3 = InlineKeyboardButton(text="Назад", callback_data="go_back")
    markup.add(callback_button, callback_button1, callback_button2, callback_button3)
    return markup


async def inline_keyboard_contacts_center():
    markup = InlineKeyboardMarkup(row_width=1)
    schedule = await db.select_data_contact_centers()
    call_list = []
    name = []
    for call_value in schedule:
        callback_data = "['contacts_center_call', '" + call_value[-1] + "']"
        name.append(call_value[3])
        call_list.append(callback_data)
    markup.add(*[InlineKeyboardButton(text=button, callback_data=call_data) for button, call_data in
                 zip(name, call_list)])
    markup.add(InlineKeyboardButton(text="⬅ Назад", callback_data="/nav_unifi"))
    return markup


def inline_keyboard_contacts_center_back():
    markup = InlineKeyboardMarkup(row_width=1)
    callback_button = InlineKeyboardButton(text="Назад", callback_data='contacts_center')
    markup.add(callback_button)
    return markup


# Кнопки Профессорско-преподавательский состав
def inline_keyboard_pps():
    markup = InlineKeyboardMarkup(row_width=1)
    callback_button = InlineKeyboardButton(text="Школа менеджмента", callback_data='shcool_management')
    callback_button1 = InlineKeyboardButton(text="Школа политики и права", callback_data='shcool_law')
    callback_button2 = InlineKeyboardButton(text="Школа Инженерного Менеджмента",callback_data='shcool_engineer')
    callback_button3 = InlineKeyboardButton(text="Школа предпринимательства и инноваций", callback_data='shcool_inovation')
    callback_button4 = InlineKeyboardButton(text="Высшая Школа Бизнеса", callback_data='shcool_bussines')
    callback_button5 = InlineKeyboardButton(text="Школа Экономики и Финансов", callback_data='shcool_economic')
    callback_button6 = InlineKeyboardButton(text="Ректорат", callback_data='rectorat')
    callback_button7 = InlineKeyboardButton(text="⬅ Назад", callback_data="/nav_unifi")
    markup.add(callback_button, callback_button1, callback_button2, callback_button3, callback_button4, callback_button5, callback_button6, callback_button7)
    return markup


def inline_keyboard_pps_shcool_management():
    markup = InlineKeyboardMarkup(row_width=1)
    callback_button = InlineKeyboardButton(text="Декан", callback_data='dekan_shcool_management')
    callback_button1 = InlineKeyboardButton(text="Преподаватели", callback_data='tutors_shcool_management')
    callback_button2 = InlineKeyboardButton(text="⬅ Назад", callback_data='tutors_university')
    markup.add(callback_button, callback_button1, callback_button2)
    return markup


def inline_keyboard_pps_shcool_law():
    markup = InlineKeyboardMarkup(row_width=1)
    callback_button = InlineKeyboardButton(text="Декан", callback_data='dekan_shcool_law')
    callback_button1 = InlineKeyboardButton(text="Преподаватели", callback_data='tutors_shcool_law')
    callback_button2 = InlineKeyboardButton(text="⬅ Назад", callback_data='tutors_university')
    markup.add(callback_button, callback_button1, callback_button2)
    return markup


def inline_keyboard_pps_shcool_engineer():
    markup = InlineKeyboardMarkup(row_width=1)
    callback_button = InlineKeyboardButton(text="Декан", callback_data='dekan_shcool_engineer')
    callback_button1 = InlineKeyboardButton(text="Преподаватели", callback_data='tutors_shcool_engineer')
    callback_button2 = InlineKeyboardButton(text="⬅ Назад", callback_data='tutors_university')
    markup.add(callback_button, callback_button1, callback_button2)
    return markup


def inline_keyboard_pps_shcool_inovation():
    markup = InlineKeyboardMarkup(row_width=1)
    callback_button = InlineKeyboardButton(text="Декан", callback_data='dekan_shcool_inovation')
    callback_button1 = InlineKeyboardButton(text="Преподаватели", callback_data='tutors_shcool_inovation')
    callback_button2 = InlineKeyboardButton(text="⬅ Назад", callback_data='tutors_university')
    markup.add(callback_button, callback_button1, callback_button2)
    return markup


def inline_keyboard_pps_shcool_bussines():
    markup = InlineKeyboardMarkup(row_width=1)
    callback_button = InlineKeyboardButton(text="Декан", callback_data='dekan_shcool_bussines')
    callback_button1 = InlineKeyboardButton(text="Преподаватели", callback_data='tutors_shcool_bussines')
    callback_button2 = InlineKeyboardButton(text="⬅ Назад", callback_data='tutors_university')
    markup.add(callback_button, callback_button1, callback_button2)
    return markup


def inline_keyboard_pps_shcool_economic():
    markup = InlineKeyboardMarkup(row_width=1)
    callback_button = InlineKeyboardButton(text="Декан", callback_data='dekan_shcool_economic')
    callback_button1 = InlineKeyboardButton(text="Преподаватели", callback_data='tutors_shcool_economic')
    callback_button2 = InlineKeyboardButton(text="⬅ Назад", callback_data='tutors_university')
    markup.add(callback_button, callback_button1, callback_button2)
    return markup


def inline_keyboard_pps_rectorat():
    markup = InlineKeyboardMarkup(row_width=1)
    callback_button = InlineKeyboardButton(text="Ректор", callback_data='rectorat_rector')
    callback_button1 = InlineKeyboardButton(text="Проректор", callback_data='rectorat_humans')
    callback_button2 = InlineKeyboardButton(text="⬅ Назад", callback_data='tutors_university')
    markup.add(callback_button, callback_button1, callback_button2)
    return markup


def inline_keyboard_pps_shcool_management_back():
    markup = InlineKeyboardMarkup(row_width=1)
    callback_button = InlineKeyboardButton(text="⬅ Назад", callback_data='shcool_management')
    markup.add(callback_button)
    return markup


def inline_keyboard_pps_shcool_law_back():
    markup = InlineKeyboardMarkup(row_width=1)
    callback_button = InlineKeyboardButton(text="⬅ Назад", callback_data='shcool_law')
    markup.add(callback_button)
    return markup


def inline_keyboard_pps_shcool_engineer_back():
    markup = InlineKeyboardMarkup(row_width=1)
    callback_button = InlineKeyboardButton(text="⬅ Назад", callback_data='shcool_engineer')
    markup.add(callback_button)
    return markup


def inline_keyboard_pps_shcool_inovation_back():
    markup = InlineKeyboardMarkup(row_width=1)
    callback_button = InlineKeyboardButton(text="⬅ Назад", callback_data='shcool_inovation')
    markup.add(callback_button)
    return markup


def inline_keyboard_pps_shcool_bussines_back():
    markup = InlineKeyboardMarkup(row_width=1)
    callback_button = InlineKeyboardButton(text="⬅ Назад", callback_data='shcool_bussines')
    markup.add(callback_button)
    return markup


def inline_keyboard_pps_shcool_economic_back():
    markup = InlineKeyboardMarkup(row_width=1)
    callback_button = InlineKeyboardButton(text="⬅ Назад", callback_data='shcool_economic')
    markup.add(callback_button)
    return markup


def inline_keyboard_pps_rectorat_back():
    markup = InlineKeyboardMarkup(row_width=1)
    callback_button = InlineKeyboardButton(text="⬅ Назад", callback_data='rectorat')
    markup.add(callback_button)
    return markup