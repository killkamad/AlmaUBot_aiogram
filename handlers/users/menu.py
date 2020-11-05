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
from utils.json_loader import json_data


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
