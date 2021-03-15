from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from data.button_names.feedback_buttons import feedback_advisor_button, send_feedback_button
from data.button_names.main_menu_buttons import to_back_button, cancel_menu_button

def inline_keyboard_feedback():
    markup = InlineKeyboardMarkup(row_width=1)
    callback_button = InlineKeyboardButton(text=feedback_advisor_button, callback_data='message_to_rector')
    callback_button1 = InlineKeyboardButton(text=to_back_button, callback_data="go_back")
    markup.add(callback_button, callback_button1)
    return markup


def inline_keyboard_send_msg_data():
    markup = InlineKeyboardMarkup(row_width=1)
    callback_button = InlineKeyboardButton(text=send_feedback_button, callback_data='SendMsgToRector')
    callback_back = InlineKeyboardButton(text=cancel_menu_button, callback_data="SendMsgCancel")
    markup.add(callback_button, callback_back)
    return markup


def inline_keyboard_cancel_msg_send():
    markup = InlineKeyboardMarkup(row_width=1)
    callback_back = InlineKeyboardButton(text=cancel_menu_button, callback_data="SendMsgCancel")
    markup.add(callback_back)
    return markup
