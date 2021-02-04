from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from keyboards.inline.callback_datas import almau_shop_faq_callback
from utils import db_api as db


async def inline_keyboard_faq_almaushop():
    markup = InlineKeyboardMarkup(row_width=1)
    faq_questions = await db.almaushop_faq_select_data()
    markup.add(
        *[InlineKeyboardButton(text=item["question"], callback_data=almau_shop_faq_callback.new(callback_id=item["id"]))
          for item in faq_questions])
    # markup.add(InlineKeyboardButton(text="⬅ Назад", callback_data="go_back"))
    return markup


def inline_keyboard_faq_almaushop_back():
    markup = InlineKeyboardMarkup(row_width=1)
    markup.add(InlineKeyboardButton(text="⬅ Назад", callback_data="back_to_almau_shop_faq"))
    return markup
