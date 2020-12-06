from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


def inline_keyboard_faq():
    markup = InlineKeyboardMarkup(row_width=1)
    callback_button = InlineKeyboardButton(text="Что такое мудл и как в него зайти?", callback_data='moodle')
    callback_button1 = InlineKeyboardButton(text="Как не получить 'retake'?", callback_data='retake')
    callback_button2 = InlineKeyboardButton(text="Как зовут нашего нового ректора?", callback_data='reactor_info')
    callback_button3 = InlineKeyboardButton(text="Как будет проходить промежуточная и итоговя аттестация?",
                                            callback_data="atestat")
    callback_button4 = InlineKeyboardButton(text="Как подключится к wi-fi в университете?", callback_data='u_wifi')
    callback_button5 = InlineKeyboardButton(text="⬅ Назад", callback_data="go_back")
    markup.add(callback_button, callback_button1, callback_button2, callback_button3, callback_button4,
               callback_button5)
    return markup
