from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


def inline_keyboard_library():
    markup = InlineKeyboardMarkup(row_width=1)
    callback_button = InlineKeyboardButton(text="🔍 Поиск книги", callback_data='library_search')
    callback_button1 = InlineKeyboardButton(text="⁉ Частые вопросы", callback_data='library_faq')
    callback_button2 = InlineKeyboardButton(text="📕 Вебсайт", callback_data='library_site')
    callback_button5 = InlineKeyboardButton(text="⬅ Назад", callback_data="go_back")
    markup.add(callback_button, callback_button1, callback_button2, callback_button5)
    return markup


def inline_keyboard_library_faq():
    markup = InlineKeyboardMarkup(row_width=1)
    callback_button = InlineKeyboardButton(text="☎ Контакты", callback_data='lib_contacts')
    callback_button1 = InlineKeyboardButton(text="🕐 Время работы", callback_data='lib_work_time')
    callback_button2 = InlineKeyboardButton(text="💡 Электронные ресурсы", callback_data='lib_el_res')
    callback_button3 = InlineKeyboardButton(text="❓ Пример удаленной регистрации", callback_data='lib_reg_ex')
    callback_button4 = InlineKeyboardButton(text="💻 Онлайн курсы", callback_data='lib_online_courses')
    callback_button5 = InlineKeyboardButton(text="💳 Потерял ID-карту", callback_data='lib_lost_card')
    callback_button6 = InlineKeyboardButton(text="📛 Правила", callback_data='lib_laws')
    callback_button7 = InlineKeyboardButton(text="📰 Права читателя", callback_data='lib_rights')
    callback_button8 = InlineKeyboardButton(text="❌ Что не разрешается", callback_data='lib_not_allow')
    callback_button9 = InlineKeyboardButton(text="⛔ Ответственность за нарушения", callback_data='lib_responsible')
    callback_back = InlineKeyboardButton(text="⬅ Назад", callback_data="go_back_library")
    markup.add(callback_button, callback_button1, callback_button2, callback_button3, callback_button4,
               callback_button5, callback_button6, callback_button7, callback_button8, callback_button9,
               callback_back)
    return markup
