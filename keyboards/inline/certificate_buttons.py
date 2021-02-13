from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from utils import db_api as db
from loader import dp, bot
from aiogram.types import CallbackQuery


async def inline_keyboard_certificate():
    markup = InlineKeyboardMarkup(row_width=1)
    callback_button = InlineKeyboardButton(text="📌 Готовые справки", callback_data='complete_certificates')
    callback_button1 = InlineKeyboardButton(text="✉ Оставить заявку", callback_data='request_certificate')
    callback_button2 = InlineKeyboardButton(text="⬅ Назад", callback_data="go_back")
    markup.add(callback_button, callback_button1, callback_button2)
    return markup


async def inline_keyboard_get_certificate(user_id):
    markup = InlineKeyboardMarkup(row_width=1)
    request = await db.select_data_certificate(user_id)
    call_list = []
    request_name = []
    for call_value in request:
        callback_data = "['certificate_call', '" + call_value[-1] + "']"
        print(callback_data)
        request_name.append(call_value[-1])
        call_list.append(callback_data)
    markup.add(*[InlineKeyboardButton(text=button, callback_data=call_data) for button, call_data in
                 zip(request_name, call_list)])
    markup.add(InlineKeyboardButton(text="⬅ Назад", callback_data="go_back"))
    return markup


def inline_keyboard_send_req_data():
    markup = InlineKeyboardMarkup(row_width=1)
    callback_button = InlineKeyboardButton(text="✅ Отправить заявку", callback_data='send_req_certificate')
    callback_back = InlineKeyboardButton(text="❌ Отмена", callback_data='send_req_cancel')
    markup.add(callback_button, callback_back)
    return markup
