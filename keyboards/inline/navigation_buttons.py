from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from utils import db_api as db

from .callback_datas import cabinet_callback, nav_center_callback

def inline_keyboard_nav_unifi():
    markup = InlineKeyboardMarkup(row_width=1)
    callback_button = InlineKeyboardButton(text="Карта-навигация по университету ", callback_data='map_nav')
    callback_button1 = InlineKeyboardButton(text="Контакты ключевых центров", callback_data='contacts_center')
    callback_button2 = InlineKeyboardButton(text="Профессорско-преподавательский состав",
                                            callback_data='tutors_university')
    callback_button3 = InlineKeyboardButton(text="⬅ Назад", callback_data="go_back")
    markup.add(callback_button, callback_button1, callback_button2, callback_button3)
    return markup


# async def inline_keyboard_contacts_center():
#     markup = InlineKeyboardMarkup(row_width=1)
#     schedule = await db.select_data_contact_centers()
#     call_list = []
#     name = []
#     for call_value in schedule:
#         callback_data = "['contacts_center_call', '" + call_value[-1] + "']"
#         name.append(call_value[3])
#         call_list.append(callback_data)
#     markup.add(*[InlineKeyboardButton(text=button, callback_data=call_data) for button, call_data in
#                  zip(name, call_list)])
#     markup.add(InlineKeyboardButton(text="⬅ Назад", callback_data="/nav_unifi"))
#     return markup


async def inline_keyboard_contacts_center():
    markup = InlineKeyboardMarkup(row_width=2)
    ceneters = await db.select_data_contact_centers()
    markup.add(
        *[InlineKeyboardButton(text=item['name_contact_center'], callback_data=nav_center_callback.new(name=item["name_contact_center"]))
          for item in ceneters])
    markup.add(InlineKeyboardButton(text="⬅ Назад", callback_data="/nav_unifi"))
    return markup


def inline_keyboard_contacts_center_back():
    markup = InlineKeyboardMarkup(row_width=1)
    callback_button = InlineKeyboardButton(text="⬅ Назад", callback_data='contacts_center')
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


# кнопки карт навигации
def inline_keyboard_map_nav():
    markup = InlineKeyboardMarkup(row_width=1)
    callback_button = InlineKeyboardButton(text="Старое здание университета", callback_data='old_building')
    callback_button1 = InlineKeyboardButton(text="Новое здание университет", callback_data='new_building')
    callback_button2 = InlineKeyboardButton(text="⬅ Назад", callback_data="/nav_unifi")
    markup.add(callback_button, callback_button1, callback_button2)
    return markup


def inline_keyboard_new_building():
    markup = InlineKeyboardMarkup(row_width=1)
    callback_button = InlineKeyboardButton(text="1 этаж", callback_data='new_building_first')
    callback_button1 = InlineKeyboardButton(text="2 этаж", callback_data='new_building_second')
    callback_button2 = InlineKeyboardButton(text="3 этаж", callback_data='new_building_third')
    callback_button3 = InlineKeyboardButton(text="4 этаж", callback_data='new_building_fourth')
    callback_button4 = InlineKeyboardButton(text="5 этаж", callback_data='new_building_fifth')
    callback_button5 = InlineKeyboardButton(text="6 этаж", callback_data='new_building_sixth')
    callback_button6 = InlineKeyboardButton(text="⬅ Назад", callback_data="map_nav")
    markup.add(callback_button, callback_button1, callback_button2, callback_button3, callback_button4, callback_button5, callback_button6)
    return markup

def inline_keyboard_old_building():
    markup = InlineKeyboardMarkup(row_width=1)
    callback_button = InlineKeyboardButton(text="1 этаж", callback_data='old_building_first')
    callback_button1 = InlineKeyboardButton(text="2 этаж", callback_data='old_building_second')
    callback_button2 = InlineKeyboardButton(text="3 этаж", callback_data='old_building_third')
    callback_button3 = InlineKeyboardButton(text="4 этаж", callback_data='old_building_fourth')
    callback_button4 = InlineKeyboardButton(text="⬅ Назад", callback_data="map_nav")
    markup.add(callback_button, callback_button1, callback_button2, callback_button3, callback_button4)
    return markup


#кнопки перехода
def inline_keyboard_new_building_back():
    markup = InlineKeyboardMarkup(row_width=1)
    callback_button = InlineKeyboardButton(text="⬅ В новое здание", callback_data="new_building")
    markup.add(callback_button)
    return markup


def inline_keyboard_old_building_back():
    markup = InlineKeyboardMarkup(row_width=1)
    callback_button = InlineKeyboardButton(text="⬅ В старое здание", callback_data="old_building")
    callback_button1 = InlineKeyboardButton(text="⬅ В новое здание", callback_data="new_building")
    markup.add(callback_button, callback_button1)
    return markup


