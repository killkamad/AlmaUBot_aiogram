import ast
import logging

from aiogram.utils import exceptions
from aiogram import types
from aiogram.types import CallbackQuery, ContentType, ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove, \
    InlineKeyboardButton, InlineKeyboardMarkup
from loader import dp, bot
from keyboards.inline import inline_keyboard_nav_university_admin_menu, inline_keyboard_contact_center_admin, \
    cancel_or_send_contact_center_admin, cancel_or_update_contact_center_admin, \
    cancel_or_delete_contact_center_admin, inline_keyboard_contacts_center_delete, \
    inline_keyboard_contacts_center_update, \
    inline_keyboard_cancel_contact_center_admin, cancel_or_send_tutors_management, inline_keyboard_map_nav_admin_menu, \
    cancel_or_send_map_nav_admin, \
    inline_keyboard_cabinets_admin, cancel_or_update_map_nav_admin, cancel_or_delete_map_nav_admin, \
    inline_keyboard_cancel_map_nav_admin, \
    map_nav_admin_choice_floor_new_delete, map_nav_admin_choice_floor_old, keyboard_map_nav_choice_building, \
    map_nav_admin_choice_floor_old_delete, keyboard_map_nav_choice_building_delete, \
    keyboard_map_nav_choice_building_update, \
    map_nav_admin_choice_floor_new_update, map_nav_admin_choice_floor_old_update, map_nav_admin_choice_floor_new, \
    keyboard_pps_choice_position, keyboard_pps_choice_position_rector, keyboard_pps_choice_shcool, inline_keyboard_cancel_tutors_admin

import asyncio

from utils import db_api as db
from .admin_menu import admin_menu

from utils.delete_messages import bot_delete_messages
from aiogram.dispatcher import FSMContext
from states.admin import SendContactCenter, UpdateContactCenter, DeleteContactCenter, Pps_admin, Map_navigation, \
    Map_navigation_update, Map_navigation_delete

from keyboards.inline import cabinet_callback, cabinet_callback_update, nav_center_callback_update, \
    nav_center_callback_delete


@dp.callback_query_handler(text_contains='nav_university_admin_menu', state=['*'])
async def callback_inline_nav_university_admin_menu(call: CallbackQuery, state: FSMContext):
    logging.info(f'User({call.message.chat.id}) вошел в админ меню Навигации, call.data - {call.data}')
    await state.reset_state()
    await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                text='Админ меню Навигации:', reply_markup=inline_keyboard_nav_university_admin_menu())


@dp.callback_query_handler(text_contains='contacts_center_admin')
async def callback_inline_contacts_center_admin(call: CallbackQuery):
    logging.info(f'User({call.message.chat.id}) вошел в админ меню Навигации, call.data - {call.data}')
    await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                text='Админ меню ключевых центров:',
                                reply_markup=inline_keyboard_contact_center_admin())


#### Создания контакт центра ####
@dp.callback_query_handler(text='send_contact_center_admin', state=None)
async def callback_inline_send_contact_center_admin(call: CallbackQuery):
    logging.info(f'User({call.message.chat.id}) нажал на кнопку {call.data}')
    await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                text='Напишите название контакт центра, например (бухгалтерия)',
                                reply_markup=inline_keyboard_cancel_contact_center_admin())
    await SendContactCenter.name.set()


@dp.callback_query_handler(text='cancel_step_contact_center_admin', state=['*'])
async def callback_inline_cancel_step(call: CallbackQuery, state: FSMContext):
    logging.info(f'User({call.message.chat.id}) нажал на кнопку {call.data}')
    await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                text='Админ меню ключевых центров',
                                reply_markup=inline_keyboard_contact_center_admin())
    await state.reset_state()


