import ast
import logging

from aiogram.utils import exceptions
from aiogram import types
from aiogram.types import CallbackQuery, ContentType
from loader import dp, bot
from keyboards.inline.admin_buttons import inline_keyboard_nav_university_admin_menu, inline_keyboard_contact_center_admin, \
    cancel_or_send_contact_center_admin, cancel_or_update_contact_center_admin, \
    cancel_or_delete_contact_center_admin, inline_keyboard_contacts_center_delete, inline_keyboard_contacts_center_update, \
    inline_keyboard_cancel_contact_center_admin

import asyncio

from utils import db_api as db
from .admin_menu import admin_menu

from utils.delete_messages import bot_delete_messages
from aiogram.dispatcher import FSMContext
from states.admin import SendContactCenter, UpdateContactCenter, DeleteContactCenter


@dp.callback_query_handler(text_contains='nav_university_admin_menu')
async def callback_inline_nav_university_admin_menu(call: CallbackQuery):
    logging.info(f'User({call.message.chat.id}) вошел в админ меню Навигации, call.data - {call.data}')
    await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                text='Админ меню Навигации:', reply_markup=inline_keyboard_nav_university_admin_menu())


@dp.callback_query_handler(text_contains='contacts_center_admin')
async def callback_inline_contacts_center_admin(call: CallbackQuery):
    logging.info(f'User({call.message.chat.id}) вошел в админ меню Навигации, call.data - {call.data}')
    await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                text='Админ меню Навигации:', reply_markup=inline_keyboard_contact_center_admin())


#### Создания контакт центра ####
@dp.callback_query_handler(text='send_contact_center_admin', state=None)
async def callback_inline_send_contact_center_admin(call: CallbackQuery):
    logging.info(f'User({call.message.chat.id}) нажал на кнопку {call.data}')
    await call.message.answer('Напишите название контакт центра, например (бухгалтерия):', reply_markup=inline_keyboard_cancel_contact_center_admin())
    await SendContactCenter.name.set()


@dp.callback_query_handler(text='cancel_step_contact_center_admin', state=['*'])
async def callback_inline_cancel_step(call: CallbackQuery, state: FSMContext):
    logging.info(f'User({call.message.chat.id}) нажал на кнопку {call.data}')
    await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                text='<b><i>ОТМЕНЕНО</i></b>', parse_mode='HTML')
    await state.reset_state()


# Проверка центра на текст
@dp.message_handler(content_types=ContentType.ANY, state=SendContactCenter.name)
async def message_send_contact_center_name(message: types.Message, state: FSMContext):
    if message.content_type == 'text':
        await state.update_data(name=message.text.lower(),
                                user_id=message.chat.id)
        await bot.send_message(message.chat.id, 'Отправьте описание контакт центра', reply_markup=inline_keyboard_cancel_contact_center_admin())
        await SendContactCenter.description.set()
    else:
        print(message.content_type)
        await bot.send_message(message.chat.id,
                               'Ошибка - название может содержать только текст\nПовторите название для кнопки, например (бухгалтерия):')


# Проверка описания центра на текст
@dp.message_handler(content_types=ContentType.ANY, state=SendContactCenter.description)
async def message_send_contact_center_description(message: types.Message, state: FSMContext):
    if message.content_type == 'text':
        await state.update_data(description = message.text.lower())
        data = await state.get_data()
        txt = f'Название кнопки будет: {data["name"]}'
        await bot.send_message(message.chat.id, txt, reply_markup=cancel_or_send_contact_center_admin())
        await state.reset_state(with_data=False)
    else:
        await message.answer('Ошибка - вы отправили не текст повторите')


# создание контакт центра в базе данных
@dp.callback_query_handler(text='send_contact_center', state=None)
async def callback_inline_send_contact_center_final(call: CallbackQuery, state: FSMContext):
    try:
        data = await state.get_data()
        await bot_delete_messages(call.message, 4)
        await db.add_contact_center_data(data['user_id'], data['description'], data["name"])
        await bot.delete_message(call.message.chat.id, call.message.message_id)
        await call.message.answer(f'описание <b>{data["name"]}</b> отправлено', parse_mode='HTML')
        logging.info(f'User({call.message.chat.id}) отправил контакты для {data["name"]}')
    except Exception as e:
        await call.message.answer(f'Ошибка контакт центр не отправлен, (Ошибка - {e})')
        print(e)


