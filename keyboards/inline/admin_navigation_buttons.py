from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from data.config import floor_1, floor_2, floor_3, floor_4, floor_5, floor_6, navigation_university, contact_centers, \
    tutors_university, old_building, new_building
from utils import db_api as db
import logging
from .callback_datas import cabinet_callback_update, nav_center_callback_update, nav_center_callback_delete


def inline_keyboard_nav_university_admin_menu():
    markup = InlineKeyboardMarkup(row_width=1)
    callback_button = InlineKeyboardButton(text=navigation_university, callback_data='map_nav_admin')
    callback_button1 = InlineKeyboardButton(text=contact_centers, callback_data='contacts_center_admin')
    callback_button2 = InlineKeyboardButton(text=tutors_university, callback_data='tutors_university_admin')
    callback_button3 = InlineKeyboardButton(text="⬅ Назад", callback_data="back_to_admin_menu")
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
    centers = await db.select_data_contact_centers()
    markup.add(
        *[InlineKeyboardButton(text=item['name_contact_center'],
                               callback_data=nav_center_callback_update.new(id=item["id"]))
          for item in centers])
    markup.add(InlineKeyboardButton(text="⬅ Назад", callback_data="cancel_step_contact_center_admin"))
    return markup


def cancel_or_update_contact_center_admin():
    markup = InlineKeyboardMarkup()
    callback_button = InlineKeyboardButton(text="✅ Изменить", callback_data="update_info_contact_center_admin")
    callback_button2 = InlineKeyboardButton(text="❌ Отмена", callback_data="cancel_step_contact_center_admin")
    markup.add(callback_button, callback_button2)
    return markup


async def inline_keyboard_contacts_center_delete():
    markup = InlineKeyboardMarkup(row_width=1)
    centers = await db.select_data_contact_centers()
    markup.add(
        *[InlineKeyboardButton(text=item['name_contact_center'],
                               callback_data=nav_center_callback_delete.new(id=item["id"]))
          for item in centers])
    markup.add(InlineKeyboardButton(text="⬅ Назад", callback_data="cancel_step_contact_center_admin"))
    return markup


def cancel_or_delete_contact_center_admin():
    markup = InlineKeyboardMarkup()
    callback_button = InlineKeyboardButton(text="✅ Удалить", callback_data="delete_info_contact_center_admin")
    callback_button2 = InlineKeyboardButton(text="⬅ Назад", callback_data="cancel_step_contact_center_admin")
    markup.add(callback_button, callback_button2)
    return markup


def inline_keyboard_cancel_contact_center_admin():
    markup = InlineKeyboardMarkup()
    cancel_button = InlineKeyboardButton(text="❌ Отмена", callback_data="cancel_step_contact_center_admin")
    markup.add(cancel_button)
    return markup


def cancel_or_send_tutors_management():
    markup = InlineKeyboardMarkup()
    callback_button = InlineKeyboardButton(text="✅ Отправить", callback_data="send_tutors_management")
    callback_button2 = InlineKeyboardButton(text="❌ Отмена", callback_data="cancel_step_tutors_admin")
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


def cancel_or_send_or_image_map_nav_admin():
    markup = InlineKeyboardMarkup(row_width=1)
    callback_button1 = InlineKeyboardButton(text="➕ Прикрепить фото", callback_data="send_image_navigation_admin")
    callback_button2 = InlineKeyboardButton(text="✅ Отправить без фото", callback_data="send_map_navigation_admin")
    callback_button3 = InlineKeyboardButton(text="❌ Отмена", callback_data="cancel_step_map_nav_admin")
    markup.add(callback_button1, callback_button2, callback_button3)
    return markup


def cancel_or_send_map_nav_admin():
    markup = InlineKeyboardMarkup(row_width=1)
    callback_button2 = InlineKeyboardButton(text="✅ Отправить", callback_data="send_map_navigation_admin")
    callback_button3 = InlineKeyboardButton(text="❌ Отмена", callback_data="cancel_step_map_nav_admin")
    markup.add(callback_button2, callback_button3)
    return markup


