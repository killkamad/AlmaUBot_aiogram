from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


# def inline_keyboard_library():
#     markup = InlineKeyboardMarkup(row_width=1)
#     callback_button1 = InlineKeyboardButton(text="📕 Вебсайт", callback_data='library_site')
#     callback_button2 = InlineKeyboardButton(text="💡 Электронные ресурсы", callback_data='library_el_res')
#     callback_button3 = InlineKeyboardButton(text="☎ Контакты", callback_data='lib_contacts')
#     callback_button4 = InlineKeyboardButton(text="🕐 Время работы", callback_data='lib_work_time')
#     callback_button7 = InlineKeyboardButton(text="💻 Онлайн курсы", callback_data='lib_online_courses')
#     callback_button8 = InlineKeyboardButton(text="💳 Потерял ID-карту", callback_data='lib_lost_card')
#     callback_button9 = InlineKeyboardButton(text="📛 Правила", callback_data='lib_laws')
#     callback_button10 = InlineKeyboardButton(text="📰 Права читателя", callback_data='lib_rights')
#     callback_button11 = InlineKeyboardButton(text="❌ Что не разрешается", callback_data='lib_not_allow')
#     callback_button12 = InlineKeyboardButton(text="⛔ Ответственность за нарушения", callback_data='lib_responsible')
#     callback_button13 = InlineKeyboardButton(text="⬅ Назад", callback_data="go_back")
#     markup.add(callback_button1, callback_button2, callback_button3, callback_button4,
#                callback_button7, callback_button8, callback_button9, callback_button10,
#                callback_button11, callback_button12, callback_button13)
#     return markup

def inline_keyboard_library_choice_db():
    markup = InlineKeyboardMarkup(row_width=2)
    button1 = InlineKeyboardButton(text="IPR Books", callback_data="IPR Books")
    button2 = InlineKeyboardButton(text="Scopus", callback_data="Scopus")
    button3 = InlineKeyboardButton(text="Web of Science", callback_data="Web of Science")
    button4 = InlineKeyboardButton(text="ЮРАЙТ", callback_data="ЮРАЙТ")
    button5 = InlineKeyboardButton(text="Polpred", callback_data="Polpred")
    button6 = InlineKeyboardButton(text="РМЭБ", callback_data="РМЭБ")
    callback_back = InlineKeyboardButton(text="⬅ Назад", callback_data="back_to_lic_db_reg")
    markup.add(button1, button2, button3, button4, button5, button6, callback_back)
    return markup


def inline_keyboard_cancel_lic_db_reg():
    markup = InlineKeyboardMarkup(row_width=1)
    cancel = InlineKeyboardButton(text="❌ Отмена", callback_data="cancel_lic_db_reg")
    markup.add(cancel)
    return markup


def inline_keyboard_library_registration():
    markup = InlineKeyboardMarkup(row_width=1)
    callback_button = InlineKeyboardButton(text="Зарегистрироваться", callback_data='library_registration_button')
    callback_back = InlineKeyboardButton(text="⬅ Назад", callback_data="back_to_library_el_res")
    markup.add(callback_button, callback_back)
    return markup


def inline_keyboard_send_reg_data():
    markup = InlineKeyboardMarkup(row_width=1)
    callback_button = InlineKeyboardButton(text="✅ Отправить Данные", callback_data='SendEmailToLibrary')
    callback_back = InlineKeyboardButton(text="❌ Отмена", callback_data="SendDataCancel")
    markup.add(callback_button, callback_back)
    return markup


def inline_keyboard_back_to_library():
    markup = InlineKeyboardMarkup(row_width=1)
    callback_back = InlineKeyboardButton(text="⬅ Назад", callback_data="go_back_library")
    markup.add(callback_back)
    return markup


def inline_keyboard_library_el_res():
    markup = InlineKeyboardMarkup(row_width=1)
    callback_button1 = InlineKeyboardButton(text="📕 Лицензионные Базы Данных", callback_data='library_registration')
    callback_button2 = InlineKeyboardButton(text="📗 Базы данных свободного доступа(Казахстанские)",
                                            callback_data='library_free_kaz')
    callback_button3 = InlineKeyboardButton(text="📗 Базы данных свободного доступа(Зарубежные)",
                                            callback_data='library_free_zarub')
    callback_button4 = InlineKeyboardButton(text="📗 Онлайн библиотеки", callback_data='library_online_librares')
    # callback_back = InlineKeyboardButton(text="⬅ Назад", callback_data="go_back_library")
    markup.add(callback_button1, callback_button2, callback_button3, callback_button4)
    return markup


