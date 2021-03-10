import ast
import logging

from aiogram.types import CallbackQuery
from loader import dp, bot
from keyboards.inline.navigation_buttons import inline_keyboard_nav_unifi, inline_keyboard_contacts_center, \
    inline_keyboard_contacts_center_back, inline_keyboard_pps, inline_keyboard_pps_rectorat, \
    inline_keyboard_pps_rectorat_back, inline_keyboard_pps_shcool_bussines_back, \
    inline_keyboard_pps_shcool_engineer_back, inline_keyboard_pps_shcool_economic_back, \
    inline_keyboard_pps_shcool_inovation_back, inline_keyboard_pps_shcool_law_back, \
    inline_keyboard_pps_shcool_management_back, inline_keyboard_map_nav, \
    inline_keyboard_old_building, inline_keyboard_new_building, inline_keyboard_new_building_back, \
    inline_keyboard_old_building_back, inline_keyboard_cabinets_first_old, inline_keyboard_cabinets_second_old, \
    inline_keyboard_cabinets_third_old, inline_keyboard_cabinets_first_new, inline_keyboard_cabinets_second_new, \
    inline_keyboard_cabinets_third_new, inline_keyboard_cabinets_fourth_new, inline_keyboard_cabinets_fourth_old, \
    inline_keyboard_cabinets_fifth_new, inline_keyboard_cabinets_sixth_new, inline_keyboard_pps_shcool_choise
from utils import db_api as db
from asyncio import create_task
from keyboards.inline import cabinet_callback, nav_center_callback


scholl_tuple = ('Школа менеджмента', 'Школа политики и права', 
                'Школа предпринимательства и инноваций',
                'Школа Экономики и Финансов',
                'Школа Инженерного Менеджмента',
                'Высшая Школа Бизнеса', 'Ректорат')
position_tuple = ('Декан', 'Преподаватели', 'Ректор', 'Проректоры')


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


##########################  Контакты ключевых центров ##############################
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

    # @dp.callback_query_handler(text_contains="['contacts_center_call'")
    # async def callback_inline_contacts_center_call(call: CallbackQuery):
    #     logging.info(f'call = {call.data}')
    #     valueFromCallBack = ast.literal_eval(call.data)[1]
    #     description = await db.contact_center_description(valueFromCallBack)
    #     await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
    #                                 text=description, reply_markup=inline_keyboard_contacts_center_back())


##########################  Контакты ключевых центров  КОНЕЦ   ##############################

##########################  Профессорско-преподовательский состав ###########################
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

####### Хэндлеры описания деканов в ппс
@dp.callback_query_handler(lambda callback_tutors: callback_tutors.data and callback_tutors.data.startswith('callback_dekan_shcool_'))
async def callback_handler_dekan_pps(call: CallbackQuery):
    calldatalast = call.data[-1]
    if calldatalast == '1':
            keyboard = inline_keyboard_pps_shcool_management_back()
            description = await db.pps_center_description(scholl_tuple[int(calldatalast)-1], position_tuple[0])
            photo_id = await db.find_photoid_pps(scholl_tuple[int(calldatalast)-1], position_tuple[0])
            await create_task(check_photo_is_none_map_nav_function(keyboard, description, photo_id, call))
    if calldatalast == '2':
            keyboard = inline_keyboard_pps_shcool_law_back()
            description = await db.pps_center_description(scholl_tuple[int(calldatalast)-1], position_tuple[0])
            photo_id = await db.find_photoid_pps(scholl_tuple[int(calldatalast)-1], position_tuple[0])
            await create_task(check_photo_is_none_map_nav_function(keyboard, description, photo_id, call))
    if calldatalast == '3':
            keyboard = inline_keyboard_pps_shcool_inovation_back()
            description = await db.pps_center_description(scholl_tuple[int(calldatalast)-1], position_tuple[0])
            photo_id = await db.find_photoid_pps(scholl_tuple[int(calldatalast)-1], position_tuple[0])
            await create_task(check_photo_is_none_map_nav_function(keyboard, description, photo_id, call))
    if calldatalast == '4':
            keyboard = inline_keyboard_pps_shcool_economic_back()
            description = await db.pps_center_description(scholl_tuple[int(calldatalast)-1], position_tuple[0])
            photo_id = await db.find_photoid_pps(scholl_tuple[int(calldatalast)-1], position_tuple[0])
            await create_task(check_photo_is_none_map_nav_function(keyboard, description, photo_id, call))
    if calldatalast == '5':
            keyboard = inline_keyboard_pps_shcool_engineer_back()
            description = await db.pps_center_description(scholl_tuple[int(calldatalast)-1], position_tuple[0])
            photo_id = await db.find_photoid_pps(scholl_tuple[int(calldatalast)-1], position_tuple[0])
            await create_task(check_photo_is_none_map_nav_function(keyboard, description, photo_id, call))
    if calldatalast == '6':
            keyboard = inline_keyboard_pps_shcool_bussines_back()
            description = await db.pps_center_description(scholl_tuple[int(calldatalast)-1], position_tuple[0])
            photo_id = await db.find_photoid_pps(scholl_tuple[int(calldatalast)-1], position_tuple[0])
            await create_task(check_photo_is_none_map_nav_function(keyboard, description, photo_id, call))