async def inline_keyboard_cabinets_admin(building, floor):
    markup = InlineKeyboardMarkup(row_width=2)
    map_navigation = await db.map_nav_description(building, floor)
    markup.add(
        *[InlineKeyboardButton(text=item['cabinet'], callback_data=cabinet_callback_update.new(cabinet=item["cabinet"]))
          for item in map_navigation])
    markup.add(InlineKeyboardButton(text="⬅ Назад", callback_data="cancel_step_map_nav_admin"))
    return markup


def cancel_or_update_map_nav_admin():
    markup = InlineKeyboardMarkup()
    callback_button = InlineKeyboardButton(text="✅ Изменить", callback_data="update_map_navigation_admin")
    callback_button2 = InlineKeyboardButton(text="❌ Отмена", callback_data="cancel_step_map_nav_admin")
    markup.add(callback_button, callback_button2)
    return markup


def cancel_or_description_or_image_map_nav_admin():
    markup = InlineKeyboardMarkup(row_width=1)
    callback_button = InlineKeyboardButton(text="➕ Прикрепить или изменить фото",
                                           callback_data="update_image_navigation_admin")
    callback_button1 = InlineKeyboardButton(text="✅ Изменить описание", callback_data="update_description_state")
    callback_button2 = InlineKeyboardButton(text="❌ Отмена", callback_data="cancel_step_map_nav_admin")
    markup.add(callback_button, callback_button1, callback_button2)
    return markup


def cancel_or_description_or_send_map_nav_admin():
    markup = InlineKeyboardMarkup(row_width=1)
    callback_button = InlineKeyboardButton(text="♻ Изменить описание", callback_data="update_description_state")
    callback_button1 = InlineKeyboardButton(text="✅ Отправить фото", callback_data="update_photo_map_navigation_admin")
    callback_button2 = InlineKeyboardButton(text="❌ Отмена", callback_data="cancel_step_map_nav_admin")
    markup.add(callback_button, callback_button1, callback_button2)
    return markup


def cancel_or_update_or_image_map_nav_admin():
    markup = InlineKeyboardMarkup(row_width=1)
    callback_button = InlineKeyboardButton(text="➕ Прикрепить или изменить фото",
                                           callback_data="update_image_navigation_admin")
    callback_button1 = InlineKeyboardButton(text="✅ Отправить изменения описания", callback_data="update_map_navigation_admin")
    callback_button2 = InlineKeyboardButton(text="❌ Отмена", callback_data="cancel_step_map_nav_admin")
    markup.add(callback_button, callback_button1, callback_button2)
    return markup


def cancel_or_delete_map_nav_admin():
    markup = InlineKeyboardMarkup()
    callback_button = InlineKeyboardButton(text="✅ Удалить", callback_data="delete_map_navigation_admin")
    callback_button2 = InlineKeyboardButton(text="❌ Отмена", callback_data="cancel_step_map_nav_admin")
    markup.add(callback_button, callback_button2)
    return markup


def inline_keyboard_cancel_map_nav_admin():
    markup = InlineKeyboardMarkup()
    cancel_button = InlineKeyboardButton(text="❌ Отмена", callback_data="cancel_step_map_nav_admin")
    markup.add(cancel_button)
    return markup


def keyboard_map_nav_choice_building():
    markup = InlineKeyboardMarkup(row_width=1)
    callback_button = InlineKeyboardButton(text=old_building, callback_data="old_building_choice_admin")
    callback_button2 = InlineKeyboardButton(text=new_building, callback_data="new_building_choice_admin")
    callback_button3 = InlineKeyboardButton(text="⬅ Назад", callback_data="cancel_step_map_nav_admin")
    markup.add(callback_button, callback_button2, callback_button3)
    return markup


def map_nav_admin_choice_floor_old():
    markup = InlineKeyboardMarkup(row_width=1)
    callback_button1 = InlineKeyboardButton(text=floor_1, callback_data="floor_choice_admin1")
    callback_button2 = InlineKeyboardButton(text=floor_2, callback_data="floor_choice_admin2")
    callback_button3 = InlineKeyboardButton(text=floor_3, callback_data="floor_choice_admin3")
    callback_button4 = InlineKeyboardButton(text=floor_4, callback_data="floor_choice_admin4")
    callback_button5 = InlineKeyboardButton(text="⬅ Назад", callback_data="cancel_step_map_nav_admin")
    markup.add(callback_button1, callback_button2, callback_button3, callback_button4, callback_button5)
    return markup