# Проверка центра на текст
@dp.message_handler(content_types=ContentType.ANY, state=SendContactCenter.name)
async def message_send_contact_center_name(message: types.Message, state: FSMContext):
    if message.content_type == 'text' and len(message.text) <= 29:
        try:
            await bot.edit_message_reply_markup(message.chat.id, message.message_id - 1)
        except:
            pass
        await state.update_data(name=message.text.lower(),
                                user_id=message.chat.id)
        await bot.send_message(message.chat.id, 'Отправьте описание контакт центра',
                               reply_markup=inline_keyboard_cancel_contact_center_admin())
        await SendContactCenter.description.set()
    else:
        try:
            await bot.edit_message_reply_markup(message.chat.id, message.message_id - 1)
        except:
            pass
        print(message.content_type)
        await bot.send_message(message.chat.id,
                               'Ошибка - ваше сообщение должно содержать только текст и не превышать 29 символов.\nПовторите название для кнопки, например (бухгалтерия):',
                               reply_markup=inline_keyboard_cancel_contact_center_admin())


# Проверка описания центра на текст
@dp.message_handler(content_types=ContentType.ANY, state=SendContactCenter.description)
async def message_send_contact_center_description(message: types.Message, state: FSMContext):
    if message.content_type == 'text':
        try:
            await bot.edit_message_reply_markup(message.chat.id, message.message_id - 1)
        except:
            pass
        await state.update_data(description=message.text.lower())
        data = await state.get_data()
        txt = f'Название кнопки будет: {data["name"]}'
        await bot.send_message(message.chat.id, txt, reply_markup=cancel_or_send_contact_center_admin())
        await state.reset_state(with_data=False)
    else:
        try:
            await bot.edit_message_reply_markup(message.chat.id, message.message_id - 1)
        except:
            pass
        await message.answer('Ошибка - вы отправили не текст повторите')


# создание контакт центра в базе данных
@dp.callback_query_handler(text='send_contact_center', state=None)
async def callback_inline_send_contact_center_final(call: CallbackQuery, state: FSMContext):
    try:
        data = await state.get_data()
        await db.add_contact_center_data(data['user_id'], data['description'], data["name"])
        logging.info(f'User({call.message.chat.id}) отправил контакты для {data["name"]}')
        await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                text=f'описание <b>{data["name"]}</b> отправлено \n'
                                      'Админ меню ключевых центров:',
                                reply_markup=inline_keyboard_contact_center_admin())
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


@dp.callback_query_handler(nav_center_callback_update.filter(), state=UpdateContactCenter.name)
async def callback_inline_updade_contact_center(call: CallbackQuery, state: FSMContext, callback_data: dict):
    logging.info(f'User({call.message.chat.id}) нажал на кнопку {call.data}')
    callback_name = callback_data.get('name')
    await state.update_data(name=callback_name, user_id=call.message.chat.id)
    await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                           text=f'Напишете заново новую информацию для <b>{callback_name}</b>:',
                           parse_mode='HTML', reply_markup=inline_keyboard_cancel_contact_center_admin())
    await UpdateContactCenter.description.set()


@dp.message_handler(content_types=ContentType.ANY, state=UpdateContactCenter.description)
async def updade_contact_center_step(message: types.Message, state: FSMContext):
    await UpdateContactCenter.description.set()
    if message.content_type == 'text':
        try:
            await bot.edit_message_reply_markup(message.chat.id, message.message_id - 1)
        except:
            pass
        await state.update_data(description=message.text.lower())
        data = await state.get_data()
        await bot.send_message(message.chat.id, text=f'Название кнопки: <b>{data["name"]}</b> \n'
                                                     f'Новое описание:<b>{data["description"]}</b>',
                               reply_markup=cancel_or_update_contact_center_admin())
        await state.reset_state(with_data=False)
    else:
        try:
            await bot.edit_message_reply_markup(message.chat.id, message.message_id - 1)
        except:
            pass
        await message.answer('Ошибка - вы отправили не текст повторите', reply_markup=inline_keyboard_cancel_contact_center_admin())


@dp.callback_query_handler(text='update_info_contact_center_admin', state=None)
async def callback_inline_send_schedule(call: CallbackQuery, state: FSMContext):
    try:
        data = await state.get_data()
        try:
            await bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id)
        except:
            pass
        await db.update_contact_center_data(data['user_id'], data['description'], data["name"])
        await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                           text=f'описание <b>{data["name"]}</b> успешно обновлено \n'
                           'Админ меню ключевых центров:',
                           parse_mode='HTML', reply_markup=inline_keyboard_contact_center_admin())
        logging.info(f'User({call.message.chat.id}) обновил описание для {data["name"]}')
    except Exception as e:
        try:
            await bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id)
        except:
            pass
        await call.message.answer(f'(Ошибка - {e})')
        logging.info(f'Ошибка - {e}')