# Базы данных свободного доступа (Казахстанские)
def inline_keyboard_library_base_kaz():
    markup = InlineKeyboardMarkup(row_width=1)
    url_button1 = InlineKeyboardButton(text='Адилет', url='https://adilet.zan.kz')
    url_button2 = InlineKeyboardButton(text='Институт Мировой Экономики и Политики', url='https://iwep.kz')
    url_button3 = InlineKeyboardButton(text='КазСтат', url='https://stat.gov.kz')
    url_button4 = InlineKeyboardButton(text='Образовательное Сообщество Казахстана', url='https://uchi.kz')
    url_button5 = InlineKeyboardButton(text='Официальный Сайт Президента РК', url='https://akorda.kz')
    url_button6 = InlineKeyboardButton(text='Фонд Науки РК', url='science-fund.kz')
    callback_back = InlineKeyboardButton(text="⬅ Назад", callback_data="back_to_library_el_res")
    markup.add(url_button1, url_button2, url_button3, url_button4, url_button5, url_button6)
    markup.row(callback_back)
    return markup
    # Фонд Науки РК science-fund.kz


# Базы данных свободного доступа (Зарубежные)
def inline_keyboard_library_base_zarub():
    markup = InlineKeyboardMarkup(row_width=2)
    url_button1 = InlineKeyboardButton(text='Australian Business Deans Council', url='https://abdc.edu.au')
    url_button2 = InlineKeyboardButton(text='bookboon', url='https://bookboon.com')
    url_button4 = InlineKeyboardButton(text='Cambridge University Press', url='https://www.cambridge.org')
    url_button5 = InlineKeyboardButton(text='Directory of Open Access Journals', url='https://doaj.org')
    url_button6 = InlineKeyboardButton(text='EBSCO', url='https://go.ebsco.com')
    url_button7 = InlineKeyboardButton(text='eldis', url='https://eldis.org')
    url_button8 = InlineKeyboardButton(text='Emerald Publishing', url='https://emeraldgrouppublishing.com')
    url_button9 = InlineKeyboardButton(text='Globethics', url='https://globethics.net')
    url_button10 = InlineKeyboardButton(text='Google Scholar', url='https://scholar.google.com')
    url_button11 = InlineKeyboardButton(text='Mendeley', url='https://mendeley.com')
    url_button12 = InlineKeyboardButton(text='OpenEdition', url='https://openedition.org')
    url_button13 = InlineKeyboardButton(text='Oxford Journals', url='https://academic.oup.com')
    url_button14 = InlineKeyboardButton(text='The World Bank', url='https://wdi.worldbank.org')
    callback_back = InlineKeyboardButton(text="⬅ Назад", callback_data="back_to_library_el_res")
    markup.add(url_button1, url_button2, url_button4, url_button5,
               url_button6, url_button7, url_button8, url_button9, url_button10,
               url_button11, url_button12, url_button13, url_button14)
    markup.row(callback_back)
    return markup


# Онлайн Библиотеки
def inline_keyboard_library_online_bib():
    markup = InlineKeyboardMarkup(row_width=1)
    url_button1 = InlineKeyboardButton(text='Единая Электронная Библиотека', url='https://elibrary.kz')
    url_button2 = InlineKeyboardButton(text='Казахстанская Национальная Электронная Библиотека',
                                       url='https://kazneb.kz')
    url_button3 = InlineKeyboardButton(text='Мировая Цифровая Библиотека', url='https://wdl.org')
    url_button4 = InlineKeyboardButton(text='Научная Электронная Библиотека', url='https://elibrary.ru')
    url_button5 = InlineKeyboardButton(text='Онлайн Библиотека MyBrary', url='https://mybrary.ru')
    url_button6 = InlineKeyboardButton(text='Открытая Библиотека kitap', url='https://kitap.kz')
    url_button7 = InlineKeyboardButton(text='Электронно-Библиотечная Система Лань', url='https://e.lanbook.com')
    url_button8 = InlineKeyboardButton(text='ЮРАЙТ Легендарные Книги', url='https://biblio-online.ru')
    callback_back = InlineKeyboardButton(text="⬅ Назад", callback_data="back_to_library_el_res")
    markup.add(url_button1, url_button2, url_button3, url_button4, url_button5, url_button6, url_button7, url_button8,
               callback_back)
    return markup
