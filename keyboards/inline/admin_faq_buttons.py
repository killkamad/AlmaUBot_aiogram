from math import ceil

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from keyboards.inline.callback_datas import main_faq_edit_callback, main_faq_delete_callback
from utils import db_api as db


# Админ меню FAQ
def inline_keyboard_faq_admin():
    markup = InlineKeyboardMarkup(row_width=1)
    callback_faq_add = InlineKeyboardButton(text="➕ Добавить FAQ", callback_data='add_main_faq')
    callback_faq_edit = InlineKeyboardButton(text="♻ Изменить FAQ", callback_data='edit_main_faq')
    callback_faq_delete = InlineKeyboardButton(text="❌ Удалить FAQ", callback_data='delete_main_faq')
    callback_back = InlineKeyboardButton(text="⬅ Назад", callback_data='back_to_admin_menu')
    markup.add(callback_faq_add, callback_faq_edit, callback_faq_delete, callback_back)
    return markup


# FAQ главного меню сохранить или отмена
def inline_keyboard_add_main_faq_or_cancel():
    markup = InlineKeyboardMarkup()
    callback_button = InlineKeyboardButton(text="✅ Сохранить", callback_data="save_main_faq")
    callback_button2 = InlineKeyboardButton(text="❌ Отмена", callback_data="cancel_main_faq")
    markup.add(callback_button, callback_button2)
    return markup


# FAQ главного меню удаление
async def inline_keyboard_delete_main_faq(page):
    max_pages = (ceil(await db.main_faq_count() / 10))
    count_rows = await db.main_faq_count()
    markup = InlineKeyboardMarkup(row_width=1)
    faq_questions = await db.main_faq_select_data(page)
    markup.add(
        *[InlineKeyboardButton(text=item["question"],
                               callback_data=main_faq_delete_callback.new(callback_id=item["id"]))
          for item in faq_questions])
    if (page < max_pages) and (count_rows > 10):
        if page != 0:
            previous_page = InlineKeyboardButton(text=f"⏪ Страница {page}", callback_data="main_faq_prev_delete")
        else:
            previous_page = InlineKeyboardButton(text=f"⏪", callback_data="main_faq_prev_delete")
        if page + 1 >= max_pages:
            next_page = InlineKeyboardButton(text=f"⏩", callback_data="main_faq_next_delete")
        else:
            next_page = InlineKeyboardButton(text=f"⏩ Страница {page + 2}", callback_data="main_faq_next_delete")
        markup.row(previous_page, next_page)
    markup.add(InlineKeyboardButton(text="⬅ Назад", callback_data="back_to_admin_faq"))
    return markup


# FAQ главного меню изменение
async def inline_keyboard_edit_main_faq(page):
    max_pages = (ceil(await db.main_faq_count() / 10))
    count_rows = await db.main_faq_count()
    markup = InlineKeyboardMarkup(row_width=1)
    faq_questions = await db.main_faq_select_data(page)
    markup.add(
        *[InlineKeyboardButton(text=item["question"],
                               callback_data=main_faq_edit_callback.new(callback_id=item["id"]))
          for item in faq_questions])
    if (page < max_pages) and (count_rows > 10):
        if page != 0:
            previous_page = InlineKeyboardButton(text=f"⏪ Страница {page}", callback_data="main_faq_prev_edit")
        else:
            previous_page = InlineKeyboardButton(text=f"⏪", callback_data="main_faq_prev_edit")
        if page + 1 >= max_pages:
            next_page = InlineKeyboardButton(text=f"⏩", callback_data="main_faq_next_edit")
        else:
            next_page = InlineKeyboardButton(text=f"⏩ Страница {page + 2}", callback_data="main_faq_next_edit")
        markup.row(previous_page, next_page)
    markup.add(InlineKeyboardButton(text="⬅ Назад", callback_data="back_to_admin_faq"))
    return markup


def cancel_or_delete_main_faq():
    markup = InlineKeyboardMarkup()
    callback_button = InlineKeyboardButton(text="✅ Удалить", callback_data="delete_main_faq")
    callback_button2 = InlineKeyboardButton(text="❌ Отмена", callback_data="cancel_del_main_faq")
    markup.add(callback_button, callback_button2)
    return markup


def inline_keyboard_edit_main_faq_choice():
    markup = InlineKeyboardMarkup()
    callback_button = InlineKeyboardButton(text="❓ Вопрос", callback_data="edit_main_faq_q")
    callback_button2 = InlineKeyboardButton(text="❗ Ответ", callback_data="edit_main_faq_a")
    callback_button3 = InlineKeyboardButton(text="⬅ Назад", callback_data="back_to_admin_edit_faq")
    markup.add(callback_button, callback_button2)
    markup.row(callback_button3)
    return markup


def inline_keyboard_edit_main_faq_or_cancel():
    markup = InlineKeyboardMarkup()
    callback_button = InlineKeyboardButton(text="✅ Изменить", callback_data="edit_main_faq_conf")
    callback_button2 = InlineKeyboardButton(text="❌ Отмена", callback_data="edit_main_faq_dec")
    markup.add(callback_button, callback_button2)
    return markup


# F.A.Q Отмена
def inline_keyboard_cancel_faq():
    markup = InlineKeyboardMarkup()
    cancel_button = InlineKeyboardButton(text="❌ Отмена", callback_data="cancel_step_faq")
    markup.add(cancel_button)
    return markup


# F.A.Q Отмена Изменения
def inline_keyboard_cancel_faq_edit():
    markup = InlineKeyboardMarkup()
    cancel_button = InlineKeyboardButton(text="❌ Отмена", callback_data="cancel_step_faq_edit")
    markup.add(cancel_button)
    return markup
