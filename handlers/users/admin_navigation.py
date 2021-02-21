import ast
import logging

from aiogram.utils import exceptions
from aiogram import types
from aiogram.types import CallbackQuery, ContentType, ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from loader import dp, bot
from keyboards.inline import inline_keyboard_nav_university_admin_menu, inline_keyboard_contact_center_admin, \
    cancel_or_send_contact_center_admin, cancel_or_update_contact_center_admin, \
    cancel_or_delete_contact_center_admin, inline_keyboard_contacts_center_delete, inline_keyboard_contacts_center_update, \
    inline_keyboard_cancel_contact_center_admin, cancel_or_send_tutors_management, inline_keyboard_map_nav_admin_menu, cancel_or_send_map_nav_admin, \
    inline_keyboard_cabinets_admin, cancel_or_update_map_nav_admin, cancel_or_delete_map_nav_admin

import asyncio

from utils import db_api as db
from .admin_menu import admin_menu

from utils.delete_messages import bot_delete_messages
from aiogram.dispatcher import FSMContext
from states.admin import SendContactCenter, UpdateContactCenter, DeleteContactCenter, Pps_admin, Map_navigation, Map_navigation_update, Map_navigation_delete

from keyboards.inline import cabinet_callback, cabinet_callback_update

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
    await call.message.answer('Админ меню навигации', reply_markup = inline_keyboard_nav_university_admin_menu())
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
@dp.callback_query_handler(text='tutors_university_admin', state=None)
async def callback_tutors_university_admin_state(call: CallbackQuery):
    await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                text='выбор для изменений', reply_markup=inline_keyboard_cancel_contact_center_admin())
    # await bot.send_message(chat_id=message.chat.id, text='ВЫБИРЕТЕ Школу', reply_markup=inline_keyboard_cancel_contact_center_admin())
    await call.message.answer('Выберите школу для которой хотите ввести изменения\n'
                              'Для отмены нажмите сверху кнопку отмены',
                              reply_markup=keyboard_pps_choice_shcool())
    await Pps_admin.shcool.set()


def keyboard_pps_choice_shcool():
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add("Школа менеджмента", "Школа политики и права")
    markup.add("Школа Инженерного Менеджмента", "Школа предпринимательства и инноваций")
    markup.add("Высшая Школа Бизнеса", "Школа Экономики и Финансов")
    markup.add("Ректорат")
    return markup


@dp.message_handler(
    lambda message: message.text in ['Школа менеджмента', 'Школа политики и права', 'Школа Инженерного Менеджмента', 'Школа предпринимательства и инноваций', 'Высшая Школа Бизнеса', 'Школа Экономики и Финансов'],
    state=Pps_admin.shcool)
