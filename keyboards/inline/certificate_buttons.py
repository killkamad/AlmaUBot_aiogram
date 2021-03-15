from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from utils import db_api as db
from .callback_datas import certificate_callback
from data.button_names.certificate_buttons import completes_button_text, request_button_text, send_request_button_text, cancel_request_button_text
from data.button_names.main_menu_buttons import cancel_menu_button

async def inline_keyboard_certificate():
    markup = InlineKeyboardMarkup(row_width=1)
    callback_button = InlineKeyboardButton(text=completes_button_text, callback_data='complete_certificates')
    callback_button1 = InlineKeyboardButton(text=request_button_text, callback_data='request_certificate')
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
    callback_button = InlineKeyboardButton(text=send_request_button_text, callback_data='send_req_certificate')
    callback_back = InlineKeyboardButton(text=cancel_menu_button, callback_data='send_req_cancel')
    markup.add(callback_button, callback_back)
    return markup


def inline_keyboard_cancel_request():
    markup = InlineKeyboardMarkup()
    cancel_button = InlineKeyboardButton(text=cancel_request_button_text, callback_data="send_req_cancel")
    markup.add(cancel_button)
    return markup
