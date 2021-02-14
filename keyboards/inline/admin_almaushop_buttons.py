from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from keyboards.inline.callback_datas import almau_shop_faq_delete_callback, almau_shop_faq_edit_callback
from utils import db_api as db
import logging


# Админ меню AlmaU Shop
def inline_keyboard_almau_shop_admin():
    markup = InlineKeyboardMarkup(row_width=1)
    callback_merch = InlineKeyboardButton(text="🛍 Обновить мерч", callback_data='update_almaushop_merch')
    callback_books = InlineKeyboardButton(text="📚 Обновить книги", callback_data='update_almaushop_books')
    callback_faq_add = InlineKeyboardButton(text="➕ Добавить FAQ", callback_data='add_faq_almaushop')
    callback_faq_edit = InlineKeyboardButton(text="♻ Изменить FAQ", callback_data='edit_faq_almaushop')
    callback_faq_delete = InlineKeyboardButton(text="❌ Удалить FAQ", callback_data='delete_faq_almaushop')
    callback_edit_website_button = InlineKeyboardButton(text="🌐 Изменить вебсайт",
                                                        callback_data='edit_website_b_almaushop')
    callback_edit_contacts_button = InlineKeyboardButton(text="☎ Изменить контакты",
                                                         callback_data='edit_contacts_b_almaushop')
    callback_back = InlineKeyboardButton(text="⬅ Назад", callback_data='back_to_admin_menu')
    markup.add(callback_merch, callback_books,
               callback_edit_website_button, callback_edit_contacts_button,
               callback_faq_add, callback_faq_edit, callback_faq_delete,
               callback_back)
    return markup


# AlmaU Shop FAQ сохранить или отмена
def inline_keyboard_add_almaushop_faq_or_cancel():
    markup = InlineKeyboardMarkup()
    callback_button = InlineKeyboardButton(text="✅ Сохранить", callback_data="save_faq_almaushop")
    callback_button2 = InlineKeyboardButton(text="❌ Отмена", callback_data="cancel_almaushop_faq")
    markup.add(callback_button, callback_button2)
    return markup


# AlmaU Shop изменение контента кнопки
def inline_keyboard_edit_button_content_almaushop_or_cancel():
    markup = InlineKeyboardMarkup()
    callback_button = InlineKeyboardButton(text="✅ Изменить", callback_data="edit_button_content_shop")
    callback_button2 = InlineKeyboardButton(text="❌ Отмена", callback_data="cancel_ed_but_con_shop")
    markup.add(callback_button, callback_button2)
    return markup


# AlmaU Shop FAQ удаление
async def inline_keyboard_delete_faq_almaushop():
    markup = InlineKeyboardMarkup(row_width=1)
    faq_questions = await db.almaushop_faq_select_data()
    markup.add(
        *[InlineKeyboardButton(text=item["question"],
                               callback_data=almau_shop_faq_delete_callback.new(callback_id=item["id"]))
          for item in faq_questions])
    markup.add(InlineKeyboardButton(text="⬅ Назад", callback_data="back_to_almaushop_admin"))
    return markup


# AlmaU Shop FAQ изменение
async def inline_keyboard_edit_faq_almaushop():
    markup = InlineKeyboardMarkup(row_width=1)
    faq_questions = await db.almaushop_faq_select_data()
    markup.add(
        *[InlineKeyboardButton(text=item["question"],
                               callback_data=almau_shop_faq_edit_callback.new(callback_id=item["id"]))
          for item in faq_questions])
    markup.add(InlineKeyboardButton(text="⬅ Назад", callback_data="back_to_almaushop_admin"))
    return markup


# AlmaU Shop FAQ Удалить или изменить
def cancel_or_delete_faq_almau_shop():
    markup = InlineKeyboardMarkup()
    callback_button = InlineKeyboardButton(text="✅ Удалить", callback_data="delete_faq_almaushop")
    callback_button2 = InlineKeyboardButton(text="❌ Отмена", callback_data="cancel_del_faq_almaushop")
    markup.add(callback_button, callback_button2)
    return markup


def inline_keyboard_edit_faq_almaushop_choice():
    markup = InlineKeyboardMarkup()
    callback_button = InlineKeyboardButton(text="❓ Вопрос", callback_data="edit_faq_shop_q")
    callback_button2 = InlineKeyboardButton(text="❗ Ответ", callback_data="edit_faq_shop_a")
    callback_button3 = InlineKeyboardButton(text="⬅ Назад", callback_data="back_to_almaushop_admin_faq")
    markup.add(callback_button, callback_button2)
    markup.row(callback_button3)
    return markup


def inline_keyboard_edit_almaushop_faq_or_cancel():
    markup = InlineKeyboardMarkup()
    callback_button = InlineKeyboardButton(text="✅ Изменить", callback_data="edit_faq_shop_conf")
    callback_button2 = InlineKeyboardButton(text="❌ Отмена", callback_data="edit_faq_shop_dec")
    markup.add(callback_button, callback_button2)
    return markup