##### Удаление контакт центра
@dp.callback_query_handler(text='delete_contact_center_admin', state=None)
async def callback_inline_delete_contact_center_admin(call: CallbackQuery):
    logging.info(f'User({call.message.chat.id}) нажал на кнопку {call.data}')
    await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                           text=f'Выберите кнопку для удаление:',
                           reply_markup=await inline_keyboard_contacts_center_delete())
    await DeleteContactCenter.name.set()


@dp.callback_query_handler(nav_center_callback_delete.filter(), state=DeleteContactCenter.name)
async def callback_inline_updade_contact_center(call: CallbackQuery, state: FSMContext, callback_data: dict):
    logging.info(f'User({call.message.chat.id}) нажал на кнопку {call.data}')
    callback_name = callback_data.get('name')
    await state.update_data(name=callback_name, user_id=call.message.chat.id)
    await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                           text=f'Вы точно уверены, что хотите удалить информацию  <b>{callback_name}</b>:',
                           reply_markup=cancel_or_delete_contact_center_admin())
    await DeleteContactCenter.confirm_delete.set()


@dp.callback_query_handler(text='delete_info_contact_center_admin', state=DeleteContactCenter.confirm_delete)
async def callback_inline_send_schedule(call: CallbackQuery, state: FSMContext):
    try:
        data = await state.get_data()
        await db.delete_contact_center_button(data["name"])
        await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                           text=f'ключевой центр <b>{data["name"]}</b> успешно удален из базы данных \n'
                                f'Админ меню ключевых центров:',
                           reply_markup=inline_keyboard_contact_center_admin())
        await state.reset_state()
        logging.info(f'User({call.message.chat.id}) удалил ключевой центр для {data["name"]}')
    except Exception as e:
        try:
            await bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id)
        except:
            pass
        await call.message.answer(f'(Ошибка - {e})')
        logging.info(f'Ошибка - {e}')


###################################профессорско преподвательский состав изменение информации#################################
@dp.callback_query_handler(text='tutors_university_admin', state=None)
async def callback_tutors_university_admin_state(call: CallbackQuery):
    await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                           text=f'Выберите школу для которой хотите ввести изменения',
                           reply_markup=keyboard_pps_choice_shcool())
    await Pps_admin.shcool.set()


@dp.callback_query_handler(lambda shcool: shcool.data and shcool.data.startswith('choice_shcool_admin'),
                           state=Pps_admin.shcool)
async def pps_admin_state_shcool(call: CallbackQuery, state: FSMContext):
    shcoolnumber = call.data[-1]
    if shcoolnumber == '1':
        async with state.proxy() as data:
            data['shcool'] = "Школа менеджмента"
    if shcoolnumber == '2':
        async with state.proxy() as data:
            data['shcool'] = "Школа политики и права"
    if shcoolnumber == '3':
        async with state.proxy() as data:
            data['shcool'] = "Школа Инженерного Менеджмента"
    if shcoolnumber == '4':
        async with state.proxy() as data:
            data['shcool'] = "Школа предпринимательства и инноваций"
    if shcoolnumber == '5':
        async with state.proxy() as data:
            data['shcool'] = "Высшая Школа Бизнеса"
    if shcoolnumber == '6':
        async with state.proxy() as data:
            data['shcool'] = "Школа Экономики и Финансов"
    await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                           text=f'выбирете что хотите изменить',
                           reply_markup=keyboard_pps_choice_position())
    await Pps_admin.position.set()


@dp.callback_query_handler(text='choice_rectorat_admin', state=Pps_admin.shcool)
async def callback_tutors_university_admin_state(call: CallbackQuery, state: FSMContext): 
    async with state.proxy() as data:
        data['shcool'] = 'Ректорат'
    await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                           text=f'выбирете что хотите изменить',
                           reply_markup=keyboard_pps_choice_position_rector())
    await Pps_admin.position.set()


