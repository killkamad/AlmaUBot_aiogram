from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


def inline_keyboard_library():
    markup = InlineKeyboardMarkup(row_width=1)
    callback_button = InlineKeyboardButton(text="🔍 Поиск книги", callback_data='library_search')
    callback_button1 = InlineKeyboardButton(text="⁉ Частые вопросы", callback_data='library_faq')
    callback_button2 = InlineKeyboardButton(text="📕 Сайт библиотеки", callback_data='library_site')
    callback_button5 = InlineKeyboardButton(text="Назад", callback_data="go_back")
    markup.add(callback_button, callback_button1, callback_button2, callback_button5)
    return markup


def inline_keyboard_library_faq():
    markup = InlineKeyboardMarkup(row_width=1)
    callback_button = InlineKeyboardButton(text="Часы работы библиотеки", callback_data='library_hours_work')
    callback_button1 = InlineKeyboardButton(text="Права читателя", callback_data='library_laws')
    callback_button2 = InlineKeyboardButton(text="Обязанности читателя", callback_data='library_laws1')
    callback_button3 = InlineKeyboardButton(text="Читателю не разрешается", callback_data='library_laws2')
    callback_button4 = InlineKeyboardButton(text="Права и обязанности библиотеки университета", callback_data='library_laws3')
    callback_button5 = InlineKeyboardButton(text="Порядок записи читателя", callback_data='library_laws4')
    callback_button6 = InlineKeyboardButton(text="Порядок пользования", callback_data='library_laws5')
    callback_back = InlineKeyboardButton(text="Назад", callback_data="go_back_library")
    markup.add(callback_button, callback_button1, callback_button2, callback_button3, callback_button4,
               callback_button5, callback_button6,
               callback_back)
    return markup
