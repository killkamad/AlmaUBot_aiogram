import ast
import logging

from aiogram.types import CallbackQuery

from keyboards.default import always_stay_keyboard
from keyboards.inline import inline_keyboard_library, inline_keyboard_library_faq
from loader import dp, bot
from keyboards.inline.menu_buttons import inline_keyboard_menu
from keyboards.inline.schedule_buttons import inline_keyboard_schedule
from keyboards.inline.faq_buttons import inline_keyboard_faq
# Импортирование функций из БД контроллера
from utils import db_api as db

from utils.misc import rate_limit


@rate_limit(5, 'menu')
@dp.message_handler(commands=['menu'])
async def menu_handler(message):
    logging.info(f'Пользователь = {message.chat.username} вошел в меню')
    await bot.send_message(message.chat.id, f'Вы находитесь в главном меню.',
                           reply_markup=always_stay_keyboard())
    await bot.send_message(message.chat.id, 'Главное меню:\n'
                                            '- Расписание - здесь можно посмотреть расписание\n'
                                            '- FAQ - часто задаваемые вопросы и ответы на них\n'
                                            '- Библиотека - поиск книг',
                           reply_markup=inline_keyboard_menu())


@dp.callback_query_handler(text='/schedule')
async def callback_inline_schedule(call: CallbackQuery):
    await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                text='Выберите ваш курс ↘', reply_markup=await inline_keyboard_schedule())


@dp.callback_query_handler(text='/faq')
async def callback_inline_schedule(call: CallbackQuery):
    await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                text='F.A.Q ↘', reply_markup=inline_keyboard_faq())


@dp.callback_query_handler(text='/library')
async def callback_inline_schedule(call: CallbackQuery):
    await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                text='Библиотека ↘', reply_markup=inline_keyboard_library())


#  Получение айди расписания из бд и отправка пользователю
@dp.callback_query_handler(text_contains="['schedule_call'")
async def callback_inline(call: CallbackQuery):
    logging.info(f'call = {call.data}')
    valueFromCallBack = ast.literal_eval(call.data)[1]
    file_id = await db.find_schedule_id(valueFromCallBack)
    await bot.send_document(call.message.chat.id, file_id)


@dp.callback_query_handler(text='go_back')
async def callback_inline(call: CallbackQuery):
    await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                text='Главное меню:\n'
                                     '- Расписание - здесь можно посмотреть расписание\n'
                                     '- FAQ - часто задаваемые вопросы и ответы на них',
                                reply_markup=inline_keyboard_menu())


# Меню F.A.Q
@dp.callback_query_handler(text=['moodle', 'retake', 'reactor_info', 'atestat', 'u_wifi'])
async def callback_inline_faq(call: CallbackQuery):
    logging.info(f'call = {call.data}')
    if call.data == "moodle":
        text = "Moodle - система дистанционного обучения, включающая в себя средства для разработки дистанционных курсов.\nАдрес образовательного портала Moodle: https://online.almau.edu.kz/\nЛогин и пароль такой же как и на AlmaUnion."
        await bot.send_message(call.message.chat.id, text=text)
    elif call.data == "retake":
        text = "Список того, что нужно делать:\n1) Обязательно посещать все пары.\n2) Выполнять всё задание до дедлайна.\n3) Вести себя адекватно.\n4) Желательно задавать вопросы у преподавателя.\n\nСписок того, что не нужно делать:\n1) Прогуливать пары.\n2) Хамить и перебивать преподавателя.\n3) Сидеть в телефоне во время пары."
        await bot.send_message(call.message.chat.id, text=text)
    elif call.data == "reactor_info":
        text = "ФИО - Сулейменов Ербол Зинаддинович.\nРодился в 1973 году в городе Ташкенте.\nИмеет высшее образование, кандидат физико-математических наук.\nС 10 декабря 2018 года Международный консультант Министерства инновационного развития Республики Узбекистан."
        await bot.send_message(call.message.chat.id, text=text)
    elif call.data == "atestat":
        text = "Возможные варианты сдачи экзаменов для студентов 1-3 курсов:\n⠀\n1. Без проведения экзаменов с выставлением оценки по результатам текущей успеваемости:\n⠀\nоценка достижения результатов обучения будет проведена на основе текущей успеваемости (в качестве оценки за экзамен будет проставлена оценка равная рейтингу допуска)\n⠀\n2. Перенос экзамена\nна 15-20 июня 2020 года:\n⠀\nЭкзамен переносится на 15-20 июня 2020 г., а студенту выставляется оценка «не завершено» («I» incomplete). В случае сохранения режима карантина в июне, возможен перенос даты на август.\n⠀\n❗️Каждый студент выбирает один из 2х предложенных вариантов и подаёт заявление эдвайзеру.\n⠀\nДля студентов выпускного курса:\n⠀\nСдача комплексного экзамена\n21 апреля- 02 мая\n⠀\nФорма проведения - Устный онлайн экзамен\n⠀\nЗащита дипломного проекта\n18 мая-06 июня\n⠀\nЗащита проекта перед аттестационной комиссией с группой в онлайн формате"
        await bot.send_message(call.message.chat.id, text=text)
    elif call.data == "u_wifi":
        text = "Для подключения нужно использовать ваш логин и пароль от AlmaUnion"
        await bot.send_message(call.message.chat.id, text=text)


# Меню библиотеки
@dp.callback_query_handler(text=['library_search', 'library_faq', 'library_site'])
async def callback_inline_library(call: CallbackQuery):
    logging.info(f'call = {call.data}')
    if call.data == "library_search":
        text = "Тут ничего нету"
        await bot.send_message(call.message.chat.id, text=text)
    elif call.data == "library_faq":
        text = "Здесь вы можете найти ответы на часто задаваемые вопросы."
        await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=text,
                                    reply_markup=inline_keyboard_library_faq())
    elif call.data == "library_site":
        text = '<a href="http://lib.almau.edu.kz">Библиотека</a>'
        await bot.send_message(call.message.chat.id, text=text, parse_mode='HTML')


# Меню библиотеки - Часто задаваемых вопросов
@dp.callback_query_handler(text=['library_hours_work', 'library_laws', 'go_back_library'])
async def callback_inline_library(call: CallbackQuery):
    logging.info(f'call = {call.data}')
    if call.data == "library_hours_work":
        text = "Библиотека AlmaU сообщает об изменении в графике работы с целью более полного удовлетворения информационных потребностей наших пользователей с 02.11.2020г:\n" \
               "- понедельник-пятница с 8-00 до 19-00;\n" \
               "- суббота с 9-00 до 18-00, с техническим перерывом с 13-00 до 14-00."
        await bot.send_message(call.message.chat.id, text=text)
    elif call.data == "library_laws":
        text = "Читатель имеет право:\n" \
               "пользоваться  библиотечно-библиографическими и информационными услугами, предоставляемыми библиотекой\n\n" \
               "получать полную информацию о составе фондов библиотеки  и консультативную помощь в поиске и выборе источников информации\n\n" \
               "получать во временное пользование документы на дом или для пользования в читальном зале\n\n" \
               "получать документы или их копии по электронной доставке документов (ЭДД) в установленном порядке\n\n" \
               "участвовать в мероприятиях, проводимых библиотекой\n\n" \
               "обращаться в администрацию библиотеки с различными запросами и предложениями."
        await bot.send_message(call.message.chat.id, text=text)
    elif call.data == "go_back_library":
        await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                    text='Библиотека ↘', reply_markup=inline_keyboard_library())