@dp.callback_query_handler(lambda shcool: shcool.data and shcool.data.startswith('choice_position_admin'),
                           state=Pps_admin.position)
async def pps_admin_state_position(call: CallbackQuery, state: FSMContext):
    positionnum = call.data[-1]
    if positionnum == '1':
        async with state.proxy() as data:
            data['position'] = "Декан"
    if positionnum == '2':
        async with state.proxy() as data:
            data['position'] = "Преподаватели"
    if positionnum == '3':
        async with state.proxy() as data:
            data['position'] = "Ректор"
    if positionnum == '4':
        async with state.proxy() as data:
            data['position'] = "Проректоры"
    await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
            text=f"Напишите описание которое хотите изменить для {data['position']} {data['shcool']}",
            reply_markup=inline_keyboard_cancel_tutors_admin())
    await Pps_admin.description.set()


@dp.message_handler(content_types=ContentType.ANY, state=Pps_admin.description)
async def message_send_tutors_management(message: types.Message, state: FSMContext):
    if message.content_type == 'text':
        await state.update_data(description=message.text.lower(), user_id=message.chat.id)
        data = await state.get_data()
        try:
            await bot.edit_message_reply_markup(message.chat.id, message.message_id - 1)
        except:
            pass
        await bot.send_message(message.chat.id, text='Отправить это описание?',
                               reply_markup=cancel_or_send_tutors_management())
        await state.reset_state(with_data=False)
    else:
        try:
            await bot.edit_message_reply_markup(message.chat.id, message.message_id - 1)
        except:
            pass
        await message.answer('Ошибка - вы отправили не текст повторите')


@dp.callback_query_handler(text='send_tutors_management', state=None)
async def callback_inline_send_tutors_management_final(call: CallbackQuery, state: FSMContext):
    try:
        data = await state.get_data()
        await db.add_pps_data(data['user_id'], data['shcool'], data['position'], data['description'])
        await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                           text= f'Описание отправлено'
                           'Админ меню навигации',
                           reply_markup=inline_keyboard_nav_university_admin_menu())
        logging.info(f'User({call.message.chat.id}) отправил информацию для преподавателей менеджмента')
    except Exception as e:
        await call.message.answer(f'Ошибка описание не отправлено, (Ошибка - {e})')
        try:
            await bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id - 1)
        except:
            pass
        print(e)


@dp.callback_query_handler(text='cancel_step_tutors_admin', state=['*'])
async def callback_inline_cancel_step(call: CallbackQuery, state: FSMContext):
    logging.info(f'User({call.message.chat.id}) нажал на кнопку {call.data}')
    # await bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id)
    await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                           text=f'Выберите школу для которой хотите ввести изменения',
                           reply_markup=keyboard_pps_choice_shcool())
    await state.reset_state()
    await Pps_admin.shcool.set()


#############админ меню карты навигации
@dp.callback_query_handler(text_contains='map_nav_admin')
async def callback_inline_contacts_center_admin(call: CallbackQuery):
    logging.info(f'User({call.message.chat.id}) вошел в админ карты-навигации, call.data - {call.data}')
    await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                text='Админ меню карты-навигации:', reply_markup=inline_keyboard_map_nav_admin_menu())


@dp.callback_query_handler(text='send_cabinet_admin', state=None)
async def callback_map_nav_admin_state(call: CallbackQuery):
    await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                text='выберите здание где хотите добавить кабинет', reply_markup=keyboard_map_nav_choice_building())
    await Map_navigation.building.set()


@dp.callback_query_handler(text='new_building_choice_admin', state=Map_navigation.building)
async def map_nav_admin_state_building1(call: CallbackQuery, state: FSMContext):
    databuilding = 'Новое здание'
    async with state.proxy() as data:
        data['building'] = databuilding
    await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                text='Выберите этаж в каком хотите добавить кабинет', reply_markup=map_nav_admin_choice_floor_new())
    await Map_navigation.floor.set()


