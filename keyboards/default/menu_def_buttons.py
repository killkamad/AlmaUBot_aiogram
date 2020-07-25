from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


def always_stay_keyboard():
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    menu = KeyboardButton(text='🏠 Меню')
    # help_c = KeyboardButton(text='❓ Помощь')
    about = KeyboardButton(text='💻 О боте')
    markup.add(menu, about)
    return markup
