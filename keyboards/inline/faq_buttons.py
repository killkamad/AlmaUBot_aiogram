from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
import logging
from keyboards.inline import main_faq_callback
from utils import db_api as db
from math import ceil


async def inline_keyboard_main_faq(page):
    # logging.info(f'page: {page}')
    max_pages = (ceil(await db.main_faq_count() / 10))
    count_rows = await db.main_faq_count()
    markup = InlineKeyboardMarkup(row_width=1)
    faq_questions = await db.main_faq_select_data(page)
    markup.add(
        *[InlineKeyboardButton(text=item["question"], callback_data=main_faq_callback.new(callback_id=item["id"]))
          for item in faq_questions])
    if (page < max_pages) and (count_rows > 10):
        if page != 0:
            previous_page = InlineKeyboardButton(text=f"⏪ Страница {page}", callback_data="main_faq_previous")
        else:
            previous_page = InlineKeyboardButton(text=f"⏪", callback_data="main_faq_previous")
        if page + 1 >= max_pages:
            next_page = InlineKeyboardButton(text=f"⏩", callback_data="main_faq_next")
        else:
            next_page = InlineKeyboardButton(text=f"⏩ Страница {page + 2}", callback_data="main_faq_next")
        markup.row(previous_page, next_page)
    # markup.add(InlineKeyboardButton(text="⬅ Назад", callback_data="go_back"))
    return markup


def inline_keyboard_main_faq_back():
    markup = InlineKeyboardMarkup(row_width=1)
    markup.add(InlineKeyboardButton(text="⬅ Назад", callback_data="back_to_main_faq"))
    return markup
