import logging

from aiogram.types import CallbackQuery
from loader import dp, bot
from keyboards.inline.navigation_buttons import inline_keyboard_nav_unifi, inline_keyboard_contacts_center, \
    inline_keyboard_contacts_center_back, inline_keyboard_pps, inline_keyboard_pps_rectorat, \
    inline_keyboard_pps_rectorat_back, inline_keyboard_pps_shcool_back, inline_keyboard_map_nav, \
    inline_keyboard_old_building, inline_keyboard_new_building, inline_keyboard_new_building_back, \
    inline_keyboard_old_building_back, inline_keyboard_cabinets_dinamyc, inline_keyboard_pps_shcool_choise
from utils import db_api as db
from asyncio import create_task
from keyboards.inline import cabinet_callback, nav_center_callback


scholl_tuple = ('Школа менеджмента', 'Школа политики и права',
                'Школа предпринимательства и инноваций',
                'Школа Экономики и Финансов',
                'Школа Инженерного Менеджмента',
                'Высшая Школа Бизнеса', 'Ректорат')
position_tuple = ('Декан', 'Преподаватели', 'Ректор', 'Проректоры')
school_callback_tuple = ('management', 'law', 'inovation', 'economic', 'engineer', 'bussines')
floors_tuple = ('1 этаж', '2 этаж', '3 этаж', '4 этаж', '5 этаж', '6 этаж')
building_tuple = ('Новое здание', 'Старое здание')
building_call_tuple = ("new_", "old_")
floor_call_tuple = ("_first", "_second", "_third",
                    "_fourth", "_fifth", "_sixth")


async def check_photo_map_nav_function(keyboard, text_buttons, call: CallbackQuery):
    logging.info(f"User({call.message.chat.id}) вошел в навигацию ({call.data})")

    if call.message.content_type == 'photo':
        await bot.delete_message(call.message.chat.id, call.message.message_id)
        await bot.send_message(chat_id=call.message.chat.id,
                               text=text_buttons,
                               reply_markup=keyboard)
    else:
        await bot.edit_message_text(chat_id=call.message.chat.id,
                                    message_id=call.message.message_id,
                                    text=text_buttons,
                                    reply_markup=keyboard)
    await call.answer()


async def check_photo_is_none_map_nav_function(keyboard, description, photo_id, call: CallbackQuery):
    logging.info(f"User({call.message.chat.id}) вошел в  ({call.data})")
    if photo_id == "None":
        await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                    text=description,
                                    reply_markup=keyboard)
    else:
        await bot.delete_message(call.message.chat.id, call.message.message_id)
        await bot.send_photo(call.message.chat.id, photo_id, caption=description,
                             reply_markup=keyboard)
    await call.answer()


@dp.callback_query_handler(text='/nav_unifi')
async def callback_inline_nav_unifi(call: CallbackQuery):
    logging.info(f"User({call.message.chat.id}) вошел в Навигацию")
    await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                text='Навигация по университету', reply_markup=inline_keyboard_nav_unifi())
    await call.answer()


# ---------------------   Контакты ключевых центров ---------------------
@dp.callback_query_handler(text='contacts_center')
async def callback_inline_contacts_center(call: CallbackQuery):
    logging.info(f"User({call.message.chat.id}) вошел в Контакты ключевых центров")
    await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                text='Контакты ключевых центров', reply_markup=await inline_keyboard_contacts_center())
    await call.answer()


@dp.callback_query_handler(nav_center_callback.filter())
async def callback_inline_contacts_center_call(call: CallbackQuery, callback_data: dict):
    logging.info(f'call = {call.data}')
    callback_center = callback_data.get('id')
    description = await db.contact_center_description(callback_center)
    await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                text=description, reply_markup=inline_keyboard_contacts_center_back())
    await call.answer()


# --------------------- Контакты ключевых центров  КОНЕЦ   ---------------------

# --------------------- Профессорско-преподовательский состав---------------------
@dp.callback_query_handler(text='tutors_university')
async def callback_inline_tutors_university(call: CallbackQuery):
    logging.info(f"User({call.message.chat.id}) вошел в Профессорско-преподавательский состав")
    await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                text='Профессорско-преподавательский состав, выберите школу',
                                reply_markup=inline_keyboard_pps())
    await call.answer()


