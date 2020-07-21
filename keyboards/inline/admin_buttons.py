from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


def inline_keyboard_admin():
    markup = InlineKeyboardMarkup()
    callback_button = InlineKeyboardButton(text="📣 Рассылка", callback_data='send_all')
    callback_button1 = InlineKeyboardButton(text="📤 Отправить расписание", callback_data='send_schedule_bot')
    markup.add(callback_button, callback_button1)
    return markup


def inline_keyboard_massive_send_all():
    markup = InlineKeyboardMarkup()
    callback_button1 = InlineKeyboardButton(text="➕ Добавить фото", callback_data="add_photo_mass")
    callback_button2 = InlineKeyboardButton(text="✔ Отправить", callback_data="send_send_to_all")
    callback_button3 = InlineKeyboardButton(text="❌ Отмена", callback_data="cancel")
    markup.row(callback_button1)
    markup.row(callback_button2, callback_button3)
    return markup


def inline_keyboard_cancel_or_send():
    markup = InlineKeyboardMarkup()
    callback_button = InlineKeyboardButton(text="✔ Отправить", callback_data="send_send_to_all")
    callback_button2 = InlineKeyboardButton(text="❌ Отмена", callback_data="cancel")
    markup.add(callback_button, callback_button2)
    return markup


def inline_keyboard_cancel():
    markup = InlineKeyboardMarkup()
    cancel_button = InlineKeyboardButton(text="❌ Отмена отправки расписания", callback_data="cancel_step")
    markup.add(cancel_button)
    return markup


def cancel_or_send_schedule():
    markup = InlineKeyboardMarkup()
    callback_button = InlineKeyboardButton(text="✔ Отправить", callback_data="send_schedule")
    callback_button2 = InlineKeyboardButton(text="❌ Отмена", callback_data="cancel_schedule")
    markup.add(callback_button, callback_button2)
    return markup
