from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


def keyboard_almaushop():
    markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    # Эмодзи отделено от текста двумя пробелами, чтобы не было конфликта с кнопками библиотеки
    callback_merch = KeyboardButton(text="🛍  Мерч")
    callback_books = KeyboardButton(text="📚  Книги")
    callback_website = KeyboardButton(text="🌐  Вебсайт")
    callback_contacts = KeyboardButton(text="☎  Контакты")
    callback_faq = KeyboardButton(text="⁉  ЧаВо")
    callback_back_to_menu = KeyboardButton(text="⬅ В главное меню")
    markup.add(callback_merch, callback_books, callback_website, callback_contacts, callback_faq)
    markup.row(callback_back_to_menu)
    return markup
