import logging

from aiogram.types import CallbackQuery, ContentType
from aiogram import types

from keyboards.default import always_stay_keyboard, keyboard_library, keyboard_library_choice_db
from keyboards.inline import inline_keyboard_menu
from states.library_state import EmailReg
from loader import dp, bot
from keyboards.inline.library_buttons import inline_keyboard_library_registration, inline_keyboard_send_reg_data, \
    inline_keyboard_back_to_library, inline_keyboard_library_el_res, inline_keyboard_library_base_kaz, \
    inline_keyboard_library_base_zarub, inline_keyboard_library_online_bib
# Импортирование функций из БД контроллера
from utils import db_api as db
from utils.misc import rate_limit
from utils.json_loader import json_data

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import aiosmtplib

from aiogram.dispatcher import FSMContext


# Меню библиотеки
# @dp.callback_query_handler(text=['library_site'])
# async def callback_inline_library(call: CallbackQuery):
#     # logging.info(f'call = {call.data}')
#     if call.data == "library_site":
#         text = (await json_data())['lib_answers']['library_site']
#         await bot.send_message(call.message.chat.id, text=text, parse_mode='HTML')


# Меню библиотеки - Часто задаваемых вопросов
# @dp.callback_query_handler(
#     text=['go_back_library', 'lib_contacts', 'lib_work_time', 'lib_el_res', 'lib_reg_ex', 'lib_online_courses',
#           'lib_lost_card', 'lib_laws', 'lib_rights', 'lib_not_allow', 'lib_responsible'])
# async def callback_inline_library(call: CallbackQuery):
#     # logging.info(f'call = {call.data}')
#     if call.data == "lib_contacts":
#         text = (await json_data())['lib_answers']['lib_contacts']
#         await bot.send_message(call.message.chat.id, text=text)
#     elif call.data == "lib_work_time":
#         text = (await json_data())['lib_answers']['lib_work_time']
#         await bot.send_message(call.message.chat.id, text=text)
#     elif call.data == "lib_el_res":
#         text = (await json_data())['lib_answers']['lib_el_res']
#         await bot.send_message(call.message.chat.id, text=text, parse_mode='HTML')
#     elif call.data == "lib_reg_ex":
#         text = (await json_data())['lib_answers']['lib_reg_ex']
#         await bot.send_message(call.message.chat.id, text=text)
#     elif call.data == "lib_online_courses":
#         text = (await json_data())['lib_answers']['lib_online_courses']
#         await bot.send_message(call.message.chat.id, text=text)
#     elif call.data == "lib_lost_card":
#         text = (await json_data())['lib_answers']['lib_lost_card']
#         await bot.send_message(call.message.chat.id, text=text)
#     elif call.data == "lib_laws":
#         text = (await json_data())['lib_answers']['lib_laws']
#         await bot.send_message(call.message.chat.id, text=text)
#     elif call.data == "lib_rights":
#         text = (await json_data())['lib_answers']['lib_rights']
#         await bot.send_message(call.message.chat.id, text=text)
#     elif call.data == "lib_not_allow":
#         text = (await json_data())['lib_answers']['lib_not_allow']
#         await bot.send_message(call.message.chat.id, text=text)
#     elif call.data == "lib_responsible":
#         text = (await json_data())['lib_answers']['lib_responsible']
#         await bot.send_message(call.message.chat.id, text=text)
#     elif call.data == "go_back_library":
#         await bot.send_message(chat_id=call.message.chat.id,
#                                text='Библиотека ↘', reply_markup=keyboard_library())


@rate_limit(1)
@dp.message_handler(
    lambda message: message.text in ['📕 Вебсайт', '💡 Электронные ресурсы', '☎ Контакты', '🕐 Время работы',
                                     '💻 Онлайн курсы', '💳 Потерял ID-карту', '📛 Правила', '📰 Права читателя',
                                     '❌ Что не разрешается', '⛔ Ответственность за нарушения', '⬅ В главное меню'])