def map_nav_admin_choice_floor_new():
    markup = InlineKeyboardMarkup(row_width=1)
    callback_button1 = InlineKeyboardButton(text=floor_1, callback_data="floor_choice_admin1")
    callback_button2 = InlineKeyboardButton(text=floor_2, callback_data="floor_choice_admin2")
    callback_button3 = InlineKeyboardButton(text=floor_3, callback_data="floor_choice_admin3")
    callback_button4 = InlineKeyboardButton(text=floor_4, callback_data="floor_choice_admin4")
    callback_button5 = InlineKeyboardButton(text=floor_5, callback_data="floor_choice_admin5")
    callback_button6 = InlineKeyboardButton(text=floor_6, callback_data="floor_choice_admin6")
    callback_button7 = InlineKeyboardButton(text="⬅ Назад", callback_data="cancel_step_map_nav_admin")
    markup.add(callback_button1, callback_button2, callback_button3, callback_button4, callback_button5,
               callback_button6, callback_button7)
    return markup


def map_nav_admin_choice_floor_old_update():
    markup = InlineKeyboardMarkup(row_width=1)
    callback_button1 = InlineKeyboardButton(text=floor_1, callback_data="floor_choice_admin_update1")
    callback_button2 = InlineKeyboardButton(text=floor_2, callback_data="floor_choice_admin_update2")
    callback_button3 = InlineKeyboardButton(text=floor_3, callback_data="floor_choice_admin_update3")
    callback_button4 = InlineKeyboardButton(text=floor_4, callback_data="floor_choice_admin_update4")
    callback_button5 = InlineKeyboardButton(text="⬅ Назад", callback_data="cancel_step_map_nav_admin")
    markup.add(callback_button1, callback_button2, callback_button3, callback_button4, callback_button5)
    return markup


def map_nav_admin_choice_floor_new_update():
    markup = InlineKeyboardMarkup(row_width=1)
    callback_button1 = InlineKeyboardButton(text=floor_1, callback_data="floor_choice_admin_update1")
    callback_button2 = InlineKeyboardButton(text=floor_2, callback_data="floor_choice_admin_update2")
    callback_button3 = InlineKeyboardButton(text=floor_3, callback_data="floor_choice_admin_update3")
    callback_button4 = InlineKeyboardButton(text=floor_4, callback_data="floor_choice_admin_update4")
    callback_button5 = InlineKeyboardButton(text=floor_5, callback_data="floor_choice_admin_update5")
    callback_button6 = InlineKeyboardButton(text=floor_6, callback_data="floor_choice_admin_update6")
    callback_button7 = InlineKeyboardButton(text="⬅ Назад", callback_data="cancel_step_map_nav_admin")
    markup.add(callback_button1, callback_button2, callback_button3, callback_button4, callback_button5,
               callback_button6, callback_button7)
    return markup


def keyboard_map_nav_choice_building_update():
    markup = InlineKeyboardMarkup(row_width=1)
    callback_button = InlineKeyboardButton(text=old_building, callback_data="old_building_choice_admin_update")
    callback_button2 = InlineKeyboardButton(text=new_building, callback_data="new_building_choice_admin_update")
    callback_button3 = InlineKeyboardButton(text="⬅ Назад", callback_data="cancel_step_map_nav_admin")
    markup.add(callback_button, callback_button2, callback_button3)
    return markup


def keyboard_map_nav_choice_building_delete():
    markup = InlineKeyboardMarkup(row_width=1)
    callback_button = InlineKeyboardButton(text=old_building, callback_data="old_building_choice_admin_delete")
    callback_button2 = InlineKeyboardButton(text=new_building, callback_data="new_building_choice_admin_delete")
    callback_button3 = InlineKeyboardButton(text="⬅ Назад", callback_data="cancel_step_map_nav_admin")
    markup.add(callback_button, callback_button2, callback_button3)
    return markup


