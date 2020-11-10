import ast
import logging

from aiogram.types import CallbackQuery, ContentType
from aiogram import types
from states.library_state import EmailReg
from keyboards.default import always_stay_keyboard
from keyboards.inline import inline_keyboard_library, inline_keyboard_library_faq
from loader import dp, bot
from keyboards.inline.menu_buttons import inline_keyboard_menu
from keyboards.inline.schedule_buttons import inline_keyboard_schedule
from keyboards.inline.faq_buttons import inline_keyboard_faq
from keyboards.inline.library_buttons import inline_keyboard_library_registration, inline_keyboard_send_reg_data, inline_keyboard_back_to_library
# Импортирование функций из БД контроллера
from utils import db_api as db

from utils.misc import rate_limit
from utils.json_loader import json_data

# imports aiosmtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import aiosmtplib

from aiogram.dispatcher import FSMContext



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
    # logging.info(f'call = {call.data}')
    if call.data == "moodle":
        text = (await json_data())['faq_answers']['moodle']
        await bot.send_message(call.message.chat.id, text=text)
    elif call.data == "retake":
        text = (await json_data())['faq_answers']['retake']
        await bot.send_message(call.message.chat.id, text=text)
    elif call.data == "reactor_info":
        text = (await json_data())['faq_answers']['rektor']
        await bot.send_message(call.message.chat.id, text=text)
    elif call.data == "atestat":
        text = (await json_data())['faq_answers']['examination']
        await bot.send_message(call.message.chat.id, text=text)
    elif call.data == "u_wifi":
        text = (await json_data())['faq_answers']['wifi1']
        await bot.send_message(call.message.chat.id, text=text)


# Меню библиотеки
@dp.callback_query_handler(text=['library_search', 'library_faq', 'library_site'])
async def callback_inline_library(call: CallbackQuery):
    # logging.info(f'call = {call.data}')
    if call.data == "library_search":
        text = "Тут ничего нету"
        await bot.send_message(call.message.chat.id, text=text)
    elif call.data == "library_faq":
        text = "Здесь вы можете найти ответы на часто задаваемые вопросы."
        await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=text,
                                    reply_markup=inline_keyboard_library_faq())
    elif call.data == "library_site":
        text = (await json_data())['lib_answers']['library_site']
        await bot.send_message(call.message.chat.id, text=text, parse_mode='HTML')


# Меню библиотеки - Часто задаваемых вопросов
@dp.callback_query_handler(
    text=['go_back_library', 'lib_contacts', 'lib_work_time', 'lib_el_res', 'lib_reg_ex', 'lib_online_courses',
          'lib_lost_card', 'lib_laws', 'lib_rights', 'lib_not_allow', 'lib_responsible'])
async def callback_inline_library(call: CallbackQuery):
    # logging.info(f'call = {call.data}')
    if call.data == "lib_contacts":
        text = (await json_data())['lib_answers']['lib_contacts']
        await bot.send_message(call.message.chat.id, text=text)
    elif call.data == "lib_work_time":
        text = (await json_data())['lib_answers']['lib_work_time']
        await bot.send_message(call.message.chat.id, text=text)
    elif call.data == "lib_el_res":
        text = (await json_data())['lib_answers']['lib_el_res']
        await bot.send_message(call.message.chat.id, text=text, parse_mode='HTML')
    elif call.data == "lib_reg_ex":
        text = (await json_data())['lib_answers']['lib_reg_ex']
        await bot.send_message(call.message.chat.id, text=text)
    elif call.data == "lib_online_courses":
        text = (await json_data())['lib_answers']['lib_online_courses']
        await bot.send_message(call.message.chat.id, text=text)
    elif call.data == "lib_lost_card":
        text = (await json_data())['lib_answers']['lib_lost_card']
        await bot.send_message(call.message.chat.id, text=text)
    elif call.data == "lib_laws":
        text = (await json_data())['lib_answers']['lib_laws']
        await bot.send_message(call.message.chat.id, text=text)
    elif call.data == "lib_rights":
        text = (await json_data())['lib_answers']['lib_rights']
        await bot.send_message(call.message.chat.id, text=text)
    elif call.data == "lib_not_allow":
        text = (await json_data())['lib_answers']['lib_not_allow']
        await bot.send_message(call.message.chat.id, text=text)
    elif call.data == "lib_responsible":
        text = (await json_data())['lib_answers']['lib_responsible']
        await bot.send_message(call.message.chat.id, text=text)
    elif call.data == "go_back_library":
        await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                    text='Библиотека ↘', reply_markup=inline_keyboard_library())


