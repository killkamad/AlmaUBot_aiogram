from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


def keyboard_almaushop():
    markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    # Эмодзи отделено от текста двумя пробелами, чтобы не было конфликта с кнопками библиотеки
    callback_button1 = KeyboardButton(text="🛍  Товары")
    callback_button2 = KeyboardButton(text="🌐  Вебсайт")
    callback_button3 = KeyboardButton(text="☎  Контакты")
    callback_button4 = KeyboardButton(text="⁉  ЧаВо")
    callback_button13 = KeyboardButton(text="⬅ В главное меню")
    markup.add(callback_button1, callback_button2, callback_button3, callback_button4, callback_button13)
    return markup
