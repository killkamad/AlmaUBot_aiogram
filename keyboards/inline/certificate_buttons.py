from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from utils import db_api as db
from .callback_datas import certificate_callback


async def inline_keyboard_certificate():
    markup = InlineKeyboardMarkup(row_width=1)
    callback_button = InlineKeyboardButton(text="📌 Готовые справки", callback_data='complete_certificates')
    callback_button1 = InlineKeyboardButton(text="✉ Оставить заявку", callback_data='request_certificate')
    # callback_button2 = InlineKeyboardButton(text="⬅ Назад", callback_data="go_back")
    markup.add(callback_button, callback_button1)
    return markup


async def inline_keyboard_get_certificate(user_id):
    markup = InlineKeyboardMarkup(row_width=1)
    certificate = await db.select_data_certificate(user_id)
    markup.add(*[InlineKeyboardButton(text=f"{item['name_certif']} {item['date_time'].strftime('%d.%m.%y')}",
                                      callback_data=certificate_callback.new(id=item['id_request'])) for item in certificate])
    markup.add(InlineKeyboardButton(text="⬅ Назад", callback_data="/certificate"))
    return markup


def inline_keyboard_send_req_data():
    markup = InlineKeyboardMarkup(row_width=1)
    callback_button = InlineKeyboardButton(text="✅ Отправить заявку", callback_data='send_req_certificate')
    callback_back = InlineKeyboardButton(text="❌ Отмена", callback_data='send_req_cancel')
    markup.add(callback_button, callback_back)
    return markup


def inline_keyboard_cancel_request():
    markup = InlineKeyboardMarkup()
    cancel_button = InlineKeyboardButton(text="❌ Отмена запроса", callback_data="send_req_cancel")
    markup.add(cancel_button)
    return markup