####### Хэндлеры описания преподавателей в ппс
@dp.callback_query_handler(lambda callback_tutors: callback_tutors.data and callback_tutors.data.startswith('callback_tutors_shcool_'))
async def callback_handler_tutors_pps(call: CallbackQuery):
    calldatalast = call.data[-1]
    if calldatalast == '1':
            keyboard = inline_keyboard_pps_shcool_management_back()
            description = await db.pps_center_description(scholl_tuple[int(calldatalast)-1], position_tuple[1])
            photo_id = await db.find_photoid_pps(scholl_tuple[int(calldatalast)-1], position_tuple[1])
            await create_task(check_photo_is_none_map_nav_function(keyboard, description, photo_id, call))
    if calldatalast == '2':
            keyboard = inline_keyboard_pps_shcool_law_back()
            description = await db.pps_center_description(scholl_tuple[int(calldatalast)-1], position_tuple[1])
            photo_id = await db.find_photoid_pps(scholl_tuple[int(calldatalast)-1], position_tuple[1])
            await create_task(check_photo_is_none_map_nav_function(keyboard, description, photo_id, call))
    if calldatalast == '3':
            keyboard = inline_keyboard_pps_shcool_inovation_back()
            description = await db.pps_center_description(scholl_tuple[int(calldatalast)-1], position_tuple[1])
            photo_id = await db.find_photoid_pps(scholl_tuple[int(calldatalast)-1], position_tuple[1])
            await create_task(check_photo_is_none_map_nav_function(keyboard, description, photo_id, call))
    if calldatalast == '4':
            keyboard = inline_keyboard_pps_shcool_economic_back()
            description = await db.pps_center_description(scholl_tuple[int(calldatalast)-1], position_tuple[1])
            photo_id = await db.find_photoid_pps(scholl_tuple[int(calldatalast)-1], position_tuple[1])
            await create_task(check_photo_is_none_map_nav_function(keyboard, description, photo_id, call))
    if calldatalast == '5':
            keyboard = inline_keyboard_pps_shcool_engineer_back()
            description = await db.pps_center_description(scholl_tuple[int(calldatalast)-1], position_tuple[1])
            photo_id = await db.find_photoid_pps(scholl_tuple[int(calldatalast)-1], position_tuple[1])
            await create_task(check_photo_is_none_map_nav_function(keyboard, description, photo_id, call))
    if calldatalast == '6':
            keyboard = inline_keyboard_pps_shcool_bussines_back()
            description = await db.pps_center_description(scholl_tuple[int(calldatalast)-1], position_tuple[1])
            photo_id = await db.find_photoid_pps(scholl_tuple[int(calldatalast)-1], position_tuple[1])
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