@dp.callback_query_handler(text='old_building_choice_admin', state=Map_navigation.building)
async def map_nav_admin_state_building2(call: CallbackQuery, state: FSMContext):
    databuilding = 'Старое здание'
    async with state.proxy() as data:
        data['building'] = databuilding
    await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                text='Выберите этаж в каком хотите добавить кабинет', reply_markup=map_nav_admin_choice_floor_old())
    await Map_navigation.floor.set()


@dp.callback_query_handler(lambda floor: floor.data and floor.data.startswith('floor_choice_admin'),
                           state=Map_navigation.floor)
async def map_nav_admin_state_floor(call: CallbackQuery, state: FSMContext):
    floornumber = call.data[-1]
    if floornumber == '1':
        async with state.proxy() as data:
            data['floor'] = "1 этаж"
    if floornumber == '2':
        async with state.proxy() as data:
            data['floor'] = "2 этаж"
    if floornumber == '3':
        async with state.proxy() as data:
            data['floor'] = "3 этаж"
    if floornumber == '4':
        async with state.proxy() as data:
            data['floor'] = "4 этаж"
    if floornumber == '5':
        async with state.proxy() as data:
            data['floor'] = "5 этаж"
    if floornumber == '6':
        async with state.proxy() as data:
            data['floor'] = "6 этаж"
    print(data['floor'])
    await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                text=f"Напишите название(например:101 кабинет) которое хотите добавить для {data['building']} {data['floor']}",
                                reply_markup=inline_keyboard_cancel_map_nav_admin())
    await Map_navigation.cabinet.set()


@dp.message_handler(content_types=ContentType.ANY, state=Map_navigation.cabinet)
async def map_nav_admin_state_cabinet(message: types.Message, state: FSMContext):
    try:
        data = await state.get_data()
        cabinets = await db.select_cabinet_admin_check()
        checkcabinet = True
        for item in cabinets:
            if item['cabinet'] == message.text:
                checkcabinet = False
            else:
                continue
        if message.content_type == 'text' and checkcabinet == True:
            async with state.proxy() as data:
                data['cabinet'] = message.text
            try:
                await bot.edit_message_reply_markup(message.chat.id, message.message_id - 1)
            except:
                pass
            await message.reply(f"Напишите описание для {data['cabinet']} {data['building']} {data['floor']} ",
                                reply_markup=inline_keyboard_cancel_map_nav_admin())
            await Map_navigation.description.set()
        else:
            try:
                await bot.edit_message_reply_markup(message.chat.id, message.message_id - 1)
            except:
                pass
            await message.answer('Ошибка - вы отправили не текст или название кабинета уже существует повторите',
                                 reply_markup=inline_keyboard_cancel_map_nav_admin())
    except Exception as e:
        await message.answer(f'Ошибка  (Ошибка - {e})')
        print(e)


@dp.message_handler(content_types=ContentType.ANY, state=Map_navigation.description)
async def map_nav_admin_state_description(message: types.Message, state: FSMContext):
    if message.content_type == 'text':
        await state.update_data(description=message.text.lower(), user_id=message.chat.id)
        data = await state.get_data()
        try:
            await bot.edit_message_reply_markup(message.chat.id, message.message_id - 1)
        except:
            pass
        await bot.send_message(message.chat.id, text=f"Отправить описание?:\n"
                                                     f"{data['building']}\n"
                                                     f"{data['floor']}\n"
                                                     f"Название кабинета(кнопки) - {data['cabinet']}\n"
                                                     f"описание - {data['description']}",
                               reply_markup=cancel_or_send_map_nav_admin())
        await state.reset_state(with_data=False)
    else:
        try:
            await bot.edit_message_reply_markup(message.chat.id, message.message_id - 1)
        except:
            pass
        await message.answer('Ошибка - вы отправили не текст повторите',
                             reply_markup=inline_keyboard_cancel_map_nav_admin())


@dp.callback_query_handler(text='send_map_navigation_admin', state=None)
async def map_nav_admin_state_send_final(call: CallbackQuery, state: FSMContext):
    try:
        data = await state.get_data()
        await db.add_map_navigation_data(data['user_id'], data['building'], data['floor'], data['cabinet'],
                                         data['description'])
        await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                text=f"{data['cabinet']} для {data['building']} {data['floor']} отправлен\n"
                                "Админ меню карт-навигации",
                                reply_markup=inline_keyboard_map_nav_admin_menu())
        
        logging.info(f'User({call.message.chat.id}) отправил информацию для кабинета')
    except Exception as e:
        await call.message.answer(f'Ошибка описание не отправлено, (Ошибка - {e})')
        print(e)


