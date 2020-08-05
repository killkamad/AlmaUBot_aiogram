from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from utils import db_api as db
import logging


def inline_keyboard_admin():
    markup = InlineKeyboardMarkup()
    callback_button = InlineKeyboardButton(text="📣 Рассылка", callback_data='send_all')
    callback_button1 = InlineKeyboardButton(text="📤 Загрузить расписание", callback_data='send_schedule_bot')
    callback_button2 = InlineKeyboardButton(text="♻ Обновить расписание", callback_data='update_schedule_bot')
    callback_button3 = InlineKeyboardButton(text="❌ Удалить расписание", callback_data='delete_schedule_bot')
    markup.row(callback_button, callback_button1)
    markup.row(callback_button2, callback_button3)
    return markup


def inline_keyboard_massive_send_all():
    markup = InlineKeyboardMarkup()
    callback_button1 = InlineKeyboardButton(text="➕ Добавить фото или документ", callback_data="add_photo_mass")
    callback_button2 = InlineKeyboardButton(text="✔ Отправить", callback_data="send_send_to_all")
    callback_button3 = InlineKeyboardButton(text="❌ Отмена", callback_data="cancel")
    markup.row(callback_button1)
    markup.row(callback_button2, callback_button3)
    return markup


def inline_keyboard_cancel_or_send():
    markup = InlineKeyboardMarkup()
    callback_button = InlineKeyboardButton(text="✔ Отправить", callback_data="send_send_to_all")
    callback_button2 = InlineKeyboardButton(text="❌ Отмена", callback_data="cancel")
    markup.add(callback_button, callback_button2)
    return markup


def inline_keyboard_cancel():
    markup = InlineKeyboardMarkup()
    cancel_button = InlineKeyboardButton(text="❌ Отмена отправки расписания", callback_data="cancel_step")
    markup.add(cancel_button)
    return markup


def cancel_or_send_schedule():
    markup = InlineKeyboardMarkup()
    callback_button = InlineKeyboardButton(text="✔ Отправить", callback_data="send_schedule")
    callback_button2 = InlineKeyboardButton(text="❌ Отмена", callback_data="cancel_schedule")
    markup.add(callback_button, callback_button2)
    return markup


def cancel_or_update_schedule():
    markup = InlineKeyboardMarkup()
    callback_button = InlineKeyboardButton(text="✔ Изменить", callback_data="update_schedule_button")
    callback_button2 = InlineKeyboardButton(text="❌ Отмена", callback_data="cancel_update_schedule")
    markup.add(callback_button, callback_button2)
    return markup


def cancel_or_delete_schedule():
    markup = InlineKeyboardMarkup()
    callback_button = InlineKeyboardButton(text="✔ Удалить", callback_data="delete_schedule_button")
    callback_button2 = InlineKeyboardButton(text="❌ Отмена", callback_data="cancel_delete_schedule")
    markup.add(callback_button, callback_button2)
    return markup


async def inline_keyboard_update_schedule():
    markup = InlineKeyboardMarkup(row_width=3)
    schedule = await db.aws_select_data_schedule()
    call_list = []
    schedule_name = []
    for call_value in schedule:
        callback_data = "['upd_sch', '" + call_value[-1] + "']"
        schedule_name.append(call_value[3])
        # logging.info(callback_data)
        call_list.append(callback_data)
    markup.add(*[InlineKeyboardButton(text=button, callback_data=call_data) for button, call_data in
                 zip(schedule_name, call_list)])
    markup.add(InlineKeyboardButton(text="🔙 Назад", callback_data="cancel_update_step"))
    return markup


async def inline_keyboard_delete_schedule():
    markup = InlineKeyboardMarkup(row_width=3)
    schedule = await db.aws_select_data_schedule()
    call_list = []
    schedule_name = []
    for call_value in schedule:
        callback_data = "['del_sch', '" + call_value[-1] + "']"
        schedule_name.append(call_value[3])
        # logging.info(callback_data)
        call_list.append(callback_data)
    markup.add(*[InlineKeyboardButton(text=button, callback_data=call_data) for button, call_data in
                 zip(schedule_name, call_list)])
    markup.add(InlineKeyboardButton(text="🔙 Назад", callback_data="cancel_delete_step"))
    return markup
