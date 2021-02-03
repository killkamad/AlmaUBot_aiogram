from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from utils import db_api as db
import logging


def inline_keyboard_admin():
    markup = InlineKeyboardMarkup(row_width=1)
    callback_sending = InlineKeyboardButton(text="📣 Рассылка", callback_data='send_all')
    callback_schedule = InlineKeyboardButton(text="📅 Расписание", callback_data='schedule_admin_menu')
    callback_almaushop = InlineKeyboardButton(text="🌀 Меню AlmaU Shop", callback_data='almaushop_admin_menu')
    callback_calendar = InlineKeyboardButton(text="🗒 Обновить Академический Календарь",
                                             callback_data='send_academic_calendar')
    markup.add(callback_sending, callback_schedule, callback_almaushop, callback_calendar)
    return markup


# Админ меню AlmaU Shop
def inline_keyboard_almau_shop_admin():
    markup = InlineKeyboardMarkup(row_width=1)
    callback_merch = InlineKeyboardButton(text="👔 Обновить мерч", callback_data='update_almaushop_merch')
    callback_books = InlineKeyboardButton(text="📚 Обновить книги", callback_data='update_almaushop_books')
    callback_faq = InlineKeyboardButton(text="⁉ Добавить вопрос FAQ", callback_data='add_faq_question_almaushop')
    callback_back = InlineKeyboardButton(text="⬅ Назад", callback_data='back_to_admin_menu')
    markup.add(callback_merch, callback_books, callback_faq, callback_back)
    return markup


# Админ меню Расписания
def inline_keyboard_schedule_admin():
    markup = InlineKeyboardMarkup(row_width=1)
    callback_upload = InlineKeyboardButton(text="📤 Загрузить расписание", callback_data='send_schedule_bot')
    callback_update = InlineKeyboardButton(text="♻ Обновить расписание", callback_data='update_schedule_bot')
    callback_delete = InlineKeyboardButton(text="❌ Удалить расписание", callback_data='delete_schedule_bot')
    callback_back = InlineKeyboardButton(text="⬅ Назад", callback_data='back_to_admin_menu')
    markup.add(callback_upload, callback_update, callback_delete, callback_back)
    return markup


def inline_keyboard_massive_send_all():
    markup = InlineKeyboardMarkup()
    callback_button1 = InlineKeyboardButton(text="➕ Добавить фото или документ", callback_data="add_photo_mass")
    callback_button2 = InlineKeyboardButton(text="✅ Отправить", callback_data="send_send_to_all")
    callback_button3 = InlineKeyboardButton(text="❌ Отмена", callback_data="cancel")
    markup.row(callback_button1)
    markup.row(callback_button2, callback_button3)
    return markup


def inline_keyboard_cancel_or_send():
    markup = InlineKeyboardMarkup()
    callback_button = InlineKeyboardButton(text="✅ Отправить", callback_data="send_send_to_all")
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
    callback_button = InlineKeyboardButton(text="✅ Отправить", callback_data="send_schedule")
    callback_button2 = InlineKeyboardButton(text="❌ Отмена", callback_data="cancel_schedule")
    markup.add(callback_button, callback_button2)
    return markup


def cancel_or_update_schedule():
    markup = InlineKeyboardMarkup()
    callback_button = InlineKeyboardButton(text="✅ Изменить", callback_data="update_schedule_button")
    callback_button2 = InlineKeyboardButton(text="❌ Отмена", callback_data="cancel_update_schedule")
    markup.add(callback_button, callback_button2)
    return markup


def cancel_or_delete_schedule():
    markup = InlineKeyboardMarkup()
    callback_button = InlineKeyboardButton(text="✅ Удалить", callback_data="delete_schedule_button")
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
    markup.add(InlineKeyboardButton(text="⬅ Назад", callback_data="cancel_update_step"))
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
    markup.add(InlineKeyboardButton(text="⬅ Назад", callback_data="cancel_delete_step"))
    return markup


def cancel_academic_calendar():
    markup = InlineKeyboardMarkup()
    cancel_button = InlineKeyboardButton(text="❌ Отмена", callback_data="cancel_step_academic_calendar")
    markup.add(cancel_button)
    return markup


def cancel_or_send_academic_calendar():
    markup = InlineKeyboardMarkup()
    callback_button = InlineKeyboardButton(text="✅ Отправить", callback_data="send_academic_calendar_to_base")
    callback_button2 = InlineKeyboardButton(text="❌ Отмена", callback_data="cancel_academic_calendar")
    markup.add(callback_button, callback_button2)
    return markup