async def tutors_university_admin_state_shcool(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['shcool'] = message.text
    await bot.send_message(chat_id=message.chat.id, text='Выбор для изменений',
                           reply_markup=inline_keyboard_cancel_contact_center_admin())
    await message.reply("выбирете что хотите изменить", reply_markup=keyboard_pps_choice_position())
    await Pps_admin.position.set()


@dp.message_handler(
    lambda message: message.text in ['Ректорат'],
    state=Pps_admin.shcool)
async def tutors_university_admin_state_rectorat(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['shcool'] = message.text
    await bot.send_message(chat_id=message.chat.id, text='Выбор для изменений',
                           reply_markup=inline_keyboard_cancel_contact_center_admin())
    await message.reply("выбирете что хотите изменить", reply_markup=keyboard_pps_choice_position_rector())
    await Pps_admin.position.set()


def keyboard_pps_choice_position():
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add("Декан", "Преподаватели")
    return markup


def keyboard_pps_choice_position_rector():
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add("Ректор", "Проректоры")
    return markup

@dp.message_handler(lambda message: message.text in ['Декан', 'Преподаватели', "Ректор", "Проректоры"],state=Pps_admin.position)
async def tutors_university_admin_state_position(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['position'] = message.text
    await message.reply(f"Напишите описание которое хотите изменить для {data['position']} {data['shcool']}", reply_markup=ReplyKeyboardRemove())
    await Pps_admin.description.set()


@dp.message_handler(content_types=ContentType.ANY, state=Pps_admin.description)
async def message_send_tutors_management(message: types.Message, state: FSMContext):
    if message.content_type == 'text':
        await state.update_data(description = message.text.lower(), user_id=message.chat.id)
        data = await state.get_data()
        await bot.send_message(message.chat.id, text='Отправить это описание?', reply_markup=cancel_or_send_tutors_management())
        await state.reset_state(with_data=False)
    else:
        await message.answer('Ошибка - вы отправили не текст повторите')


@dp.callback_query_handler(text='send_tutors_management', state=None)
async def callback_inline_send_tutors_management_final(call: CallbackQuery, state: FSMContext):
    try:
        data = await state.get_data()
        await bot_delete_messages(call.message, 9)
        await db.add_pps_data(data['user_id'], data['shcool'], data['position'], data['description'])
        await bot.delete_message(call.message.chat.id, call.message.message_id)
        await call.message.answer(f'описание отправлено')
        await call.message.answer('Админ меню навигации', reply_markup = inline_keyboard_nav_university_admin_menu())
        logging.info(f'User({call.message.chat.id}) отправил информацию для преподавателей менеджмента')
    except Exception as e:
        await call.message.answer(f'Ошибка описание не отправлено, (Ошибка - {e})')
        print(e)


@dp.callback_query_handler(text_contains='map_nav_admin')
async def callback_inline_contacts_center_admin(call: CallbackQuery):
    logging.info(f'User({call.message.chat.id}) вошел в админ карты-навигации, call.data - {call.data}')
    await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                text='Админ меню карты-навигации:', reply_markup=inline_keyboard_map_nav_admin_menu())


@dp.callback_query_handler(text='send_cabinet_admin', state=None)
async def callback_map_nav_admin_state(call: CallbackQuery):
    await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                text='выбор для изменений', reply_markup=inline_keyboard_cancel_contact_center_admin())
    # await bot.send_message(chat_id=message.chat.id, text='ВЫБИРЕТЕ Школу', reply_markup=inline_keyboard_cancel_contact_center_admin())
    await call.message.answer('Выберите здание для которой хотите ввести изменения\n'
                              'Для отмены нажмите сверху кнопку отмены',
                              reply_markup=keyboard_map_nav_choice_building())
    await Map_navigation.building.set()


def keyboard_map_nav_choice_building():
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add("Старое здание", "Новое здание")
    return markup


@dp.message_handler(lambda message: message.text in ['Новое здание'],state=Map_navigation.building)
async def map_nav_admin_state_building(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['building'] = message.text
    await bot.send_message(chat_id=message.chat.id, text='Выбор для изменений',
                           reply_markup=inline_keyboard_cancel_contact_center_admin())
    await message.reply("выбирете что хотите изменить", reply_markup=map_nav_admin_choice_floor_new())
    await Map_navigation.floor.set()


@dp.message_handler(lambda message: message.text in ['Старое здание'],state=Map_navigation.building)
async def map_nav_admin_state_building(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['building'] = message.text
    await bot.send_message(chat_id=message.chat.id, text='Выбор для изменений',
                           reply_markup=inline_keyboard_cancel_contact_center_admin())
    await message.reply("выбирете что хотите изменить", reply_markup=map_nav_admin_choice_floor_old())
    await Map_navigation.floor.set()


def map_nav_admin_choice_floor_old():
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add("1 этаж", "2 этаж")
    markup.add("3 этаж", "4 этаж")
    markup.add("5 этаж", "6 этаж")
    return markup


def map_nav_admin_choice_floor_new():
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add("1 этаж", "2 этаж")
    markup.add("3 этаж", "4 этаж")
    return markup


@dp.message_handler(lambda message: message.text in ['1 этаж', '2 этаж', "3 этаж", "4 этаж", "5 этаж", "6 этаж"],state=Map_navigation.floor)
async def map_nav_admin_state_floor(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['floor'] = message.text
    await message.reply(f"Напишите название(например:101 кабинет) которое хотите добавить для {data['building']} {data['floor']}", reply_markup=ReplyKeyboardRemove())
    await Map_navigation.cabinet.set()


@dp.message_handler(content_types=ContentType.ANY, state=Map_navigation.cabinet)
async def map_nav_admin_state_cabinet(message: types.Message, state: FSMContext):
    if message.content_type == 'text':
        async with state.proxy() as data:
            data['cabinet'] = message.text
        await message.reply(f"Напишите описание для {data['cabinet']} {data['building']} {data['floor']} ", reply_markup=inline_keyboard_cancel_contact_center_admin())
        await Map_navigation.description.set()
    else:
        await message.answer('Ошибка - вы отправили не текст повторите')


@dp.message_handler(content_types=ContentType.ANY, state=Map_navigation.description)
async def map_nav_admin_state_description(message: types.Message, state: FSMContext):
    if message.content_type == 'text':
        await state.update_data(description = message.text.lower(), user_id=message.chat.id)
        data = await state.get_data()
        await bot.send_message(message.chat.id, text= f"Отправить описание?:\n"
                                                      f"{data['building']}\n"
                                                      f"{data['floor']}\n"
                                                      f"Название кабинета(кнопки) - {data['cabinet']}\n"
                                                      f"описание - {data['description']}", reply_markup=cancel_or_send_map_nav_admin())
        await state.reset_state(with_data=False)
    else:
        await message.answer('Ошибка - вы отправили не текст повторите')


@dp.callback_query_handler(text='send_map_navigation_admin', state=None)
async def map_nav_admin_state_send_final(call: CallbackQuery, state: FSMContext):
    try:
        data = await state.get_data()
        # await bot_delete_messages(call.message, 9)
        await db.add_map_navigation_data(data['user_id'], data['building'], data['floor'], data['cabinet'], data['description'])
        await bot.delete_message(call.message.chat.id, call.message.message_id)
        await call.message.answer(f'описание отправлено')
        await call.message.answer('Админ меню навигации', reply_markup = inline_keyboard_nav_university_admin_menu())
        logging.info(f'User({call.message.chat.id}) отправил информацию для кабинета')
    except Exception as e:
        await call.message.answer(f'Ошибка описание не отправлено, (Ошибка - {e})')
        print(e)


###################################################################################################


@dp.callback_query_handler(text='update_cabinet_admin', state=None)
async def callback_map_nav_admin_state_update(call: CallbackQuery):
    await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                text='выбор для изменений', reply_markup=inline_keyboard_cancel_contact_center_admin())
    # await bot.send_message(chat_id=message.chat.id, text='ВЫБИРЕТЕ Школу', reply_markup=inline_keyboard_cancel_contact_center_admin())
    await call.message.answer('Выберите здание для которой хотите ввести изменения\n'
                              'Для отмены нажмите сверху кнопку отмены',
                              reply_markup=keyboard_map_nav_choice_building())
    await Map_navigation_update.building.set()


@dp.message_handler(lambda message: message.text in ['Новое здание'],state=Map_navigation_update.building)
async def map_nav_admin_state_building_update(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['building'] = message.text
    await bot.send_message(chat_id=message.chat.id, text='Выбор для изменений',
                           reply_markup=inline_keyboard_cancel_contact_center_admin())
    await message.reply("выбирете что хотите изменить", reply_markup=map_nav_admin_choice_floor_new())
    await Map_navigation_update.floor.set()


@dp.message_handler(lambda message: message.text in ['Старое здание'],state=Map_navigation_update.building)
async def map_nav_admin_state_building_update(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['building'] = message.text
    await bot.send_message(chat_id=message.chat.id, text='Выбор для изменений',
                           reply_markup=inline_keyboard_cancel_contact_center_admin())
    await message.reply("выбирете что хотите изменить", reply_markup=map_nav_admin_choice_floor_old())
    await Map_navigation_update.floor.set()


@dp.message_handler(lambda message: message.text in ['1 этаж', '2 этаж', "3 этаж", "4 этаж", "5 этаж", "6 этаж"],state=Map_navigation_update.floor)
async def map_nav_admin_state_floor_update(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['floor'] = message.text
    floor = data['floor']
    building = data['building']
    await message.reply(f"выберите что хотите изменить", reply_markup=ReplyKeyboardRemove())
    await bot.send_message(chat_id=message.chat.id, text = 'Кабинеты', reply_markup= await inline_keyboard_cabinets_admin(building, floor))
    await Map_navigation_update.cabinet.set()


@dp.callback_query_handler(cabinet_callback_update.filter(), state=Map_navigation_update.cabinet)
async def map_nav_admin_state_cabinet_update(call: CallbackQuery, state: FSMContext, callback_data: dict):
    logging.info(f'User({call.message.chat.id}) нажал на кнопку {call.data}')
    cabinet_name = callback_data.get('cabinet')
    await state.update_data(cabinet=cabinet_name)
    await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                text=f'Напишите изменения для <b>{cabinet_name}</b>:',
                                parse_mode='HTML', reply_markup=inline_keyboard_cancel_contact_center_admin())

    await Map_navigation_update.description.set()


@dp.message_handler(content_types=ContentType.ANY, state=Map_navigation_update.description)
async def map_nav_admin_state_description_update(message: types.Message, state: FSMContext):
    if message.content_type == 'text':
        await state.update_data(description = message.text.lower(), user_id=message.chat.id)
        data = await state.get_data()
        await bot.send_message(message.chat.id, text= f"Изменить описание?:\n"
                                                      f"{data['building']}\n"
                                                      f"{data['floor']}\n"
                                                      f"Название кабинета(кнопки) - {data['cabinet']}\n"
                                                      f"описание - {data['description']}", reply_markup=cancel_or_update_map_nav_admin())
        await state.reset_state(with_data=False)
    else:
        await message.answer('Ошибка - вы отправили не текст повторите')


@dp.callback_query_handler(text='update_map_navigation_admin', state=None)
async def map_nav_admin_state_update_final(call: CallbackQuery, state: FSMContext):
    try:
        data = await state.get_data()
        # await bot_delete_messages(call.message, 9)
        await db.update_map_nav_description_data(data['user_id'], data['building'], data['floor'], data['cabinet'], data['description'])
        await bot.delete_message(call.message.chat.id, call.message.message_id)
        await call.message.answer(f'описание изменено')
        await call.message.answer('Админ меню навигации', reply_markup = inline_keyboard_nav_university_admin_menu())
        logging.info(f'User({call.message.chat.id}) изменил информацию для кабинета')
    except Exception as e:
        await call.message.answer(f'Ошибка описание не отправлено, (Ошибка - {e})')
        print(e)


#################################################################################


@dp.callback_query_handler(text='delete_cabinet_admin', state=None)
async def callback_map_nav_admin_state_delete(call: CallbackQuery):
    await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                text='выбор для удаления', reply_markup=inline_keyboard_cancel_contact_center_admin())
    # await bot.send_message(chat_id=message.chat.id, text='ВЫБИРЕТЕ Школу', reply_markup=inline_keyboard_cancel_contact_center_admin())
    await call.message.answer('Выберите здание где хотите удалить кабинет\n'
                              'Для отмены нажмите сверху кнопку отмены',
                              reply_markup=keyboard_map_nav_choice_building())
    await Map_navigation_delete.building.set()


@dp.message_handler(lambda message: message.text in ['Новое здание'],state=Map_navigation_delete.building)
async def map_nav_admin_state_building_delete(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['building'] = message.text
    await bot.send_message(chat_id=message.chat.id, text='Выбор для удаления',
                           reply_markup=inline_keyboard_cancel_contact_center_admin())
    await message.reply("выбирете что хотите изменить", reply_markup=map_nav_admin_choice_floor_new())
    await Map_navigation_delete.floor.set()


@dp.message_handler(lambda message: message.text in ['Старое здание'],state=Map_navigation_delete.building)
async def map_nav_admin_state_building_delete(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['building'] = message.text
    await bot.send_message(chat_id=message.chat.id, text='Выбор для изменений',
                           reply_markup=inline_keyboard_cancel_contact_center_admin())
    await message.reply("выбирете что хотите изменить", reply_markup=map_nav_admin_choice_floor_old())
    await Map_navigation_delete.floor.set()


@dp.message_handler(lambda message: message.text in ['1 этаж', '2 этаж', "3 этаж", "4 этаж", "5 этаж", "6 этаж"],state=Map_navigation_delete.floor)
async def map_nav_admin_state_floor_delete(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['floor'] = message.text
    floor = data['floor']
    building = data['building']
    await message.reply(f"выберите что хотите изменить", reply_markup=ReplyKeyboardRemove())
    await bot.send_message(chat_id=message.chat.id, text = 'Кабинеты', reply_markup= await inline_keyboard_cabinets_admin(building, floor))
    await Map_navigation_delete.cabinet.set()


@dp.callback_query_handler(cabinet_callback_update.filter(), state=Map_navigation_delete.cabinet)
async def map_nav_admin_state_cabinet_delete(call: CallbackQuery, state: FSMContext, callback_data: dict):
    logging.info(f'User({call.message.chat.id}) нажал на кнопку {call.data}')
    cabinet_name = callback_data.get('cabinet')
    await state.update_data(cabinet=cabinet_name)
    await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                text=f'Удалить <b>{cabinet_name}? </b>:',
                                parse_mode='HTML', reply_markup=cancel_or_delete_map_nav_admin())

    await state.reset_state(with_data=False)

@dp.callback_query_handler(text='delete_map_navigation_admin', state=None)
async def map_nav_admin_state_delete_final(call: CallbackQuery, state: FSMContext):
    try:
        data = await state.get_data()
        # await bot_delete_messages(call.message, 9)
        await db.delete_map_nav_description_data(data['building'], data['floor'], data['cabinet'])
        await bot.delete_message(call.message.chat.id, call.message.message_id)
        await call.message.answer(f'описание удалено')
        await call.message.answer('Админ меню навигации', reply_markup = inline_keyboard_nav_university_admin_menu())
        logging.info(f'User({call.message.chat.id}) удалил информацию кабинета')
    except Exception as e:
        await call.message.answer(f'Ошибка описание не отправлено, (Ошибка - {e})')
        print(e)