@dp.callback_query_handler(text='shcool_management')
async def callback_inline_shcool_management(call: CallbackQuery):
    schoolUni = "1"
    text_buttons = scholl_tuple[0]
    keyboard = inline_keyboard_pps_shcool_choise(schoolUni)
    await create_task(check_photo_map_nav_function(keyboard, text_buttons, call))


@dp.callback_query_handler(text='shcool_law')
async def callback_inline_shcool_law(call: CallbackQuery):
    schoolUni = "2"
    text_buttons = scholl_tuple[1]
    keyboard = inline_keyboard_pps_shcool_choise(schoolUni)
    await create_task(check_photo_map_nav_function(keyboard, text_buttons, call))


@dp.callback_query_handler(text='shcool_inovation')
async def callback_inline_shcool_inovation(call: CallbackQuery):
    schoolUni = "3"
    text_buttons = scholl_tuple[2]
    keyboard = inline_keyboard_pps_shcool_choise(schoolUni)
    await create_task(check_photo_map_nav_function(keyboard, text_buttons, call))


@dp.callback_query_handler(text='shcool_economic')
async def callback_inline_shcool_economic(call: CallbackQuery):
    schoolUni = "4"
    text_buttons = scholl_tuple[3]
    keyboard = inline_keyboard_pps_shcool_choise(schoolUni)
    await create_task(check_photo_map_nav_function(keyboard, text_buttons, call))


@dp.callback_query_handler(text='shcool_engineer')
async def callback_inline_shcool_engineer(call: CallbackQuery):
    schoolUni = "5"
    text_buttons = scholl_tuple[4]
    keyboard = inline_keyboard_pps_shcool_choise(schoolUni)
    await create_task(check_photo_map_nav_function(keyboard, text_buttons, call))


@dp.callback_query_handler(text='shcool_bussines')
async def callback_inline_shcool_bussines(call: CallbackQuery):
    schoolUni = "6"
    text_buttons = scholl_tuple[5]
    keyboard = inline_keyboard_pps_shcool_choise(schoolUni)
    await create_task(check_photo_map_nav_function(keyboard, text_buttons, call))


@dp.callback_query_handler(text='rectorat')
async def callback_inline_rectorat(call: CallbackQuery):
    text_buttons = scholl_tuple[6]
    keyboard = inline_keyboard_pps_rectorat()
    await create_task(check_photo_map_nav_function(keyboard, text_buttons, call))


# Хэндлеры описания деканов в ппс
@dp.callback_query_handler(
    lambda callback_tutors: callback_tutors.data and callback_tutors.data.startswith('callback_dekan_shcool_'))
async def callback_handler_dekan_pps(call: CallbackQuery):
    calldatalast = call.data[-1]
    for i in range(7):
        if calldatalast == str(i):
            keyboard = inline_keyboard_pps_shcool_back(school_callback_tuple[i-1])
            description = await db.pps_center_description(scholl_tuple[int(calldatalast) - 1], position_tuple[0])
            photo_id = await db.find_photoid_pps(scholl_tuple[int(calldatalast) - 1], position_tuple[0])
            await create_task(check_photo_is_none_map_nav_function(keyboard, description, photo_id, call))


# Хэндлеры описания преподавателей в ппс
@dp.callback_query_handler(
    lambda callback_tutors: callback_tutors.data and callback_tutors.data.startswith('callback_tutors_shcool_'))
async def callback_handler_tutors_pps(call: CallbackQuery):
    calldatalast = call.data[-1]
    for i in range(7):
        if calldatalast == str(i):
            keyboard = inline_keyboard_pps_shcool_back(school_callback_tuple[i-1])
            description = await db.pps_center_description(scholl_tuple[int(calldatalast) - 1], position_tuple[1])
            photo_id = await db.find_photoid_pps(scholl_tuple[int(calldatalast) - 1], position_tuple[1])
            await create_task(check_photo_is_none_map_nav_function(keyboard, description, photo_id, call))


@dp.callback_query_handler(text='rectorat_rector')
async def callback_inline_rectorat_rector(call: CallbackQuery):
    keyboard = inline_keyboard_pps_rectorat_back()
    description = await db.pps_center_description(scholl_tuple[6], position_tuple[2])
    photo_id = await db.find_photoid_pps(scholl_tuple[6], position_tuple[2])
    await create_task(check_photo_is_none_map_nav_function(keyboard, description, photo_id, call))


