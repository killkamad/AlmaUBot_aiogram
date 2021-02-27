from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


def inline_keyboard_feedback():
    markup = InlineKeyboardMarkup(row_width=1)
    callback_button = InlineKeyboardButton(text="Написать письмо ректору", callback_data='message_to_rector')
    callback_button1 = InlineKeyboardButton(text="⬅ Назад", callback_data="go_back")
    markup.add(callback_button, callback_button1)
    return markup


def inline_keyboard_send_msg_data():
    markup = InlineKeyboardMarkup(row_width=1)
    callback_button = InlineKeyboardButton(text="✅ Отправить письмо", callback_data='SendMsgToRector')
    callback_back = InlineKeyboardButton(text="❌ Отмена", callback_data="SendMsgCancel")
    markup.add(callback_button, callback_back)
    return markup


def inline_keyboard_cancel_msg_send():
    markup = InlineKeyboardMarkup(row_width=1)
    callback_back = InlineKeyboardButton(text="❌ Отмена отправки", callback_data="SendMsgCancel")
    markup.add(callback_back)
    return markup