##########################  Профессорско-преподовательский состав КОНЕЦ ###########################


##########################  Навигация по университету #############################################
@dp.callback_query_handler(text='map_nav')
async def callback_inline_nav_unifi_map_nav(call: CallbackQuery):
    text_buttons = 'Карта-навигация по университету, выбирете здание:'
    keyboard = inline_keyboard_map_nav()
    await create_task(check_photo_map_nav_function(keyboard, text_buttons, call))


########
@dp.callback_query_handler(text='old_building')
async def callback_inline_nav_unifi_old_building(call: CallbackQuery):
    text_buttons = 'Старое здание университета, выберите этаж:'
    keyboard = inline_keyboard_old_building()
    await create_task(check_photo_map_nav_function(keyboard, text_buttons, call))


#######
@dp.callback_query_handler(text='new_building')
async def callback_inline_nav_unifi_new_building(call: CallbackQuery):
    text_buttons = 'Новое здание университета, выберите этаж:'
    keyboard = inline_keyboard_new_building()
    await create_task(check_photo_map_nav_function(keyboard, text_buttons, call))


######### хэндлеры старое здание
choise_cab = "Выберите кабинет:"
@dp.callback_query_handler(text='old_building_first')
async def callback_inline_nav_unifi_old_building_first(call: CallbackQuery):
    keyboard = await inline_keyboard_cabinets_first_old()
    await create_task(check_photo_map_nav_function(keyboard, choise_cab, call))


@dp.callback_query_handler(text='old_building_second')
async def callback_inline_nav_unifi_old_building_second(call: CallbackQuery):
    keyboard = await inline_keyboard_cabinets_second_old()
    await create_task(check_photo_map_nav_function(keyboard, choise_cab, call))

@dp.callback_query_handler(text='old_building_third')
async def callback_inline_nav_unifi_old_building_third(call: CallbackQuery):
    keyboard = await inline_keyboard_cabinets_third_old()
    await create_task(check_photo_map_nav_function(keyboard, choise_cab, call))

@dp.callback_query_handler(text='old_building_fourth')
async def callback_inline_nav_unifi_old_building_fourth(call: CallbackQuery):
    keyboard = await inline_keyboard_cabinets_fourth_old()
    await create_task(check_photo_map_nav_function(keyboard, choise_cab, call))

############## хэндлеры новое здание
@dp.callback_query_handler(text='new_building_first')
async def callback_inline_nav_unifi_new_building_first(call: CallbackQuery):
    keyboard = await inline_keyboard_cabinets_first_new()
    await create_task(check_photo_map_nav_function(keyboard, choise_cab, call))

@dp.callback_query_handler(text='new_building_second')
async def callback_inline_nav_unifi_new_building_second(call: CallbackQuery):
    keyboard = await inline_keyboard_cabinets_second_new()
    await create_task(check_photo_map_nav_function(keyboard, choise_cab, call))

@dp.callback_query_handler(text='new_building_third')
async def callback_inline_nav_unifi_new_building_third(call: CallbackQuery):
    keyboard = await inline_keyboard_cabinets_third_new()
    await create_task(check_photo_map_nav_function(keyboard, choise_cab, call))

@dp.callback_query_handler(text='new_building_fourth')
async def callback_inline_nav_unifi_new_building_fourth(call: CallbackQuery):
    keyboard = await inline_keyboard_cabinets_fourth_new()
    await create_task(check_photo_map_nav_function(keyboard, choise_cab, call))

@dp.callback_query_handler(text='new_building_fifth')
async def callback_inline_nav_unifi_new_building_fifth(call: CallbackQuery):
    keyboard = await inline_keyboard_cabinets_fifth_new()
    await create_task(check_photo_map_nav_function(keyboard, choise_cab, call))