@dp.callback_query_handler(text='rectorat_humans')
async def callback_inline_rectorat_humans(call: CallbackQuery):
    keyboard = inline_keyboard_pps_rectorat_back()
    description = await db.pps_center_description(scholl_tuple[6], position_tuple[3])
    photo_id = await db.find_photoid_pps(scholl_tuple[6], position_tuple[3])
    await create_task(check_photo_is_none_map_nav_function(keyboard, description, photo_id, call))


# --------------------- Профессорско-преподовательский состав КОНЕЦ ---------------------

# ---------------------  Навигация по университету ---------------------
@dp.callback_query_handler(text='map_nav')
async def callback_inline_nav_unifi_map_nav(call: CallbackQuery):
    text_buttons = 'Карта-навигация по университету, выбирете здание:'
    keyboard = inline_keyboard_map_nav()
    await create_task(check_photo_map_nav_function(keyboard, text_buttons, call))


# ------------------------------------------------------
@dp.callback_query_handler(text='old_building')
async def callback_inline_nav_unifi_old_building(call: CallbackQuery):
    text_buttons = 'Старое здание университета, выберите этаж:'
    keyboard = inline_keyboard_old_building()
    await create_task(check_photo_map_nav_function(keyboard, text_buttons, call))


# -------------------------------------------------------
@dp.callback_query_handler(text='new_building')
async def callback_inline_nav_unifi_new_building(call: CallbackQuery):
    text_buttons = 'Новое здание университета, выберите этаж:'
    keyboard = inline_keyboard_new_building()
    await create_task(check_photo_map_nav_function(keyboard, text_buttons, call))


# хэндлеры старое здание
choise_cab = "Выберите кабинет:"

@dp.callback_query_handler(
    lambda callback_floors_old: callback_floors_old.data and callback_floors_old.data.startswith('old_building_'))
async def callback_inline_nav_unifi_old_building_first(call: CallbackQuery):
    call_data_last = call.data[12:-1] + call.data[-1]
    for floors in floor_call_tuple:
            if call_data_last == floors:
                floor_callback = floors_tuple[floor_call_tuple.index(floors)]
                keyboard = await inline_keyboard_cabinets_dinamyc(building_tuple[1], floor_callback)
                await create_task(check_photo_map_nav_function(keyboard, choise_cab, call))


# хэндлеры новое здание
@dp.callback_query_handler(
    lambda callback_floors_new: callback_floors_new.data and callback_floors_new.data.startswith('new_building_'))
async def callback_inline_nav_unifi_old_building_first(call: CallbackQuery):
    call_data_last = call.data[12:-1] + call.data[-1]
    for floors in floor_call_tuple:
            if call_data_last == floors:
                floor_callback = floors_tuple[floor_call_tuple.index(floors)]
                keyboard = await inline_keyboard_cabinets_dinamyc(building_tuple[0], floor_callback)
                await create_task(check_photo_map_nav_function(keyboard, choise_cab, call))


@dp.callback_query_handler(cabinet_callback.filter())
async def callback_inline(call: CallbackQuery, callback_data: dict):
    logging.info(f'call = {call.data}')
    callback_id = callback_data.get('id')
    description = await db.find_cabinet_description(callback_id)
    photo_id = await db.find_photoid_description(callback_id)
    floor = await db.find_floor_cabinet(callback_id)
    building = await db.find_building_cabinet(callback_id)
    if building == building_tuple[1]:
        for floors in floors_tuple:
            if floor == floors:
                building_callback = building_call_tuple[1]
                floor_callback = floor_call_tuple[floors_tuple.index(floors)]
                keyboard = inline_keyboard_old_building_back(building_callback, floor_callback)
                await create_task(check_photo_is_none_map_nav_function(keyboard, description, photo_id, call))
    elif building == building_tuple[0]:
        for floors in floors_tuple:
            if floor == floors:
                building_callback = building_call_tuple[0]
                floor_callback = floor_call_tuple[floors_tuple.index(floors)]
                keyboard = inline_keyboard_old_building_back(building_callback, floor_callback)
                await create_task(check_photo_is_none_map_nav_function(keyboard, description, photo_id, call))
    else:
        keyboard = inline_keyboard_new_building_back()
        await create_task(check_photo_is_none_map_nav_function(keyboard, description, photo_id, call))
    await call.answer()
# ---------------------Навигация по университету КОНЕЦ ---------------------
