from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


# Академический календарь отмена
def cancel_academic_calendar():
    markup = InlineKeyboardMarkup()
    cancel_button = InlineKeyboardButton(text="❌ Отмена", callback_data="cancel_step_academic_calendar")
    markup.add(cancel_button)
    return markup


# Академический календарь отправить или отмена
def cancel_or_send_academic_calendar():
    markup = InlineKeyboardMarkup()
    callback_button = InlineKeyboardButton(text="✅ Отправить", callback_data="send_academic_calendar_to_base")
    callback_button2 = InlineKeyboardButton(text="❌ Отмена", callback_data="cancel_academic_calendar")
    markup.add(callback_button, callback_button2)
    return markup