@dp.callback_query_handler(text='new_building_sixth')
async def callback_inline_nav_unifi_new_building_sixth(call: CallbackQuery):
    keyboard = await inline_keyboard_cabinets_sixth_new()
    await create_task(check_photo_map_nav_function(keyboard, choise_cab, call))


# сделал очень тупую конструкцию для кнопки назад
@dp.callback_query_handler(cabinet_callback.filter())
async def callback_inline(call: CallbackQuery, callback_data: dict):
    logging.info(f'call = {call.data}')
    cabinet = callback_data.get('cabinet')
    description = await db.find_cabinet_description(cabinet)
    photo_id = await db.find_photoid_description(cabinet)
    id_cab = await db.find_id_cabinet(cabinet)
    floor = await db.find_floor_cabinet(id_cab)
    building = await db.find_building_cabinet(id_cab)
    if floor == '1 этаж' and building == 'Старое здание':
        building_callback = "old_"
        floor_callback = "_first"
        keyboard = inline_keyboard_old_building_back(building_callback, floor_callback)
        await create_task(check_photo_is_none_map_nav_function(keyboard, description, photo_id, call))
    elif floor == '2 этаж' and building == 'Старое здание':
        building_callback = "old_"
        floor_callback = "_second"
        keyboard = inline_keyboard_old_building_back(building_callback, floor_callback)
        await create_task(check_photo_is_none_map_nav_function(keyboard, description, photo_id, call))
    elif floor == '3 этаж' and building == 'Старое здание':
        building_callback = "old_"
        floor_callback = "_third"
        keyboard = inline_keyboard_old_building_back(building_callback, floor_callback)
        await create_task(check_photo_is_none_map_nav_function(keyboard, description, photo_id, call))
    elif floor == '4 этаж' and building == 'Старое здание':
        building_callback = "old_"
        floor_callback = "_fourth"
        keyboard = inline_keyboard_old_building_back(building_callback, floor_callback)
        await create_task(check_photo_is_none_map_nav_function(keyboard, description, photo_id, call))
    elif floor == '1 этаж' and building == 'Новое здание':
        building_callback = "new_"
        floor_callback = "_first"
        keyboard = inline_keyboard_old_building_back(building_callback, floor_callback)
        await create_task(check_photo_is_none_map_nav_function(keyboard, description, photo_id, call))
    elif floor == '2 этаж' and building == 'Новое здание':
        building_callback = "new_"
        floor_callback = "_second"
        keyboard = inline_keyboard_old_building_back(building_callback, floor_callback)
        await create_task(check_photo_is_none_map_nav_function(keyboard, description, photo_id, call))
    elif floor == '3 этаж' and building == 'Новое здание':
        building_callback = "new_"
        floor_callback = "_third"
        keyboard = inline_keyboard_old_building_back(building_callback, floor_callback)
        await create_task(check_photo_is_none_map_nav_function(keyboard, description, photo_id, call))
    elif floor == '4 этаж' and building == 'Новое здание':
        building_callback = "new_"
        floor_callback = "_fourth"
        keyboard = inline_keyboard_old_building_back(building_callback, floor_callback)
        await create_task(check_photo_is_none_map_nav_function(keyboard, description, photo_id, call))
    elif floor == '5 этаж' and building == 'Новое здание':
        building_callback = "new_"
        floor_callback = "_fifth"
        keyboard = inline_keyboard_old_building_back(building_callback, floor_callback)
        await create_task(check_photo_is_none_map_nav_function(keyboard, description, photo_id, call))
    elif floor == '6 этаж' and building == 'Новое здание':
        building_callback = "new_"
        floor_callback = "_sixth"
        keyboard = inline_keyboard_old_building_back(building_callback, floor_callback)
        await create_task(check_photo_is_none_map_nav_function(keyboard, description, photo_id, call))
    else:
        keyboard = inline_keyboard_new_building_back
        await create_task(check_photo_is_none_map_nav_function(keyboard, description, photo_id, call))
    await call.answer()
##########################  Навигация по университету КОНЕЦ #############################################