#### Обновление контакт центра ####
@dp.callback_query_handler(text='update_contact_center_admin', state=None)
async def callback_inline_update_schedule_bot(call: CallbackQuery):
    logging.info(f'User({call.message.chat.id}) нажал на кнопку {call.data}')
    await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                text='Выберите кнопку для изменения:',
                                reply_markup=await inline_keyboard_contacts_center_update())
    await UpdateContactCenter.name.set()


@dp.callback_query_handler(text_contains="['updade_contact_center'", state=UpdateContactCenter.name)
async def callback_inline_updade_contact_center(call: CallbackQuery, state: FSMContext):
    logging.info(f'User({call.message.chat.id}) нажал на кнопку {call.data}')
    name_call = ast.literal_eval(call.data)[1]
    await state.update_data(name=name_call, user_id=call.message.chat.id)
    await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                text=f'Напишете заново новую информацию для <b>{name_call}</b>:',
                                parse_mode='HTML', reply_markup=inline_keyboard_cancel_contact_center_admin())
    await UpdateContactCenter.description.set()


@dp.message_handler(content_types=ContentType.ANY, state=UpdateContactCenter.description)
async def updade_contact_center_step(message: types.Message, state: FSMContext):
    await UpdateContactCenter.description.set()
    if message.content_type == 'text':
        await state.update_data(description=message.text.lower())
        data = await state.get_data()
        txt = f'Название кнопки: <b>{data["name"]}</b>'
        await bot.send_message(message.chat.id, txt, reply_markup=cancel_or_update_contact_center_admin())
        await state.reset_state(with_data=False)
    else:
        await message.answer('Ошибка - вы отправили не текст повторите')


@dp.callback_query_handler(text='update_info_contact_center_admin', state=None)
async def callback_inline_send_schedule(call: CallbackQuery, state: FSMContext):
    try:
        data = await state.get_data()
        await bot_delete_messages(call.message, 2)
        await db.update_contact_center_data(data['user_id'], data['description'], data["name"])
        await bot.delete_message(call.message.chat.id, call.message.message_id)
        await call.message.answer(f'Описание <b>{data["name"]}</b> успешно обновлено', parse_mode='HTML')
        logging.info(f'User({call.message.chat.id}) обновил описание для {data["name"]}')
    except Exception as e:
        await call.message.answer(f'(Ошибка - {e})')
        logging.info(f'Ошибка - {e}')


@dp.callback_query_handler(text='delete_contact_center_admin', state=None)
async def callback_inline_delete_contact_center_admin(call: CallbackQuery):
    logging.info(f'User({call.message.chat.id}) нажал на кнопку {call.data}')
    await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                text='Выберите кнопку для удаление:',
                                reply_markup=await inline_keyboard_contacts_center_delete())
    await DeleteContactCenter.name.set()


@dp.callback_query_handler(text_contains="['delete_contact_center'", state=DeleteContactCenter.name)
async def callback_inline_update_schedule(call: CallbackQuery, state: FSMContext):
    logging.info(f'User({call.message.chat.id}) нажал на кнопку {call.data}')
    button_name = ast.literal_eval(call.data)[1]
    await state.update_data(name=button_name, user_id=call.message.chat.id)
    await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                text=f'Вы точно уверены, что хотите удалить информацию для <b>{button_name}</b>:',
                                parse_mode='HTML', reply_markup=cancel_or_delete_contact_center_admin())
    await DeleteContactCenter.confirm_delete.set()


@dp.callback_query_handler(text='delete_info_contact_center_admin', state=DeleteContactCenter.confirm_delete)
async def callback_inline_send_schedule(call: CallbackQuery, state: FSMContext):
    try:
        data = await state.get_data()
        await db.delete_contact_center_button(data["name"])
        await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                    text=f'ключевой центр <b>{data["name"]}</b> успешно удален из базы данных',
                                    parse_mode='HTML')
        await admin_menu(call.message)
        await state.reset_state()
        logging.info(f'User({call.message.chat.id}) удалил ключевой центр для {data["name"]}')
    except Exception as e:
        await call.message.answer(f'(Ошибка - {e})')
        logging.info(f'Ошибка - {e}')