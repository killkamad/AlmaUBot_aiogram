from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from utils import db_api as db
from .callback_datas import schedule_update_callback, schedule_delete_callback


# Админ меню Расписания
def inline_keyboard_schedule_admin():
    markup = InlineKeyboardMarkup(row_width=1)
    callback_upload = InlineKeyboardButton(text="📤 Добавить расписание", callback_data='send_schedule_bot')
    callback_update = InlineKeyboardButton(text="♻ Обновить расписание", callback_data='update_schedule_bot')
    callback_delete = InlineKeyboardButton(text="❌ Удалить расписание", callback_data='delete_schedule_bot')
    callback_back = InlineKeyboardButton(text="⬅ Назад", callback_data='back_to_admin_menu')
    markup.add(callback_upload, callback_update, callback_delete, callback_back)
    return markup


# Расписание отправка или отмена
def cancel_or_send_schedule():
    markup = InlineKeyboardMarkup()
    callback_button = InlineKeyboardButton(text="✅ Отправить", callback_data="send_schedule")
    callback_button2 = InlineKeyboardButton(text="❌ Отмена", callback_data="cancel_schedule")
    markup.add(callback_button, callback_button2)
    return markup


# Расписание Изменение или отмена
def cancel_or_update_schedule():
    markup = InlineKeyboardMarkup()
    callback_button = InlineKeyboardButton(text="✅ Изменить", callback_data="update_schedule_button")
    callback_button2 = InlineKeyboardButton(text="❌ Отмена", callback_data="cancel_update_schedule")
    markup.add(callback_button, callback_button2)
    return markup


# Расписание Удаление или отмена
def cancel_or_delete_schedule():
    markup = InlineKeyboardMarkup()
    callback_button = InlineKeyboardButton(text="✅ Удалить", callback_data="delete_schedule_button")
    callback_button2 = InlineKeyboardButton(text="❌ Отмена", callback_data="cancel_delete_schedule")
    markup.add(callback_button, callback_button2)
    return markup


# Расписание динамические кнопки, для обновления
async def inline_keyboard_update_schedule():
    markup = InlineKeyboardMarkup(row_width=2)
    schedule = await db.aws_select_data_schedule()
    markup.add(*[InlineKeyboardButton(text=item['name_sched'],
                                      callback_data=schedule_update_callback.new(schedule_id=item["id"])) for
                 item in schedule])
    markup.add(InlineKeyboardButton(text="⬅ Назад", callback_data="cancel_update_step"))
    return markup


# Расписание динамические кнопки, для удаления
async def inline_keyboard_delete_schedule():
    markup = InlineKeyboardMarkup(row_width=2)
    schedule = await db.aws_select_data_schedule()
    markup.add(*[InlineKeyboardButton(text=item['name_sched'],
                                      callback_data=schedule_delete_callback.new(schedule_id=item["id"])) for
                 item in schedule])
    markup.add(InlineKeyboardButton(text="⬅ Назад", callback_data="cancel_delete_step"))
    return markup


# Расписание Отмена
def inline_keyboard_cancel_schedule():
    markup = InlineKeyboardMarkup()
    cancel_button = InlineKeyboardButton(text="❌ Отмена отправки расписания", callback_data="cancel_step_schedule")
    markup.add(cancel_button)
    return markup
