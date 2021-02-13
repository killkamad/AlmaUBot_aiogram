import ast
import logging

from aiogram.types import CallbackQuery
from loader import dp, bot
from keyboards.inline.navigation_buttons import inline_keyboard_nav_unifi, inline_keyboard_contacts_center, \
    inline_keyboard_contacts_center_back, inline_keyboard_pps, inline_keyboard_pps_shcool_management, \
    inline_keyboard_pps_rectorat, inline_keyboard_pps_shcool_law, inline_keyboard_pps_shcool_inovation, \
    inline_keyboard_pps_shcool_economic, inline_keyboard_pps_shcool_engineer, inline_keyboard_pps_shcool_bussines, \
    inline_keyboard_pps_rectorat_back, inline_keyboard_pps_shcool_bussines_back, \
    inline_keyboard_pps_shcool_engineer_back, inline_keyboard_pps_shcool_economic_back, \
    inline_keyboard_pps_shcool_inovation_back, inline_keyboard_pps_shcool_law_back, \
    inline_keyboard_pps_shcool_management_back
from utils import db_api as db


@dp.callback_query_handler(text='/nav_unifi')
async def callback_inline_nav_unifi(call: CallbackQuery):
    logging.info(f"User({call.message.chat.id}) вошел в Навигацию")
    await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                text='Навигация по университету', reply_markup=inline_keyboard_nav_unifi())


@dp.callback_query_handler(text='contacts_center')
async def callback_inline_contacts_center(call: CallbackQuery):
    logging.info(f"User({call.message.chat.id}) вошел в Контакты ключевых центров")
    await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                text='Контакты ключевых центров', reply_markup=await inline_keyboard_contacts_center())


@dp.callback_query_handler(text_contains="['contacts_center_call'")
async def callback_inline_contacts_center_call(call: CallbackQuery):
    logging.info(f'call = {call.data}')
    valueFromCallBack = ast.literal_eval(call.data)[1]
    description = await db.contact_center_description(valueFromCallBack)
    await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                text=description, reply_markup=inline_keyboard_contacts_center_back())


@dp.callback_query_handler(text='tutors_university')
async def callback_inline_contacts_center(call: CallbackQuery):
    logging.info(f"User({call.message.chat.id}) вошел в Профессорско-преподавательский состав")
    await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                text='Профессорско-преподавательский состав, выберите школу', reply_markup = inline_keyboard_pps())


@dp.callback_query_handler(text='shcool_management')
async def callback_inline_contacts_center(call: CallbackQuery):
    logging.info(f"User({call.message.chat.id}) вошел в Школа менеджмента")
    await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                text='Школа менеджмента', reply_markup = inline_keyboard_pps_shcool_management())


@dp.callback_query_handler(text='shcool_law')
async def callback_inline_contacts_center(call: CallbackQuery):
    logging.info(f"User({call.message.chat.id}) вошел в Школа политики и права")
    await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                text='Школа политики и права', reply_markup = inline_keyboard_pps_shcool_law())


@dp.callback_query_handler(text='shcool_inovation')
async def callback_inline_contacts_center(call: CallbackQuery):
    logging.info(f"User({call.message.chat.id}) вошел в Школа предпринимательства и инноваций")
    await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                text='Школа предпринимательства и инноваций', reply_markup = inline_keyboard_pps_shcool_inovation())


@dp.callback_query_handler(text='shcool_economic')
async def callback_inline_contacts_center(call: CallbackQuery):
    logging.info(f"User({call.message.chat.id}) вошел в Школа Экономики и Финансов")
    await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                text='Школа Экономики и Финансов', reply_markup =inline_keyboard_pps_shcool_economic())


@dp.callback_query_handler(text='shcool_engineer')
async def callback_inline_contacts_center(call: CallbackQuery):
    logging.info(f"User({call.message.chat.id}) вошел в Школа Инженерного Менеджмента")
    await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                text='Школа Инженерного Менеджмента', reply_markup = inline_keyboard_pps_shcool_engineer())


@dp.callback_query_handler(text='shcool_bussines')
async def callback_inline_contacts_center(call: CallbackQuery):
    logging.info(f"User({call.message.chat.id}) вошел в Высшая школа бизнеса")
    await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                text='Высшая Школа Бизнеса', reply_markup = inline_keyboard_pps_shcool_bussines())


@dp.callback_query_handler(text='rectorat')
async def callback_inline_contacts_center(call: CallbackQuery):
    logging.info(f"User({call.message.chat.id}) вошел в Ректорат")
    await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                text='Ректорат', reply_markup = inline_keyboard_pps_rectorat())


#######
@dp.callback_query_handler(text='dekan_shcool_management')
async def callback_inline_contacts_center(call: CallbackQuery):
    logging.info(f"User({call.message.chat.id}) вошел в Школа менеджмента")
    shcool = 'Школа менеджмента'
    position = 'Декан'
    description = await db.pps_center_description(shcool, position)
    await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                text=description, reply_markup = inline_keyboard_pps_shcool_management_back())


@dp.callback_query_handler(text='dekan_shcool_law')
async def callback_inline_contacts_center(call: CallbackQuery):
    logging.info(f"User({call.message.chat.id}) вошел в Школа политики и права")
    shcool = 'Школа политики и права'
    position = 'Декан'
    description = await db.pps_center_description(shcool, position)
    await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                text=description, reply_markup = inline_keyboard_pps_shcool_law_back())


