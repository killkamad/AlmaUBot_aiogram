from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from utils import db_api as db
from .callback_datas import schedule_update_callback, schedule_delete_callback
from data.button_names.schedule_buttons import add_schedule_button, update_schedule_button, delete_schedule_button, cancel_send_schedule_button
from data.button_names.admin_menu_buttons import back_to_admin_menu_button, send_admin_button, edit_admin_button, \
                                                 delete_admin_button, cancel_admin_button


# Админ меню Расписания
def inline_keyboard_schedule_admin():
    markup = InlineKeyboardMarkup(row_width=1)
    callback_upload = InlineKeyboardButton(text=add_schedule_button, callback_data='send_schedule_bot')
    callback_update = InlineKeyboardButton(text=update_schedule_button, callback_data='update_schedule_bot')
    callback_delete = InlineKeyboardButton(text=delete_schedule_button, callback_data='delete_schedule_bot')
    callback_back = InlineKeyboardButton(text=back_to_admin_menu_button, callback_data='back_to_admin_menu')
    markup.add(callback_upload, callback_update, callback_delete, callback_back)
    return markup


# Расписание отправка или отмена
def cancel_or_send_schedule():
    markup = InlineKeyboardMarkup()
    callback_button = InlineKeyboardButton(text=send_admin_button, callback_data="send_schedule")
    callback_button2 = InlineKeyboardButton(text=cancel_admin_button, callback_data="cancel_schedule")
    markup.add(callback_button, callback_button2)
    return markup


# Расписание Изменение или отмена
def cancel_or_update_schedule():
    markup = InlineKeyboardMarkup()
    callback_button = InlineKeyboardButton(text=edit_admin_button, callback_data="update_schedule_button")
    callback_button2 = InlineKeyboardButton(text=cancel_admin_button, callback_data="cancel_update_schedule")
    markup.add(callback_button, callback_button2)
    return markup


# Расписание Удаление или отмена
def cancel_or_delete_schedule():
    markup = InlineKeyboardMarkup()
    callback_button = InlineKeyboardButton(text=delete_admin_button, callback_data="delete_schedule_button")
    callback_button2 = InlineKeyboardButton(text=cancel_admin_button, callback_data="cancel_delete_schedule")
    markup.add(callback_button, callback_button2)
    return markup


# Расписание динамические кнопки, для обновления
async def inline_keyboard_update_schedule():
    markup = InlineKeyboardMarkup(row_width=2)
    schedule = await db.aws_select_data_schedule()
    markup.add(*[InlineKeyboardButton(text=item['name_sched'],
                                      callback_data=schedule_update_callback.new(schedule_id=item["id"])) for
                 item in schedule])
    markup.add(InlineKeyboardButton(text=back_to_admin_menu_button, callback_data="cancel_update_step"))
    return markup


# Расписание динамические кнопки, для удаления
async def inline_keyboard_delete_schedule():
    markup = InlineKeyboardMarkup(row_width=2)
    schedule = await db.aws_select_data_schedule()
    markup.add(*[InlineKeyboardButton(text=item['name_sched'],
                                      callback_data=schedule_delete_callback.new(schedule_id=item["id"])) for
                 item in schedule])
    markup.add(InlineKeyboardButton(text=back_to_admin_menu_button, callback_data="cancel_delete_step"))
    return markup


# Расписание Отмена
def inline_keyboard_cancel_schedule():
    markup = InlineKeyboardMarkup()
    cancel_button = InlineKeyboardButton(text=cancel_send_schedule_button, callback_data="cancel_step_schedule")
    markup.add(cancel_button)
    return markup
