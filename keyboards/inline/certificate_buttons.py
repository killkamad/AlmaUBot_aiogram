from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from utils import db_api as db
from .callback_datas import instruction_callback
from data.button_names.certificate_buttons import completes_button_text, request_button_text, send_request_button_text, \
    cancel_request_button_text, almaunion_link_button_text
from data.button_names.main_menu_buttons import cancel_menu_button


async def inline_keyboard_certificate():
    markup = InlineKeyboardMarkup(row_width=1)
    # callback_button = InlineKeyboardButton(text=completes_button_text, callback_data='complete_certificates')
    instructions = await db.select_data_instruction()
    markup.add(*[InlineKeyboardButton(text=item['button_name'],
                                      callback_data=instruction_callback.new(id=item['id'])) for item in
                 instructions])
    callback_button_link = InlineKeyboardButton(text=almaunion_link_button_text, url='https://almaunion.almau.edu.kz/report')
    callback_button_req = InlineKeyboardButton(text=request_button_text, callback_data='request_certificate')
    # callback_button2 = InlineKeyboardButton(text="⬅ Назад", callback_data="go_back")
    markup.add(callback_button_link, callback_button_req)
    return markup


# async def inline_keyboard_get_certificate(user_id):
#     markup = InlineKeyboardMarkup(row_width=1)
#     certificate = await db.select_data_certificate(user_id)
#     markup.add(*[InlineKeyboardButton(text=f"{item['certif_type']} {item['date_time'].strftime('%d.%m.%y')}",
#                                       callback_data=certificate_callback.new(id=item['id'])) for item in
#                  certificate])
#     markup.add(InlineKeyboardButton(text="⬅ Назад", callback_data="/certificate"))
#     return markup


def inline_keyboard_certificate_back():
    markup = InlineKeyboardMarkup(row_width=1)
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