def map_nav_admin_choice_floor_old_delete():
    markup = InlineKeyboardMarkup(row_width=1)
    callback_button1 = InlineKeyboardButton(text=floor_1, callback_data="floor_choice_admin_delete1")
    callback_button2 = InlineKeyboardButton(text=floor_2, callback_data="floor_choice_admin_delete2")
    callback_button3 = InlineKeyboardButton(text=floor_3, callback_data="floor_choice_admin_delete3")
    callback_button4 = InlineKeyboardButton(text=floor_4, callback_data="floor_choice_admin_delete4")
    callback_button5 = InlineKeyboardButton(text="⬅ Назад", callback_data="cancel_step_map_nav_admin")
    markup.add(callback_button1, callback_button2, callback_button3, callback_button4, callback_button5)
    return markup


def map_nav_admin_choice_floor_new_delete():
    markup = InlineKeyboardMarkup(row_width=1)
    callback_button1 = InlineKeyboardButton(text=floor_1, callback_data="floor_choice_admin_delete1")
    callback_button2 = InlineKeyboardButton(text=floor_2, callback_data="floor_choice_admin_delete2")
    callback_button3 = InlineKeyboardButton(text=floor_3, callback_data="floor_choice_admin_delete3")
    callback_button4 = InlineKeyboardButton(text=floor_4, callback_data="floor_choice_admin_delete4")
    callback_button5 = InlineKeyboardButton(text=floor_5, callback_data="floor_choice_admin_delete5")
    callback_button6 = InlineKeyboardButton(text=floor_6, callback_data="floor_choice_admin_delete6")
    callback_button7 = InlineKeyboardButton(text="⬅ Назад", callback_data="cancel_step_map_nav_admin")
    markup.add(callback_button1, callback_button2, callback_button3, callback_button4, callback_button5,
               callback_button6, callback_button7)
    return markup


def keyboard_pps_choice_position():
    markup = InlineKeyboardMarkup(row_width=1)
    callback_button1 = InlineKeyboardButton(text="Декан", callback_data="choice_position_admin1")
    callback_button2 = InlineKeyboardButton(text="Преподаватели", callback_data="choice_position_admin2")
    callback_button3 = InlineKeyboardButton(text="⬅ Назад", callback_data="cancel_step_tutors_admin")
    markup.add(callback_button1, callback_button2, callback_button3)
    return markup


def keyboard_pps_choice_position_rector():
    markup = InlineKeyboardMarkup(row_width=1)
    callback_button1 = InlineKeyboardButton(text="Ректор", callback_data="choice_position_admin3")
    callback_button2 = InlineKeyboardButton(text="Проректоры", callback_data="choice_position_admin4")
    callback_button3 = InlineKeyboardButton(text="⬅ Назад", callback_data="cancel_step_tutors_admin")
    markup.add(callback_button1, callback_button2, callback_button3)
    return markup


def keyboard_pps_choice_shcool():
    markup = InlineKeyboardMarkup(row_width=1)
    callback_button1 = InlineKeyboardButton(text="Школа менеджмента", callback_data="choice_shcool_admin1")
    callback_button2 = InlineKeyboardButton(text="Школа политики и права", callback_data="choice_shcool_admin2")
    callback_button3 = InlineKeyboardButton(text="Школа Инженерного Менеджмента", callback_data="choice_shcool_admin3")
    callback_button4 = InlineKeyboardButton(text="Школа предпринимательства и инноваций",
                                            callback_data="choice_shcool_admin4")
    callback_button5 = InlineKeyboardButton(text="Высшая Школа Бизнеса", callback_data="choice_shcool_admin5")
    callback_button6 = InlineKeyboardButton(text="Школа Экономики и Финансов", callback_data="choice_shcool_admin6")
    callback_button7 = InlineKeyboardButton(text="Ректорат", callback_data="choice_rectorat_admin")
    callback_button8 = InlineKeyboardButton(text="⬅ Назад", callback_data="nav_university_admin_menu")
    markup.add(callback_button1, callback_button2, callback_button3, callback_button4, callback_button5,
               callback_button6, callback_button7, callback_button8)
    return markup


def inline_keyboard_cancel_tutors_admin():
    markup = InlineKeyboardMarkup()
    cancel_button = InlineKeyboardButton(text="❌ Отмена", callback_data="cancel_step_tutors_admin")
    markup.add(cancel_button)
    return markup