async def library_text_buttons_handler(message: types.Message):
    # Кнопки БИБЛИОТЕКИ
    if message.text == '📕 Вебсайт':
        text = (await json_data())['lib_answers']['library_site']
        await bot.send_message(message.chat.id, text=text, parse_mode='HTML')
    elif message.text == '💡 Электронные ресурсы':
        await bot.send_message(chat_id=message.chat.id,
                               text='Электронные ресурсы\n',
                               reply_markup=inline_keyboard_library_el_res())
    elif message.text == '☎ Контакты':
        text = (await json_data())['lib_answers']['lib_contacts']
        await bot.send_message(message.chat.id, text=text)
    elif message.text == '🕐 Время работы':
        text = (await json_data())['lib_answers']['lib_work_time']
        await bot.send_message(message.chat.id, text=text)
    elif message.text == '💻 Онлайн курсы':
        text = (await json_data())['lib_answers']['lib_online_courses']
        await bot.send_message(message.chat.id, text=text)
    elif message.text == '💳 Потерял ID-карту':
        text = (await json_data())['lib_answers']['lib_lost_card']
        await bot.send_message(message.chat.id, text=text)
    elif message.text == '📛 Правила':
        text = (await json_data())['lib_answers']['lib_laws']
        await bot.send_message(message.chat.id, text=text)
    elif message.text == '📰 Права читателя':
        text = (await json_data())['lib_answers']['lib_rights']
        await bot.send_message(message.chat.id, text=text)
    elif message.text == '❌ Что не разрешается':
        text = (await json_data())['lib_answers']['lib_not_allow']
        await bot.send_message(message.chat.id, text=text)
    elif message.text == '⛔ Ответственность за нарушения':
        text = (await json_data())['lib_answers']['lib_responsible']
        await bot.send_message(message.chat.id, text=text)
    elif message.text == '⬅ В главное меню':
        await message.answer('Возвращение в главное меню', reply_markup=always_stay_keyboard())
        await message.answer('Главное меню:\n'
                             '- Расписание - здесь можно посмотреть расписание\n'
                             '- FAQ - часто задаваемые вопросы и ответы на них\n'
                             '- Библиотека - поиск книг',
                             reply_markup=inline_keyboard_menu())


@dp.callback_query_handler(text=['library_registration'])
async def callback_library_registration(call: CallbackQuery):
    await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                text='Регистрация на лицензионные базы данных\n'
                                     'Такие как:\n'
                                     '- IPR Books iprbookshop.ru\n'
                                     '- Scopus scopus.com\n'
                                     '- Web of Science webofknowledge.com\n'
                                     '- Образовательная Платформа ЮРАЙТ urait.ru\n'
                                     '- Электронно-Библиотечная Система Polpred polpred.com\n'
                                     '- Республиканская Межвузовская Электронная Библиотека rmebrk.kz',
                                reply_markup=inline_keyboard_library_registration())


# Отравка клавиатуры для выбора базы данных для регистрации
@dp.callback_query_handler(text='library_registration_button', state=None)
async def callback_library_registration(call: CallbackQuery):
    await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                text='Регистрация проводится путем отправки данных в библиотеку ALMAU.\n'
                                     'Если не можете здесь отправить данные то зарегестрируйтесь через сайт lib.almau.edu.kz/page/9 \n')
    await call.message.answer('Выберите базу данных на которую хотите зарегистрироваться',
                              reply_markup=keyboard_library_choice_db())
    await EmailReg.bookbase.set()


# Сохранение выбранной базы данных и запрос ФИО
@dp.message_handler(state=EmailReg.bookbase)
async def process_name(message: types.Message, state: FSMContext):
    markup = types.ReplyKeyboardRemove()
    async with state.proxy() as data:
        data['bookbase'] = message.text
    await EmailReg.next()
    await message.reply("Напишите ваше ФИО", reply_markup=markup)