@dp.callback_query_handler(text=['library_registration'])
async def callback_library_registration(call: CallbackQuery):
    await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                text='Регистрация на лицензионные базы данных\n'
                                     'Такие как:\n'
                                     '- IPR Books iprbookshop.ru\n'
                                     '- Scopus scopus.com\n'
                                     '- Web of Science webofknowledge.com\n',
                                reply_markup=inline_keyboard_library_registration())


@dp.callback_query_handler(text='library_registration_button',  state=None)
async def callback_library_registration(call: CallbackQuery):
    await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                text='Регистрация проводится путем отправки данных в библиотеку ALMAU.\n'
                                     '- IPR Books iprbookshop.ru\n'
                                     '- Scopus scopus.com\n'
                                     '- Web of Science webofknowledge.com\n'
                                     'Если не можете здесь отправить данные то зарегестрируйтесь через сайт lib.almau.edu.kz/page/9 \n')
    await call.message.answer('Напишите ФИО\n'
                              'Номер телефона\n'
                              'Вашу электронную почту\n'
                              'Обозначтье базу данных на которую хотитие зарегистрироваться\n')
    await EmailReg.names.set()


@dp.message_handler(content_types=ContentType.ANY, state=EmailReg.names)
async def SendToEmail(message: types.Message, state: FSMContext):
    if message.content_type == 'text':
        if len(message.text) <= 990:
            await state.update_data(SendEmailData=message.text)
            message_txt = 'Ваши данные:\n' + message.text 
            await bot.send_message(message.chat.id, message_txt, reply_markup=inline_keyboard_send_reg_data())
            await state.reset_state(with_data=False)
        else:
            await bot.send_message(message.chat.id,
                                   f'Ваше сообщение содержит больше количество символов = <b>{len(message.text)}</b>. Бот может обработать максимум 1000 символов. Сократите количество и попробуйте снова',
                                   parse_mode='HTML')
    else:
        print(message.content_type)
        await bot.send_message(message.chat.id,
                               'Ошибка - ваше сообщение должно содержать только текст')


@dp.callback_query_handler(text='SendDataCancel')
async def callback_inline_SendDataCancel(call: CallbackQuery, state: FSMContext):
    await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                text='ОТМЕНЕНЕНО', reply_markup=inline_keyboard_back_to_library())
    await state.reset_state()


@dp.callback_query_handler(text='SendEmailToLibrary')
async def callback_inline_SendEmailToLibrary(call: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    Emailmessage = MIMEMultipart("alternative")
    Emailmessage["From"] = "daniyar.urazbayev99@gmail.com"
    Emailmessage["To"] = "bronislavishe@gmail.com"
    Emailmessage["Subject"] = "Регистрация на лицензионные базы с телеграм бота"

    sending_message = MIMEText( 
       f"<html><body><h1>Здраствуйте,  тут пришли регистрационные данные <br/> {data['SendEmailData']} </h1></body></html>", "html", "utf-8"
    )

    Emailmessage.attach(sending_message)
    await aiosmtplib.send(Emailmessage, hostname="smtp.gmail.com", port=587, start_tls=True, recipients=["bronislavishe@gmail.com"],
    username="daniyar.urazbayev99@gmail.com",
    password="admin456852")
    await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                text='Данные отправлены, Ждите ответ на вашу почту', reply_markup=inline_keyboard_back_to_library())