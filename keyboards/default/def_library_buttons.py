from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


def keyboard_library():
    markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    callback_button1 = KeyboardButton(text="🌐 Вебсайт")
    callback_button2 = KeyboardButton(text="⚡ Электронные ресурсы")
    callback_button3 = KeyboardButton(text="☎ Контакты")
    callback_button4 = KeyboardButton(text="🕐 Время работы")
    callback_button7 = KeyboardButton(text="🎓 Онлайн курсы")
    callback_button8 = KeyboardButton(text="💳 Потерял(a) ID-карту")
    callback_button9 = KeyboardButton(text="⚠ Правила")
    callback_button10 = KeyboardButton(text="📰 Права читателя")
    callback_button11 = KeyboardButton(text="🚫 Что не разрешается")
    callback_button12 = KeyboardButton(text="⛔ Ответственность за нарушения")
    callback_button13 = KeyboardButton(text="⬅ В главное меню")
    markup.add(callback_button1, callback_button2, callback_button3, callback_button4,
               callback_button7, callback_button8, callback_button9, callback_button10,
               callback_button11, callback_button12, callback_button13)
    return markup


def keyboard_library_choice_db():
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add("IPR Books", "Scopus")
    markup.add("Web of Science", "ЮРАЙТ")
    markup.add("Polpred", "РМЭБ")
    return markup


def keyboard_library_send_phone():
    markup = ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    button_phone = KeyboardButton(text="☎ Отправить номер телефона", request_contact=True)
    markup.add(button_phone)
    return markup