# Сохранение ФИО и запрос Email
@dp.message_handler(state=EmailReg.names)
async def process_name(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['names'] = message.text
    await EmailReg.next()
    await message.reply("Напишите ваш Email")


# Сохранение Email и запрос номера телефона
@dp.message_handler(state=EmailReg.email)
async def process_name(message: types.Message, state: FSMContext):
    # markup_request = types.ReplyKeyboardMarkup(resize_keyboard=True)
    # markup_request.add(types.KeyboardButton('Отправить свой контакт ☎️', request_contact=True))
    async with state.proxy() as data:
        data['email'] = message.text
    await EmailReg.next()
    await message.reply("Отправьте свой номер телефона")
    # , reply_markup=markup_request


# Сохранение Номера телефона и показ всех записанных данных, с вариантами 'отправить' или 'отменить'
@dp.message_handler(content_types=ContentType.ANY, state=EmailReg.phone)
async def SendToEmail(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['phone'] = message.text

    message_txt = f"Ваши данные:\n" \
                  f"ФИО: {data['names']}\n" \
                  f"Ваш email: {data['email']}\n" \
                  f"Ваш телефон: {data['phone']}\n" \
                  f"Желаемая база регистрации: {data['bookbase']}"
    await bot.send_message(message.chat.id, message_txt, reply_markup=inline_keyboard_send_reg_data())
    await state.reset_state(with_data=False)


# Если пользователь нажал кнопку Отмена происходит отмена и возвращение в меню библиотеки
@dp.callback_query_handler(text='SendDataCancel')
async def callback_inline_SendDataCancel(call: CallbackQuery, state: FSMContext):
    await bot.delete_message(call.message.chat.id, call.message.message_id)
    await bot.send_message(chat_id=call.message.chat.id,
                           text='Регистрация Отменена\n'
                                'Возвращение в меню библиотеки', reply_markup=keyboard_library())
    await state.reset_state()


# Handler для кнопки возврат в ЭЛЕКТРОННЫЕ РЕСУРСЫ
@dp.callback_query_handler(text='back_to_library_el_res')
async def callback_el_res(call: CallbackQuery):
    await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                text='Электронные ресурсы\n',
                                reply_markup=inline_keyboard_library_el_res())


# Handler для остальных кнопок баз данных
@dp.callback_query_handler(text=['library_free_kaz', 'library_free_zarub', 'library_online_librares'])
async def callback_el_res_choice(call: CallbackQuery):
    # logging.info(f'call = {call.data}')
    if call.data == "library_free_kaz":
        text = "Базы данных свободного доступа(Казахстанские)"
        await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                    text=text,
                                    reply_markup=inline_keyboard_library_base_kaz())
    elif call.data == "library_free_zarub":
        text = "Базы данных свободного доступа(Зарубежные)"
        await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                    text=text,
                                    reply_markup=inline_keyboard_library_base_zarub())
    elif call.data == "library_online_librares":
        text = "Онлайн Библиотеки"
        await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                    text=text,
                                    reply_markup=inline_keyboard_library_online_bib())


@dp.callback_query_handler(text='SendEmailToLibrary')
async def callback_inline_SendEmailToLibrary(call: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    await db.add_lib_reg_request_data(call.message.chat.id, call.message.message_id, data['names'], data['phone'], data['email'],
                                      data['bookbase'])
    Emailmessage = MIMEMultipart("alternative")
    Emailmessage["From"] = "daniyar.urazbayev99@gmail.com"
    # Emailmessage["To"] = "bronislavishe@gmail.com"
    Emailmessage["To"] = "killka_m@mail.ru"
    Emailmessage["Subject"] = "Регистрация на лицензионные базы с телеграм бота"

    sending_message = MIMEText(
        f"<html><body><h1>Здраствуйте, тут пришли регистрационные данные <br/> ФИО - {data['names']} <br/> Email - {data['email']} <br/> Телефон - {data['phone']}  <br/> База Данных - {data['bookbase']} </h1></body></html>",
        "html", "utf-8"
    )

    Emailmessage.attach(sending_message)
    await aiosmtplib.send(Emailmessage, hostname="smtp.gmail.com", port=587, start_tls=True,
                          recipients=["killka_m@mail.ru"],
                          username="daniyar.urazbayev99@gmail.com",
                          password="admin456852")
    await bot.delete_message(call.message.chat.id, call.message.message_id)
    await bot.send_message(chat_id=call.message.chat.id,
                           text='Запрос на ругистрацию успешно отправлен, Ожидайте ответа на указанную почту',
                           reply_markup=keyboard_library())
