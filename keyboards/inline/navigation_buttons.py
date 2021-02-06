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
    markup.add(InlineKeyboardButton(text="⬅ Назад", callback_data="go_back"))
    return markup


def inline_keyboard_contacts_center_back():
    markup = InlineKeyboardMarkup(row_width=1)
    callback_button = InlineKeyboardButton(text="Назад", callback_data='contacts_center')
    markup.add(callback_button)
    return markup