@dp.callback_query_handler(text='dekan_shcool_inovation')
async def callback_inline_contacts_center(call: CallbackQuery):
    logging.info(f"User({call.message.chat.id}) вошел в Школа предпринимательства и инноваций")
    shcool = 'Школа предпринимательства и инноваций'
    position = 'Декан'
    description = await db.pps_center_description(shcool, position)
    await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                text=description, reply_markup = inline_keyboard_pps_shcool_inovation_back())


@dp.callback_query_handler(text='dekan_shcool_economic')
async def callback_inline_contacts_center(call: CallbackQuery):
    logging.info(f"User({call.message.chat.id}) вошел в Школа Экономики и Финансов")
    shcool = 'Школа Экономики и Финансов'
    position = 'Декан'
    description = await db.pps_center_description(shcool, position)
    await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                text=description, reply_markup =inline_keyboard_pps_shcool_economic_back())


@dp.callback_query_handler(text='dekan_shcool_engineer')
async def callback_inline_contacts_center(call: CallbackQuery):
    logging.info(f"User({call.message.chat.id}) вошел в Школа Инженерного Менеджмента")
    shcool = 'Школа Инженерного Менеджмента'
    position = 'Декан'
    description = await db.pps_center_description(shcool, position)
    await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                text=description, reply_markup = inline_keyboard_pps_shcool_engineer_back())


@dp.callback_query_handler(text='dekan_shcool_bussines')
async def callback_inline_contacts_center(call: CallbackQuery):
    logging.info(f"User({call.message.chat.id}) вошел в Высшая школа бизнеса")
    shcool = 'Высшая Школа Бизнеса'
    position = 'Декан'
    description = await db.pps_center_description(shcool, position)
    await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                text=description, reply_markup = inline_keyboard_pps_shcool_bussines_back())


@dp.callback_query_handler(text='rectorat_rector')
async def callback_inline_contacts_center(call: CallbackQuery):
    logging.info(f"User({call.message.chat.id}) вошел в Ректорат")
    shcool = 'Ректорат'
    position = 'Ректор'
    description = await db.pps_center_description(shcool, position)
    await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                text=description, reply_markup = inline_keyboard_pps_rectorat_back())


########################
@dp.callback_query_handler(text='tutors_shcool_management')
async def callback_inline_contacts_center(call: CallbackQuery):
    logging.info(f"User({call.message.chat.id}) вошел в tutors Школа менеджмента")
    shcool = 'Школа менеджмента'
    position = 'Преподаватели'
    description = await db.pps_center_description(shcool, position)
    await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                text=description, reply_markup = inline_keyboard_pps_shcool_management_back())


@dp.callback_query_handler(text='tutors_shcool_law')
async def callback_inline_contacts_center(call: CallbackQuery):
    logging.info(f"User({call.message.chat.id}) вошел в tutors Школа политики и права")
    shcool = 'Школа политики и права'
    position = 'Преподаватели'
    description = await db.pps_center_description(shcool, position)
    await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                text=description, reply_markup = inline_keyboard_pps_shcool_law_back())


@dp.callback_query_handler(text='tutors_shcool_inovation')
async def callback_inline_contacts_center(call: CallbackQuery):
    logging.info(f"User({call.message.chat.id}) вошел в tutors Школа предпринимательства и инноваций")
    shcool = 'Школа предпринимательства и инноваций'
    position = 'Преподаватели'
    description = await db.pps_center_description(shcool, position)
    await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                text=description, reply_markup = inline_keyboard_pps_shcool_inovation_back())


@dp.callback_query_handler(text='tutors_shcool_economic')
async def callback_inline_contacts_center(call: CallbackQuery):
    logging.info(f"User({call.message.chat.id}) вошел в tutors Школа Экономики и Финансов")
    shcool = 'Школа Экономики и Финансов'
    position = 'Преподаватели'
    description = await db.pps_center_description(shcool, position)
    await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                text=description, reply_markup =inline_keyboard_pps_shcool_economic_back())


@dp.callback_query_handler(text='tutors_shcool_engineer')
async def callback_inline_contacts_center(call: CallbackQuery):
    logging.info(f"User({call.message.chat.id}) вошел в tutors Школа Инженерного Менеджмента")
    shcool = 'Школа Инженерного Менеджмента'
    position = 'Преподаватели'
    description = await db.pps_center_description(shcool, position)
    await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                text=description, reply_markup = inline_keyboard_pps_shcool_engineer_back())


@dp.callback_query_handler(text='tutors_shcool_bussines')
async def callback_inline_contacts_center(call: CallbackQuery):
    logging.info(f"User({call.message.chat.id}) вошел в tutors Высшая школа бизнеса")
    shcool = 'Высшая Школа Бизнеса'
    position = 'Преподаватели'
    description = await db.pps_center_description(shcool, position)
    await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                text=description, reply_markup = inline_keyboard_pps_shcool_bussines_back())


@dp.callback_query_handler(text='rectorat_humans')
async def callback_inline_contacts_center(call: CallbackQuery):
    logging.info(f"User({call.message.chat.id}) вошел в humans Ректорат")
    shcool = 'Ректорат'
    position = 'Проректоры'
    description = await db.pps_center_description(shcool, position)
    await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                text=description, reply_markup = inline_keyboard_pps_rectorat_back())