#кнопки кабинетов нового здания
async def inline_keyboard_cabinets_first_new():
    markup = InlineKeyboardMarkup(row_width=3)
    building = "Новое здание"
    floor = "1 этаж"
    mapnav = await db.map_nav_description(building, floor)
    markup.add(*[InlineKeyboardButton(text=item['cabinet'], callback_data=cabinet_callback.new(cabinet=item["cabinet"])) for item in mapnav])
    markup.add(InlineKeyboardButton(text="⬅ Назад", callback_data="new_building"))
    return markup

async def inline_keyboard_cabinets_second_new():
    markup = InlineKeyboardMarkup(row_width=3)
    building = "Новое здание"
    floor = "2 этаж"
    mapnav = await db.map_nav_description(building, floor)
    markup.add(*[InlineKeyboardButton(text=item['cabinet'], callback_data=cabinet_callback.new(cabinet=item["cabinet"])) for item in mapnav])
    markup.add(InlineKeyboardButton(text="⬅ Назад", callback_data="new_building"))
    return markup


async def inline_keyboard_cabinets_third_new():
    markup = InlineKeyboardMarkup(row_width=3)
    building = "Новое здание"
    floor = "3 этаж"
    mapnav = await db.map_nav_description(building, floor)
    markup.add(*[InlineKeyboardButton(text=item['cabinet'], callback_data=cabinet_callback.new(cabinet=item["cabinet"])) for item in mapnav])
    markup.add(InlineKeyboardButton(text="⬅ Назад", callback_data="new_building"))
    return markup


async def inline_keyboard_cabinets_fourth_new():
    markup = InlineKeyboardMarkup(row_width=3)
    building = "Новое здание"
    floor = "4 этаж"
    mapnav = await db.map_nav_description(building, floor)
    markup.add(*[InlineKeyboardButton(text=item['cabinet'], callback_data=cabinet_callback.new(cabinet=item["cabinet"])) for item in mapnav])
    markup.add(InlineKeyboardButton(text="⬅ Назад", callback_data="new_building"))
    return markup


async def inline_keyboard_cabinets_fifth_new():
    markup = InlineKeyboardMarkup(row_width=3)
    building = "Новое здание"
    floor = "5 этаж"
    mapnav = await db.map_nav_description(building, floor)
    markup.add(*[InlineKeyboardButton(text=item['cabinet'], callback_data=cabinet_callback.new(cabinet=item["cabinet"])) for item in mapnav])
    markup.add(InlineKeyboardButton(text="⬅ Назад", callback_data="new_building"))
    return markup


async def inline_keyboard_cabinets_sixth_new():
    markup = InlineKeyboardMarkup(row_width=3)
    building = "Новое здание"
    floor = "6 этаж"
    mapnav = await db.map_nav_description(building, floor)
    markup.add(*[InlineKeyboardButton(text=item['cabinet'], callback_data=cabinet_callback.new(cabinet=item["cabinet"])) for item in mapnav])
    markup.add(InlineKeyboardButton(text="⬅ Назад", callback_data="new_building"))
    return markup


#кнопки кабинетов старого здания
async def inline_keyboard_cabinets_first_old():
    markup = InlineKeyboardMarkup(row_width=3)
    building = "Старое здание"
    floor = "1 этаж"
    mapnav = await db.map_nav_description(building, floor)
    markup.add(*[InlineKeyboardButton(text=item['cabinet'], callback_data=cabinet_callback.new(cabinet=item["cabinet"])) for item in mapnav])
    markup.add(InlineKeyboardButton(text="⬅ Назад", callback_data="old_building"))
    return markup

async def inline_keyboard_cabinets_second_old():
    markup = InlineKeyboardMarkup(row_width=3)
    building = "Старое здание"
    floor = "2 этаж"
    mapnav = await db.map_nav_description(building, floor)
    markup.add(*[InlineKeyboardButton(text=item['cabinet'], callback_data=cabinet_callback.new(cabinet=item["cabinet"])) for item in mapnav])
    markup.add(InlineKeyboardButton(text="⬅ Назад", callback_data="old_building"))
    return markup


async def inline_keyboard_cabinets_third_old():
    markup = InlineKeyboardMarkup(row_width=3)
    building = "Старое здание"
    floor = "3 этаж"
    mapnav = await db.map_nav_description(building, floor)
    markup.add(*[InlineKeyboardButton(text=item['cabinet'], callback_data=cabinet_callback.new(cabinet=item["cabinet"])) for item in mapnav])
    markup.add(InlineKeyboardButton(text="⬅ Назад", callback_data="old_building"))
    return markup


async def inline_keyboard_cabinets_fourth_old():
    markup = InlineKeyboardMarkup(row_width=3)
    building = "Старое здание"
    floor = "4 этаж"
    mapnav = await db.map_nav_description(building, floor)
    markup.add(*[InlineKeyboardButton(text=item['cabinet'], callback_data=cabinet_callback.new(cabinet=item["cabinet"])) for item in mapnav])
    markup.add(InlineKeyboardButton(text="⬅ Назад", callback_data="old_building"))
    return markup