########################################Обновление Кабинетов###############################################


@dp.callback_query_handler(text='update_cabinet_admin', state=None)
async def callback_map_nav_admin_state_update(call: CallbackQuery):
    await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                text='выберите здание где хотите обновить кабинет', reply_markup=keyboard_map_nav_choice_building_update())
    await Map_navigation_update.building.set()


@dp.callback_query_handler(text='new_building_choice_admin_update', state=Map_navigation_update.building)
async def map_nav_admin_state_building_update(call: CallbackQuery, state: FSMContext):
    databuilding = 'Новое здание'
    async with state.proxy() as data:
        data['building'] = databuilding
    await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                text='Выберите этаж в каком хотите изменить описание кабинет', 
                                reply_markup=map_nav_admin_choice_floor_new_update())
    await Map_navigation_update.floor.set()


@dp.callback_query_handler(text='old_building_choice_admin_update', state=Map_navigation_update.building)
async def map_nav_admin_state_building_update(call: CallbackQuery, state: FSMContext):
    databuilding = 'Старое здание'
    async with state.proxy() as data:
        data['building'] = databuilding
    print(data['building'])
    await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                text='Выберите этаж в каком хотите изменить описание кабинет', 
                                reply_markup=map_nav_admin_choice_floor_old_update())
    await Map_navigation_update.floor.set()


@dp.callback_query_handler(lambda floor: floor.data and floor.data.startswith('floor_choice_admin_update'),
                           state=Map_navigation_update.floor)
async def map_nav_admin_state_floor_update(call: CallbackQuery, state: FSMContext):
    floornumber = call.data[-1]
    if floornumber == '1':
        async with state.proxy() as data:
            data['floor'] = "1 этаж"
    if floornumber == '2':
        async with state.proxy() as data:
            data['floor'] = "2 этаж"
    if floornumber == '3':
        async with state.proxy() as data:
            data['floor'] = "3 этаж"
    if floornumber == '4':
        async with state.proxy() as data:
            data['floor'] = "4 этаж"
    if floornumber == '5':
        async with state.proxy() as data:
            data['floor'] = "5 этаж"
    if floornumber == '6':
        async with state.proxy() as data:
            data['floor'] = "6 этаж"
    floor = data['floor']
    building = data['building']
    await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                text='Выберите кабинет для изменения:', 
                                reply_markup=await inline_keyboard_cabinets_admin(building, floor))
    await Map_navigation_update.cabinet.set()


@dp.callback_query_handler(cabinet_callback_update.filter(), state=Map_navigation_update.cabinet)
async def map_nav_admin_state_cabinet_update(call: CallbackQuery, state: FSMContext, callback_data: dict):
    logging.info(f'User({call.message.chat.id}) нажал на кнопку {call.data}')
    cabinet_name = callback_data.get('cabinet')
    await state.update_data(cabinet=cabinet_name)
    await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                text=f'Напишите изменения для <b>{cabinet_name}</b>:',
                                parse_mode='HTML', reply_markup=inline_keyboard_cancel_map_nav_admin())

    await Map_navigation_update.description.set()


@dp.message_handler(content_types=ContentType.ANY, state=Map_navigation_update.description)
async def map_nav_admin_state_description_update(message: types.Message, state: FSMContext):
    if message.content_type == 'text':
        await state.update_data(description=message.text.lower(), user_id=message.chat.id)
        data = await state.get_data()
        await bot.edit_message_reply_markup(message.chat.id, message.message_id - 1)
        await bot.send_message(message.chat.id, text=f"Изменить описание?:\n"
                                                     f"{data['building']}\n"
                                                     f"{data['floor']}\n"
                                                     f"Название кабинета(кнопки) - {data['cabinet']}\n"
                                                     f"описание - {data['description']}",
                               reply_markup=cancel_or_update_map_nav_admin())
        await state.reset_state(with_data=False)
    else:
        await message.answer('Ошибка - вы отправили не текст повторите')


