from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


# Рассылка
def inline_keyboard_mass_mailing_send_or_attach():
    markup = InlineKeyboardMarkup(row_width=1)
    callback_button1 = InlineKeyboardButton(text="➕ Прикрепить файл или фото", callback_data="attach_pic_or_doc")
    callback_button2 = InlineKeyboardButton(text="✅ Отправить рассылку", callback_data="send_send_to_all")
    callback_button3 = InlineKeyboardButton(text="❌ Отмена", callback_data="cancel_massive_sending")
    markup.add(callback_button1, callback_button2, callback_button3)
    return markup


# Рассылка
def inline_keyboard_cancel_or_send():
    markup = InlineKeyboardMarkup()
    callback_button = InlineKeyboardButton(text="✅ Отправить", callback_data="send_send_to_all")
    callback_button2 = InlineKeyboardButton(text="❌ Отмена", callback_data="cancel_massive_sending")
    markup.add(callback_button, callback_button2)
    return markup


# # Расписание Отмена
# def inline_keyboard_cancel():
#     markup = InlineKeyboardMarkup()
#     cancel_button = InlineKeyboardButton(text="❌ Отмена отправки расписания", callback_data="cancel_step")
#     markup.add(cancel_button)
#     return markup


# Добавление F.A.Q Отмена
def inline_keyboard_cancel_mass_mailing():
    markup = InlineKeyboardMarkup()
    cancel_button = InlineKeyboardButton(text="❌ Отмена", callback_data="cancel_mass_mailing")
    markup.add(cancel_button)
    return markup
