import json
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from data.button_names.academ_calendar_buttons import send_academ_calendar, cancel_academ_calendar


# Академический календарь отмена
def cancel_academic_calendar():
    markup = InlineKeyboardMarkup()
    cancel_button = InlineKeyboardButton(text=cancel_academ_calendar, callback_data="cancel_step_academic_calendar")
    markup.add(cancel_button)
    return markup


# Академический календарь отправить или отмена
def cancel_or_send_academic_calendar():
    markup = InlineKeyboardMarkup()
    callback_button = InlineKeyboardButton(text=send_academ_calendar, callback_data="send_academic_calendar_to_base")
    callback_button2 = InlineKeyboardButton(text=cancel_academ_calendar, callback_data="cancel_academic_calendar")
    markup.add(callback_button, callback_button2)
    return markup