@dp.callback_query_handler(text='update_map_navigation_admin', state=None)
async def map_nav_admin_state_update_final(call: CallbackQuery, state: FSMContext):
    try:
        data = await state.get_data()
        await db.update_map_nav_description_data(data['user_id'], data['building'], data['floor'], data['cabinet'],
                                                 data['description'])
        await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                text=f"{data['cabinet']} для {data['building']} {data['floor']} изменен\n"
                                "Админ меню карт-навигации",
                                reply_markup=inline_keyboard_map_nav_admin_menu())
        logging.info(f'User({call.message.chat.id}) изменил информацию для кабинета')
    except Exception as e:
        await call.message.answer(f'Ошибка описание не отправлено, (Ошибка - {e})')
        print(e)


#######################################  Удаление Кабинетов   ##########################################


@dp.callback_query_handler(text='delete_cabinet_admin', state=None)
async def callback_map_nav_admin_state_delete(call: CallbackQuery):
    await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                text='Выберите здание где хотите удалить кабинет', reply_markup=keyboard_map_nav_choice_building_delete())
    await Map_navigation_delete.building.set()


@dp.callback_query_handler(text='new_building_choice_admin_delete', state=Map_navigation_delete.building)
async def map_nav_admin_state_building1_delete(call: CallbackQuery, state: FSMContext):
    databuilding = 'Новое здание'
    async with state.proxy() as data:
        data['building'] = databuilding
    await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                text='Выберите этаж в каком хотите удалить кабинет', reply_markup=map_nav_admin_choice_floor_new_delete())
    await Map_navigation_delete.floor.set()


@dp.callback_query_handler(text='old_building_choice_admin_delete', state=Map_navigation_delete.building)
async def map_nav_admin_state_building2_delete(call: CallbackQuery, state: FSMContext):
    databuilding = 'Старое здание'
    async with state.proxy() as data:
        data['building'] = databuilding
    await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                text='Выберите этаж в каком хотите удалить кабинет', reply_markup=map_nav_admin_choice_floor_old_delete())
    await Map_navigation_delete.floor.set()


@dp.callback_query_handler(lambda floor: floor.data and floor.data.startswith('floor_choice_admin_delete'),
                           state=Map_navigation_delete.floor)
async def map_nav_admin_state_floor(call: CallbackQuery, state: FSMContext):
    floornumber = call.data[-1]
    if floornumber == '1':
        async with state.proxy() as data:
            data['floor'] = "1 этаж"
    if floornumber == '2':
        async with state.proxy() as data:
            data['floor'] = "2 этаж"
    if floornumber == '3':
        async with state.proxy() as data:
            data['floor'] = "3 этаж"
    if floornumber == '4':
        async with state.proxy() as data:
            data['floor'] = "4 этаж"
    if floornumber == '5':
        async with state.proxy() as data:
            data['floor'] = "5 этаж"
    if floornumber == '6':
        async with state.proxy() as data:
            data['floor'] = "6 этаж"
    floor = data['floor']
    building = data['building']
    await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                text='Выберите какой кабинет хотите удалить',
                                reply_markup=await inline_keyboard_cabinets_admin(building, floor))
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
        await db.delete_map_nav_description_data(data['building'], data['floor'], data['cabinet'])
        await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                text=f"{data['cabinet']} для {data['building']} {data['floor']} удален\n"
                                "Админ меню карт-навигации",
                                reply_markup=inline_keyboard_map_nav_admin_menu())
        logging.info(f'User({call.message.chat.id}) удалил информацию кабинета')
    except Exception as e:
        await call.message.answer(f'Ошибка описание не отправлено, (Ошибка - {e})')
        print(e)


@dp.callback_query_handler(text='cancel_step_map_nav_admin', state=['*'])
async def callback_inline_cancel_step(call: CallbackQuery, state: FSMContext):
    logging.info(f'User({call.message.chat.id}) нажал на кнопку {call.data}')
    await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                text="Админ меню карт-навигации",
                                reply_markup=inline_keyboard_map_nav_admin_menu())
    await state.reset_state()
