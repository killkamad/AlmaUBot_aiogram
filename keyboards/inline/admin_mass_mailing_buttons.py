from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


# Рассылка
def inline_keyboard_massive_send_all():
    markup = InlineKeyboardMarkup()
    callback_button1 = InlineKeyboardButton(text="➕ Добавить фото или документ", callback_data="add_photo_mass")
    callback_button2 = InlineKeyboardButton(text="✅ Отправить", callback_data="send_send_to_all")
    callback_button3 = InlineKeyboardButton(text="❌ Отмена", callback_data="cancel_massive_sending")
    markup.row(callback_button1)
    markup.row(callback_button2, callback_button3)
    return markup


# Рассылка
def inline_keyboard_cancel_or_send():
    markup = InlineKeyboardMarkup()
    callback_button = InlineKeyboardButton(text="✅ Отправить", callback_data="send_send_to_all")
    callback_button2 = InlineKeyboardButton(text="❌ Отмена", callback_data="cancel_massive_sending")
    markup.add(callback_button, callback_button2)
    return markup


# Расписание Отмена
def inline_keyboard_cancel():
    markup = InlineKeyboardMarkup()
    cancel_button = InlineKeyboardButton(text="❌ Отмена отправки расписания", callback_data="cancel_step")
    markup.add(cancel_button)
    return markup
