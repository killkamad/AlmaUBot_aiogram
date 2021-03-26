import logging

from aiogram import types
from aiogram.types import CallbackQuery, ContentType
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
    keyboard_pps_choice_position, keyboard_pps_choice_position_rector, keyboard_pps_choice_shcool, \
    inline_keyboard_cancel_tutors_admin, cancel_or_send_or_image_map_nav_admin, cancel_or_update_or_image_map_nav_admin, \
    cancel_or_description_or_image_map_nav_admin, cancel_or_description_or_send_map_nav_admin, \
    inline_keyboard_description_image_tutors_admin, \
    cancel_or_description_or_send_tutors_admin, cancel_or_update_or_image_tutors_admin, cancel_or_delete_photo_pps_admin

import asyncio

from utils import db_api as db
from utils.delete_inline_buttons import delete_inline_buttons_in_dialogue
from aiogram.dispatcher import FSMContext
from states.admin import SendContactCenter, UpdateContactCenter, DeleteContactCenter, PpsAdmin, MapNavigation, \
    MapNavigationUpdate, MapNavigationDelete

from keyboards.inline import cabinet_callback_update, nav_center_callback_update, \
    nav_center_callback_delete


@dp.callback_query_handler(text_contains='nav_university_admin_menu', state=['*'])
async def callback_inline_nav_university_admin_menu(call: CallbackQuery, state: FSMContext):
    logging.info(f'User({call.message.chat.id}) вошел в админ меню Навигации, call.data - {call.data}')
    await state.reset_state()
    await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                text='Админ меню Навигации:', reply_markup=inline_keyboard_nav_university_admin_menu())
    await call.answer()


@dp.callback_query_handler(text_contains='contacts_center_admin')
async def callback_inline_contacts_center_admin(call: CallbackQuery):
    logging.info(f'User({call.message.chat.id}) вошел в админ меню Навигации, call.data - {call.data}')
    await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                text='Админ меню ключевых центров:',
                                reply_markup=inline_keyboard_contact_center_admin())
    await call.answer()


#### Создания контакт центра ####
@dp.callback_query_handler(text='send_contact_center_admin', state=None)
async def callback_inline_send_contact_center_admin(call: CallbackQuery):
    logging.info(f'User({call.message.chat.id}) нажал на кнопку {call.data}')
    await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                text='Напишите название ключевого центра, например (бухгалтерия)',
                                reply_markup=inline_keyboard_cancel_contact_center_admin())
    await SendContactCenter.name.set()
    await call.answer()


@dp.callback_query_handler(text='cancel_step_contact_center_admin', state=['*'])
async def callback_inline_cancel_step(call: CallbackQuery, state: FSMContext):
    logging.info(f'User({call.message.chat.id}) нажал на кнопку {call.data}')
    await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                text='Админ меню ключевых центров',
                                reply_markup=inline_keyboard_contact_center_admin())
    await state.reset_state()
    await call.answer()


# Проверка центра на текст
@dp.message_handler(content_types=ContentType.ANY, state=SendContactCenter.name)
async def message_send_contact_center_name(message: types.Message, state: FSMContext):
    await delete_inline_buttons_in_dialogue(message)
    if message.content_type == 'text' and len(message.text) <= 64:
        await state.update_data(name=message.text,
                                user_id=message.chat.id)
        data = await state.get_data()
        await bot.send_message(message.chat.id, text=f'<b>Название центра:</b> {data["name"]} \n'
                                                     f'Отправьте описание ключевого центра', parse_mode='HTML',
                               reply_markup=inline_keyboard_cancel_contact_center_admin())
        await SendContactCenter.description.set()
    else:
        print(message.content_type)
        await bot.send_message(message.chat.id,
                               'Ошибка - ваше сообщение должно содержать только текст и не превышать 64 символов.\n'
                               'Повторите название для кнопки, например (бухгалтерия):',
                               reply_markup=inline_keyboard_cancel_contact_center_admin())


# Проверка описания центра на текст
@dp.message_handler(content_types=ContentType.ANY, state=SendContactCenter.description)
async def message_send_contact_center_description(message: types.Message, state: FSMContext):
    await delete_inline_buttons_in_dialogue(message)
    if message.content_type == 'text':
        if len(message.text) <= 4000:
            await state.update_data(description=message.text)
            data = await state.get_data()
            await bot.send_message(message.chat.id, text=f'<b>Данные:</b>\n'
                                                         f'<b>• Название центра:</b> {data["name"]} \n'
                                                         f'<b>• Описание:</b> {data["description"]}', parse_mode='HTML',
                                   reply_markup=cancel_or_send_contact_center_admin())
            await state.reset_state(with_data=False)
        else:
            await bot.send_message(message.chat.id,
                                   'Ошибка - ваше сообщение должно содержать только текст и не превышать 4000 символов.\n'
                                   'Попробуйте заново отправить описание:',
                                   reply_markup=inline_keyboard_cancel_contact_center_admin())
    else:
        await message.answer('Ошибка - вы отправили не текст повторите',
                             reply_markup=inline_keyboard_cancel_contact_center_admin())


# создание контакт центра в базе данных
@dp.callback_query_handler(text='send_contact_center', state=None)
async def callback_inline_send_contact_center_final(call: CallbackQuery, state: FSMContext):
    try:
        data = await state.get_data()
        await db.add_contact_center_data(data['user_id'], data['description'], data["name"])
        logging.info(f'User({call.message.chat.id}) отправил контакты для {data["name"]}')
        await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                    text=f'✅ Описание центра <b>{data["name"]}</b> успешно отправлено. \n'
                                         'Админ меню ключевых центров:', parse_mode='HTML',
                                    reply_markup=inline_keyboard_contact_center_admin())
        await call.answer()
    except Exception as e:
        await call.message.answer(f'Ошибка контакт центр не отправлен, (Ошибка - {e})')
        print(e)


#### Обновление контакт центра ####
@dp.callback_query_handler(text='update_contact_center_admin', state=None)
async def callback_inline_update_schedule_bot(call: CallbackQuery):
    logging.info(f'User({call.message.chat.id}) нажал на кнопку {call.data}')
    await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                text='Выберите центр для изменения информации',
                                reply_markup=await inline_keyboard_contacts_center_update())
    await UpdateContactCenter.name.set()
    await call.answer()


@dp.callback_query_handler(nav_center_callback_update.filter(), state=UpdateContactCenter.name)
async def callback_inline_updade_contact_center(call: CallbackQuery, state: FSMContext, callback_data: dict):
    logging.info(f'User({call.message.chat.id}) нажал на кнопку {call.data}')
    callback_id = callback_data.get('id')
    center_name = await db.search_contact_center_name(callback_id)
    old_description = await db.description_contact_center_name(callback_id)
    await state.update_data(name=center_name, user_id=call.message.chat.id)
    await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                text=f"<b>Актуальная информация центра</b>: \n {old_description} \n"
                                     f"<b>Напишете новую информацию для центра: <i>{center_name}</i></b>",
                                parse_mode='HTML', reply_markup=inline_keyboard_cancel_contact_center_admin())
    await UpdateContactCenter.description.set()
    await call.answer()


@dp.message_handler(content_types=ContentType.ANY, state=UpdateContactCenter.description)
async def update_contact_center_step(message: types.Message, state: FSMContext):
    await delete_inline_buttons_in_dialogue(message)
    await UpdateContactCenter.description.set()
    if message.content_type == 'text':
        await state.update_data(description=message.text)
        data = await state.get_data()
        await bot.send_message(message.chat.id, text=f'<b>Данные:</b>\n'
                                                     f'• <b>Название центра:</b> {data["name"]} \n'
                                                     f'• <b>Описание:</b> {data["description"]}', parse_mode='HTML',
                               reply_markup=cancel_or_update_contact_center_admin())
        await state.reset_state(with_data=False)
    else:
        await message.answer('Ошибка - вы отправили не текст повторите',
                             reply_markup=inline_keyboard_cancel_contact_center_admin())


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
                                    text=f'✅ Описание <b>{data["name"]}</b> успешно обновлено. \n'
                                         'Админ меню ключевых центров:',
                                    parse_mode='HTML', reply_markup=inline_keyboard_contact_center_admin())
        logging.info(f'User({call.message.chat.id}) обновил описание для {data["name"]}')
        await call.answer()
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
    await call.answer()


@dp.callback_query_handler(nav_center_callback_delete.filter(), state=DeleteContactCenter.name)
async def callback_inline_update_contact_center(call: CallbackQuery, state: FSMContext, callback_data: dict):
    logging.info(f'User({call.message.chat.id}) нажал на кнопку {call.data}')
    callback_id = callback_data.get('id')
    center_name = await db.search_contact_center_name(callback_id)
    await state.update_data(name=center_name, user_id=call.message.chat.id)
    await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                text=f'Вы точно уверены, что хотите удалить информацию: <b>{center_name}</b>',
                                parse_mode='HTML', reply_markup=cancel_or_delete_contact_center_admin())
    await DeleteContactCenter.confirm_delete.set()
    await call.answer()


@dp.callback_query_handler(text='delete_info_contact_center_admin', state=DeleteContactCenter.confirm_delete)
async def callback_inline_delete_info_contact_center_admin(call: CallbackQuery, state: FSMContext):
    try:
        data = await state.get_data()
        await db.delete_contact_center_button(data["name"])
        await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                    text=f'✅ Ключевой центр <b>{data["name"]}</b> успешно удален из базы данных. \n'
                                         f'Админ меню ключевых центров:', parse_mode='HTML',
                                    reply_markup=inline_keyboard_contact_center_admin())
        await state.reset_state()
        logging.info(f'User({call.message.chat.id}) удалил ключевой центр для {data["name"]}')
        await call.answer()
    except Exception as e:
        try:
            await bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id)
        except:
            pass
        await call.message.answer(f'(Ошибка - {e})')
        logging.info(f'Ошибка - {e}')


###################################  профессорско преподвательский состав изменение информации#################################
@dp.callback_query_handler(text='tutors_university_admin', state=None)
async def callback_tutors_university_admin_state(call: CallbackQuery):
    await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                text=f'Выберите школу для которой хотите ввести изменения',
                                reply_markup=keyboard_pps_choice_shcool())
    await PpsAdmin.school.set()
    await call.answer()


@dp.callback_query_handler(lambda shcool: shcool.data and shcool.data.startswith('choice_shcool_admin'),
                           state=PpsAdmin.school)
async def pps_admin_state_shcool(call: CallbackQuery, state: FSMContext):
    school_number = call.data[-1]
    if school_number == '1':
        async with state.proxy() as data:
            data['shcool'] = "Школа менеджмента"
    if school_number == '2':
        async with state.proxy() as data:
            data['shcool'] = "Школа политики и права"
    if school_number == '3':
        async with state.proxy() as data:
            data['shcool'] = "Школа Инженерного Менеджмента"
    if school_number == '4':
        async with state.proxy() as data:
            data['shcool'] = "Школа предпринимательства и инноваций"
    if school_number == '5':
        async with state.proxy() as data:
            data['shcool'] = "Высшая Школа Бизнеса"
    if school_number == '6':
        async with state.proxy() as data:
            data['shcool'] = "Школа Экономики и Финансов"
    await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                text=f'Выбирете что хотите изменить',
                                reply_markup=keyboard_pps_choice_position())
    await PpsAdmin.position.set()
    await call.answer()


@dp.callback_query_handler(text='choice_rectorat_admin', state=PpsAdmin.school)
async def callback_choice_rectorat_admin_admin_state(call: CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        data['shcool'] = 'Ректорат'
    await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                text=f'Выбирете что хотите изменить',
                                reply_markup=keyboard_pps_choice_position_rector())
    await PpsAdmin.position.set()
    await call.answer()


@dp.callback_query_handler(lambda shcool: shcool.data and shcool.data.startswith('choice_position_admin'),
                           state=PpsAdmin.position)
async def pps_admin_state_position(call: CallbackQuery, state: FSMContext):
    position_number = call.data[-1]
    if position_number == '1':
        async with state.proxy() as data:
            data['position'] = "Декан"
    if position_number == '2':
        async with state.proxy() as data:
            data['position'] = "Преподаватели"
    if position_number == '3':
        async with state.proxy() as data:
            data['position'] = "Ректор"
    if position_number == '4':
        async with state.proxy() as data:
            data['position'] = "Проректоры"
    await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                text=f"<b>Выберите что хотите изменить для:</b> \n"
                                     f"<b>• Позиция:</b> {data['position']} \n"
                                     f"<b>• Подразделение:</b> {data['shcool']} \n",
                                parse_mode='HTML', reply_markup=inline_keyboard_description_image_tutors_admin())
    # await PpsAdmin.description.set()
    await state.reset_state(with_data=False)
    await call.answer()


@dp.callback_query_handler(text='update_pps_description_state', state=None)
async def pps_admin_state_cabinet_update_description(call: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                text=f'<b>Напишите изменение информации для:</b>\n'
                                     f"<b>• Позиция:</b> {data['position']} \n"
                                     f"<b>• Подразделение:</b> {data['shcool']} \n",
                                parse_mode='HTML', reply_markup=inline_keyboard_cancel_tutors_admin())
    await PpsAdmin.description.set()
    await call.answer()


@dp.callback_query_handler(text='update_image_pps_admin', state=None)
async def pps_admin_image_send_message(call: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                text=f'<b>Отправьте фото для:</b>\n'
                                     f"<b>• Позиция:</b> {data['position']} \n"
                                     f"<b>• Подразделение:</b> {data['shcool']} \n",
                                parse_mode='HTML',
                                reply_markup=inline_keyboard_cancel_tutors_admin())
    await PpsAdmin.image.set()
    await call.answer()


@dp.message_handler(content_types=ContentType.ANY, state=PpsAdmin.image)
async def pps_admin_state_image(message: types.Message, state: FSMContext):
    await delete_inline_buttons_in_dialogue(message)
    if message.content_type == 'photo':
        data = await state.get_data()
        await state.update_data(user_id=message.chat.id)
        async with state.proxy() as data:
            data['image'] = message.photo[-1].file_id
        if len(data) > 4:
            await state.update_data(image=message.photo[-1].file_id)
            await bot.send_message(message.chat.id, text=f"<b>Фото прикреплено!</b>\n"
                                                         f"<b>• Позиция:</b> {data['position']} \n"
                                                         f"<b>• Подразделение:</b> {data['shcool']} \n"
                                                         f"<b>Отправить изменения?</b>",
                                   parse_mode='HTML',
                                   reply_markup=cancel_or_send_tutors_management())
            await state.reset_state(with_data=False)
        else:
            await state.update_data(image=message.photo[-1].file_id)
            await bot.send_message(message.chat.id, text=f"<b>Фото прикреплено!</b>\n"
                                                         f"<b>• Позиция:</b> {data['position']} \n"
                                                         f"<b>• Подразделение:</b> {data['shcool']} \n"
                                                         f"<b>Изменить описание?</b>",
                                   parse_mode='HTML',
                                   reply_markup=cancel_or_description_or_send_tutors_admin())
            await state.reset_state(with_data=False)
    else:
        await message.answer('Ошибка - вы отправили не фото повторите',
                             reply_markup=inline_keyboard_cancel_map_nav_admin())


@dp.message_handler(content_types=ContentType.ANY, state=PpsAdmin.description)
async def message_send_tutors_management(message: types.Message, state: FSMContext):
    await delete_inline_buttons_in_dialogue(message)
    if message.content_type == 'text':
        await state.update_data(description=message.text, user_id=message.chat.id)
        data = await state.get_data()
        await state.update_data(user_id=message.chat.id)
        if len(data) > 4:
            await bot.send_message(message.chat.id, text=f'<b>Данные:</b>\n'
                                                         f"<b>• Описание:</b> {data['description']} \n"
                                                         f"<b>• Позиция:</b> {data['position']} \n"
                                                         f"<b>• Подразделение:</b> {data['shcool']} \n"
                                                         f"<b>Отправить изменения?</b>",
                                   parse_mode='HTML',
                                   reply_markup=cancel_or_send_tutors_management())
            await state.reset_state(with_data=False)
        else:
            await bot.send_message(message.chat.id, text=f'<b>Данные:</b>\n'
                                                         f"<b>• Описание:</b> {data['description']} \n"
                                                         f"<b>• Позиция:</b> {data['position']} \n"
                                                         f"<b>• Подразделение:</b> {data['shcool']} \n"
                                                         f'<b>Прикрепить или изменить фото?</b>',
                                   parse_mode='HTML',
                                   reply_markup=cancel_or_update_or_image_tutors_admin())
            await state.reset_state(with_data=False)
    else:
        await message.answer('Ошибка - вы отправили не текст повторите',
                             reply_markup=inline_keyboard_cancel_contact_center_admin())


@dp.callback_query_handler(text='send_tutors_management', state=None)
async def callback_inline_send_tutors_management_final_description_and_photo(call: CallbackQuery, state: FSMContext):
    try:
        data = await state.get_data()
        await db.add_pps_data(data['user_id'], data['shcool'], data['position'], data['description'], data['image'])
        await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                    text=f'✅ Информация для <b>{data["position"]}</b> '
                                         f'<b>{data["shcool"]}</b> успешно отправлено.\n'
                                         f'Админ меню навигации', parse_mode='HTML',
                                    reply_markup=inline_keyboard_nav_university_admin_menu())
        logging.info(f'User({call.message.chat.id}) отправил информацию для преподавателей менеджмента')
        await call.answer()
    except Exception as e:
        await call.message.answer(f'Ошибка описание не отправлено, (Ошибка - {e})')
        print(e)


@dp.callback_query_handler(text='send_tutors_management_description', state=None)
async def callback_inline_send_tutors_management_final_description(call: CallbackQuery, state: FSMContext):
    try:
        data = await state.get_data()
        await db.add_pps_data_description(data['user_id'], data['shcool'], data['position'], data['description'])
        await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                    text=f'✅ Описание для <b>{data["position"]}</b> '
                                         f'<b>{data["shcool"]}</b> успешно отправлено.\n'
                                         f'Админ меню навигации', parse_mode='HTML',
                                    reply_markup=inline_keyboard_nav_university_admin_menu())
        logging.info(f'User({call.message.chat.id}) отправил информацию для преподавателей менеджмента')
        await state.reset_state()
        await call.answer()
    except Exception as e:
        await call.message.answer(f'Ошибка описание не отправлено, (Ошибка - {e})')
        print(e)


@dp.callback_query_handler(text='send_tutors_management_photo', state=None)
async def callback_inline_send_tutors_management_final_photo(call: CallbackQuery, state: FSMContext):
    try:
        data = await state.get_data()
        await db.add_pps_data_photo(data['user_id'], data['shcool'], data['position'], data['image'])
        await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                    text=f'✅ Фото для <b>{data["position"]}</b> '
                                         f'<b>{data["shcool"]}</b> успешно отправлено.\n'
                                         f'Админ меню навигации', parse_mode='HTML',
                                    reply_markup=inline_keyboard_nav_university_admin_menu())
        logging.info(f'User({call.message.chat.id}) отправил информацию для преподавателей менеджмента')
        await state.reset_state()
        await call.answer()
    except Exception as e:
        await call.message.answer(f'Ошибка описание не отправлено, (Ошибка - {e})')
        print(e)


# Удаление фото с ппс
@dp.callback_query_handler(text='delete_pps_photo_state', state=None)
async def pps_admin_state_cabinet_delete_photo(call: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                text=f'<b>Удалить фото для: </b>\n'
                                     f"<b>• Позиция:</b> {data['position']} \n"
                                     f"<b>• Подразделение:</b> {data['shcool']} \n", parse_mode='HTML',
                                reply_markup=cancel_or_delete_photo_pps_admin())
    await PpsAdmin.image.set()
    await call.answer()


@dp.callback_query_handler(text='delete_tutors_management_photo', state=PpsAdmin.image)
async def callback_inline_delete_tutors_management_final_photo(call: CallbackQuery, state: FSMContext):
    try:
        async with state.proxy() as data:
            data['image'] = None
            data['user_id'] = call.message.chat.id
        data = await state.get_data()
        await db.add_pps_data_photo(data['user_id'], data['shcool'], data['position'], data['image'])
        await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                    text=f'✅ Фото для <b>{data["position"]}</b> '
                                         f'<b>{data["shcool"]}</b> успешно удалено.\n'
                                         f'Админ меню навигации', parse_mode='HTML',
                                    reply_markup=inline_keyboard_nav_university_admin_menu())
        logging.info(f'User({call.message.chat.id}) отправил информацию для преподавателей менеджмента')
        await state.reset_state()
        await call.answer()
    except Exception as e:
        await call.message.answer(f'Ошибка описание не отправлено, (Ошибка - {e})')
        print(e)


@dp.callback_query_handler(text='cancel_step_tutors_admin', state=['*'])
async def callback_inline_cancel_step_tutors(call: CallbackQuery, state: FSMContext):
    logging.info(f'User({call.message.chat.id}) нажал на кнопку {call.data}')
    # await bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id)
    await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                text=f'Выберите школу для которой хотите ввести изменения',
                                reply_markup=keyboard_pps_choice_shcool())
    await state.reset_state()
    await PpsAdmin.school.set()
    await call.answer()


#############  админ меню карты навигации
@dp.callback_query_handler(text_contains='map_nav_admin')
async def callback_inline_map_nav_admin_admin(call: CallbackQuery):
    logging.info(f'User({call.message.chat.id}) вошел в админ карты-навигации, call.data - {call.data}')
    await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                text='Админ меню карты-навигации:', reply_markup=inline_keyboard_map_nav_admin_menu())
    await call.answer()


@dp.callback_query_handler(text='send_cabinet_admin', state=None)
async def callback_map_nav_send_cabinet_admin_state(call: CallbackQuery):
    await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                text='Выберите здание где хотите добавить кабинет',
                                reply_markup=keyboard_map_nav_choice_building())
    await MapNavigation.building.set()
    await call.answer()


@dp.callback_query_handler(text='new_building_choice_admin', state=MapNavigation.building)
async def map_nav_admin_state_building1(call: CallbackQuery, state: FSMContext):
    building_data = 'Новое здание'
    async with state.proxy() as data:
        data['building'] = building_data
    await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                text='Выберите этаж в каком хотите добавить кабинет',
                                reply_markup=map_nav_admin_choice_floor_new())
    await MapNavigation.floor.set()
    await call.answer()


@dp.callback_query_handler(text='old_building_choice_admin', state=MapNavigation.building)
async def map_nav_admin_state_building2(call: CallbackQuery, state: FSMContext):
    building_data = 'Старое здание'
    async with state.proxy() as data:
        data['building'] = building_data
    await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                text='Выберите этаж в каком хотите добавить кабинет',
                                reply_markup=map_nav_admin_choice_floor_old())
    await MapNavigation.floor.set()
    await call.answer()


@dp.callback_query_handler(lambda floor: floor.data and floor.data.startswith('floor_choice_admin'),
                           state=MapNavigation.floor)
async def map_nav_admin_state_floor(call: CallbackQuery, state: FSMContext):
    floor_number = call.data[-1]
    if floor_number == '1':
        async with state.proxy() as data:
            data['floor'] = "1 этаж"
    if floor_number == '2':
        async with state.proxy() as data:
            data['floor'] = "2 этаж"
    if floor_number == '3':
        async with state.proxy() as data:
            data['floor'] = "3 этаж"
    if floor_number == '4':
        async with state.proxy() as data:
            data['floor'] = "4 этаж"
    if floor_number == '5':
        async with state.proxy() as data:
            data['floor'] = "5 этаж"
    if floor_number == '6':
        async with state.proxy() as data:
            data['floor'] = "6 этаж"
    # print(data['floor'])
    await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                text=f"<b>Напишите название(например:101 кабинет) которое хотите добавить для:</b>\n"
                                     f"<b>• Здание:</b> {data['building']}\n"
                                     f"<b>• Этаж:</b> {data['floor']}\n",
                                parse_mode='HTML',
                                reply_markup=inline_keyboard_cancel_map_nav_admin())
    await MapNavigation.cabinet.set()
    await call.answer()


@dp.message_handler(content_types=ContentType.ANY, state=MapNavigation.cabinet)
async def map_nav_admin_state_cabinet(message: types.Message, state: FSMContext):
    await delete_inline_buttons_in_dialogue(message)
    try:
        data = await state.get_data()
        cabinets = await db.select_cabinet_admin_check()
        check_cabinet = True
        for item in cabinets:
            if item['cabinet'] == message.text:
                check_cabinet = False
            else:
                continue
        if (message.content_type == 'text') and (check_cabinet is True):
            if len(message.text) <= 28:
                async with state.proxy() as data:
                    data['cabinet'] = message.text
                await message.reply(f"<b>Напишите описание для:</b>\n"
                                    f"<b>• Кабинет:</b> {data['cabinet']}\n"
                                    f"<b>• Здание:</b> {data['building']}\n"
                                    f"<b>• Этаж:</b> {data['floor']}\n",
                                    parse_mode='HTML',
                                    reply_markup=inline_keyboard_cancel_map_nav_admin())
                await MapNavigation.description.set()
            else:
                await message.answer(f'Ваше сообщение содержит {len(message.text)}, максимально допустимое значание 28',
                                     reply_markup=inline_keyboard_cancel_map_nav_admin())
        else:
            await message.answer('Ошибка - вы отправили не текст или название кабинета уже существует повторите',
                                 reply_markup=inline_keyboard_cancel_map_nav_admin())
    except Exception as e:
        await message.answer(f'Ошибка  (Ошибка - {e})')
        print(e)


@dp.message_handler(content_types=ContentType.ANY, state=MapNavigation.description)
async def map_nav_admin_state_description(message: types.Message, state: FSMContext):
    await delete_inline_buttons_in_dialogue(message)
    if message.content_type == 'text':
        await state.update_data(description=message.text, user_id=message.chat.id)
        data = await state.get_data()
        await bot.send_message(message.chat.id, text=f"<b>Данные:</b>\n"
                                                     f"<b>• Кабинет:</b> {data['cabinet']}\n"
                                                     f"<b>• Здание:</b> {data['building']}\n"
                                                     f"<b>• Этаж:</b> {data['floor']}\n"
                                                     f"<b>• Описание:</b> {data['description']}\n"
                                                     f"<b>Прикрепить фото?</b>", parse_mode='HTML',
                               reply_markup=cancel_or_send_or_image_map_nav_admin())
        await state.reset_state(with_data=False)
    else:
        await message.answer('Ошибка - вы отправили не текст повторите',
                             reply_markup=inline_keyboard_cancel_map_nav_admin())


@dp.callback_query_handler(text='send_image_navigation_admin', state=None)
async def map_nav_admin_image_send(call: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                text=f'<b>Отправьте фото для:</b>\n'
                                     f"<b>• Кабинет:</b> {data['cabinet']}\n"
                                     f"<b>• Здание:</b> {data['building']}\n"
                                     f"<b>• Этаж:</b> {data['floor']}\n",
                                parse_mode='HTML',
                                reply_markup=inline_keyboard_cancel_map_nav_admin())
    await MapNavigation.image.set()
    await call.answer()


@dp.message_handler(content_types=ContentType.ANY, state=MapNavigation.image)
async def map_nav_admin_state_image(message: types.Message, state: FSMContext):
    await delete_inline_buttons_in_dialogue(message)
    if message.content_type == 'photo':
        data = await state.get_data()
        await state.update_data(image=message.photo[-1].file_id)
        await bot.send_message(message.chat.id, text=f"Фото прикреплено!\n"
                                                     f"<b>Данные:</b>\n"
                                                     f"<b>• Кабинет:</b> {data['cabinet']}\n"
                                                     f"<b>• Здание:</b> {data['building']}\n"
                                                     f"<b>• Этаж:</b> {data['floor']}\n"
                                                     f"<b>• Описание:</b> {data['description']}\n",
                               parse_mode='HTML',
                               reply_markup=cancel_or_send_map_nav_admin())
        await state.reset_state(with_data=False)
    else:
        await message.answer('Ошибка - вы отправили не фото повторите',
                             reply_markup=inline_keyboard_cancel_map_nav_admin())


@dp.callback_query_handler(text='send_map_navigation_admin', state=None)
async def map_nav_admin_state_send_final(call: CallbackQuery, state: FSMContext):
    try:
        data = await state.get_data()
        if len(data) > 5:
            await db.add_map_navigation_data(data['user_id'], data['building'], data['floor'], data['cabinet'],
                                             data['description'], data['image'])
            await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                        text=f"✅ Помещение <b>{data['cabinet']}</b> для:\n"
                                             f"<b>{data['building']}</b> <b>{data['floor']}</b> успешно отправлено.\n"
                                             "Админ меню карт-навигации",
                                        parse_mode='HTML',
                                        reply_markup=inline_keyboard_map_nav_admin_menu())
            await state.reset_state()
        else:
            async with state.proxy() as data:
                data['image'] = None
            await db.add_map_navigation_data(data['user_id'], data['building'], data['floor'], data['cabinet'],
                                             data['description'], data['image'])
            await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                        text=f"✅ Помещение <b>{data['cabinet']}</b> для:\n"
                                             f"<b>{data['building']}</b> <b>{data['floor']}</b> успешно отправлено.\n"
                                             "Админ меню карт-навигации",
                                        parse_mode='HTML',
                                        reply_markup=inline_keyboard_map_nav_admin_menu())
            await state.reset_state()
        logging.info(f'User({call.message.chat.id}) отправил информацию для кабинета')
        await call.answer()
    except Exception as e:
        await call.message.answer(f'Ошибка описание не отправлено, (Ошибка - {e})')
        print(e)


########################################  Обновление Кабинетов   ###############################################


@dp.callback_query_handler(text='update_cabinet_admin', state=None)
async def callback_map_nav_admin_state_update(call: CallbackQuery):
    await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                text='Выберите здание где хотите обновить кабинет',
                                reply_markup=keyboard_map_nav_choice_building_update())
    await MapNavigationUpdate.building.set()
    await call.answer()


@dp.callback_query_handler(text='new_building_choice_admin_update', state=MapNavigationUpdate.building)
async def map_nav_admin_state_building_update(call: CallbackQuery, state: FSMContext):
    data_building = 'Новое здание'
    async with state.proxy() as data:
        data['building'] = data_building
    await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                text='Выберите этаж в каком хотите изменить описание кабинет',
                                reply_markup=map_nav_admin_choice_floor_new_update())
    await MapNavigationUpdate.floor.set()
    await call.answer()


@dp.callback_query_handler(text='old_building_choice_admin_update', state=MapNavigationUpdate.building)
async def map_nav_admin_state_old_building_choice_admin_update(call: CallbackQuery, state: FSMContext):
    data_building = 'Старое здание'
    async with state.proxy() as data:
        data['building'] = data_building
    # print(data['building'])
    await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                text='Выберите этаж в каком хотите изменить описание кабинет',
                                reply_markup=map_nav_admin_choice_floor_old_update())
    await MapNavigationUpdate.floor.set()
    await call.answer()


@dp.callback_query_handler(lambda floor: floor.data and floor.data.startswith('floor_choice_admin_update'),
                           state=MapNavigationUpdate.floor)
async def map_nav_admin_state_floor_update(call: CallbackQuery, state: FSMContext):
    floor_number = call.data[-1]
    if floor_number == '1':
        async with state.proxy() as data:
            data['floor'] = "1 этаж"
    if floor_number == '2':
        async with state.proxy() as data:
            data['floor'] = "2 этаж"
    if floor_number == '3':
        async with state.proxy() as data:
            data['floor'] = "3 этаж"
    if floor_number == '4':
        async with state.proxy() as data:
            data['floor'] = "4 этаж"
    if floor_number == '5':
        async with state.proxy() as data:
            data['floor'] = "5 этаж"
    if floor_number == '6':
        async with state.proxy() as data:
            data['floor'] = "6 этаж"
    floor = data['floor']
    building = data['building']
    await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                text='Выберите кабинет для изменения:',
                                reply_markup=await inline_keyboard_cabinets_admin(building, floor))
    await MapNavigationUpdate.cabinet.set()
    await call.answer()


@dp.callback_query_handler(cabinet_callback_update.filter(), state=MapNavigationUpdate.cabinet)
async def map_nav_admin_state_cabinet_update(call: CallbackQuery, state: FSMContext, callback_data: dict):
    logging.info(f'User({call.message.chat.id}) нажал на кнопку {call.data}')
    cabinet_name = callback_data.get('cabinet')
    async with state.proxy() as data:
        data['cabinet'] = cabinet_name
    await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                text=f'<b>Выберите что хотите изменить для:</b>\n'
                                     f"<b>• Кабинет:</b> {data['cabinet']}\n"
                                     f"<b>• Здание:</b> {data['building']}\n"
                                     f"<b>• Этаж:</b> {data['floor']}\n",
                                parse_mode='HTML', reply_markup=cancel_or_description_or_image_map_nav_admin())
    await state.reset_state(with_data=False)
    print(callback_data)
    await call.answer()


@dp.callback_query_handler(text='update_description_state', state=None)
async def map_nav_admin_state_cabinet_update_description(call: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                text=f"<b>Напишите изменение описания:</b>\n"
                                     f"<b>• Кабинет:</b> {data['cabinet']}\n"
                                     f"<b>• Здание:</b> {data['building']}\n"
                                     f"<b>• Этаж:</b> {data['floor']}\n",
                                parse_mode='HTML',
                                reply_markup=inline_keyboard_cancel_map_nav_admin())
    await MapNavigationUpdate.description.set()
    await call.answer()


@dp.message_handler(content_types=ContentType.ANY, state=MapNavigationUpdate.description)
async def map_nav_admin_state_description_update(message: types.Message, state: FSMContext):
    await delete_inline_buttons_in_dialogue(message)
    if message.content_type == 'text':
        data = await state.get_data()
        await state.update_data(user_id=message.chat.id)
        async with state.proxy() as data:
            data['description'] = message.text
        if len(data) > 5:
            await bot.send_message(message.chat.id, text=f"<b>Данные:</b>\n"
                                                         f"<b>• Кабинет:</b> {data['cabinet']}\n"
                                                         f"<b>• Здание:</b> {data['building']}\n"
                                                         f"<b>• Этаж:</b> {data['floor']}\n"
                                                         f"<b>• Описание:</b> {data['description']}\n"
                                                         f"<b>Отправить данные?</b>",
                                   parse_mode='HTML',
                                   reply_markup=cancel_or_update_map_nav_admin())
            await state.reset_state(with_data=False)
        else:
            await bot.send_message(message.chat.id, text=f"<b>Данные:</b>\n"
                                                         f"<b>• Кабинет:</b> {data['cabinet']}\n"
                                                         f"<b>• Здание:</b> {data['building']}\n"
                                                         f"<b>• Этаж:</b> {data['floor']}\n"
                                                         f"<b>• Описание:</b> {data['description']}\n"
                                                         f"<b>Добавить или изменить фото?</b>",
                                   parse_mode='HTML',
                                   reply_markup=cancel_or_update_or_image_map_nav_admin())
            await state.reset_state(with_data=False)

    else:
        await message.answer('Ошибка - вы отправили не текст повторите',
                             reply_markup=inline_keyboard_cancel_contact_center_admin())


@dp.callback_query_handler(text='update_image_navigation_admin', state=None)
async def map_nav_admin_image_send_message(call: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                text=f'<b>Отправьте фото для:</b>\n'
                                     f"<b>• Кабинет:</b> {data['cabinet']}\n"
                                     f"<b>• Здание:</b> {data['building']}\n"
                                     f"<b>• Этаж:</b> {data['floor']}\n",
                                parse_mode='HTML',
                                reply_markup=inline_keyboard_cancel_map_nav_admin())
    await MapNavigationUpdate.image.set()
    await call.answer()


@dp.message_handler(content_types=ContentType.ANY, state=MapNavigationUpdate.image)
async def map_nav_admin_state_image_step(message: types.Message, state: FSMContext):
    await delete_inline_buttons_in_dialogue(message)
    if message.content_type == 'photo':
        data = await state.get_data()
        await state.update_data(user_id=message.chat.id)
        async with state.proxy() as data:
            data['image'] = message.photo[-1].file_id
        if len(data) > 5:
            await bot.send_message(message.chat.id, text=f"<b>Фото изменено!</b>\n"
                                                         f"<b>Данные:</b>\n"
                                                         f"<b>• Кабинет:</b> {data['cabinet']}\n"
                                                         f"<b>• Здание:</b> {data['building']}\n"
                                                         f"<b>• Этаж:</b> {data['floor']}\n"
                                                         f"<b>• Описание:</b> {data['description']}\n"
                                                         f"<b>Отправить данные?</b>",
                                   parse_mode='HTML',
                                   reply_markup=cancel_or_update_map_nav_admin())
            await state.reset_state(with_data=False)
        else:
            await bot.send_message(message.chat.id, text=f"Фото изменено!\n"
                                                         f"<b>Данные:</b>\n"
                                                         f"<b>• Кабинет:</b> {data['cabinet']}\n"
                                                         f"<b>• Здание:</b> {data['building']}\n"
                                                         f"<b>• Этаж:</b> {data['floor']}\n"
                                                         f"<b>Отправить данные?</b>",
                                   parse_mode='HTML',
                                   reply_markup=cancel_or_description_or_send_map_nav_admin())
            await state.reset_state(with_data=False)
    else:
        await message.answer('Ошибка - вы отправили не фото повторите',
                             reply_markup=inline_keyboard_cancel_map_nav_admin())


@dp.callback_query_handler(text='update_map_navigation_admin', state=None)
async def map_nav_admin_state_send_final_description(call: CallbackQuery, state: FSMContext):
    try:
        data = await state.get_data()
        if len(data) > 5:
            await db.update_map_nav_description_data(data['user_id'], data['building'], data['floor'], data['cabinet'],
                                                     data['description'], data['image'])
            await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                        text=f"✅ Помещение <b>{data['cabinet']}</b> для:\n"
                                             f"<b>{data['building']}</b> <b>{data['floor']}</b> успешно изменено.\n"
                                             "Админ меню карт-навигации",
                                        parse_mode='HTML',
                                        reply_markup=inline_keyboard_map_nav_admin_menu())
            await state.reset_state()
        else:
            await db.update_map_nav_description_data_noimage(data['user_id'], data['building'], data['floor'],
                                                             data['cabinet'],
                                                             data['description'])
            await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                        text=f"✅ Помещение <b>{data['cabinet']}</b> для:\n"
                                             f"<b>{data['building']}</b> <b>{data['floor']}</b> успешно изменено.\n"
                                             "Админ меню карт-навигации",
                                        parse_mode='HTML',
                                        reply_markup=inline_keyboard_map_nav_admin_menu())
            await state.reset_state()
        logging.info(f'User({call.message.chat.id}) отправил информацию для кабинета')
        await call.answer()
    except Exception as e:
        await call.message.answer(f'Ошибка описание не отправлено, (Ошибка - {e})')
        print(e)


@dp.callback_query_handler(text='update_photo_map_navigation_admin', state=None)
async def map_nav_admin_state_send_final_photo(call: CallbackQuery, state: FSMContext):
    try:
        data = await state.get_data()
        await db.update_map_nav_description_data_nodescription(data['user_id'], data['building'], data['floor'],
                                                               data['cabinet'],
                                                               data['image'])
        await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                    text=f"✅ Помещение <b>{data['cabinet']}</b> для:\n"
                                         f"<b>{data['building']}</b> <b>{data['floor']}</b> успешно изменено.\n"
                                         "Админ меню карт-навигации",
                                    parse_mode='HTML',
                                    reply_markup=inline_keyboard_map_nav_admin_menu())
        await state.reset_state()
        logging.info(f'User({call.message.chat.id}) отправил фото для кабинета')
        await call.answer()
    except Exception as e:
        await call.message.answer(f'Ошибка описание не отправлено, (Ошибка - {e})')
        print(e)


#######################################  Удаление Кабинетов   ##########################################


@dp.callback_query_handler(text='delete_cabinet_admin', state=None)
async def callback_map_nav_admin_state_delete(call: CallbackQuery):
    await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                text='Выберите здание где хотите удалить кабинет',
                                reply_markup=keyboard_map_nav_choice_building_delete())
    await MapNavigationDelete.building.set()
    await call.answer()


@dp.callback_query_handler(text='new_building_choice_admin_delete', state=MapNavigationDelete.building)
async def map_nav_admin_state_building1_delete(call: CallbackQuery, state: FSMContext):
    building_data = 'Новое здание'
    async with state.proxy() as data:
        data['building'] = building_data
    await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                text='Выберите этаж в каком хотите удалить кабинет',
                                reply_markup=map_nav_admin_choice_floor_new_delete())
    await MapNavigationDelete.floor.set()
    await call.answer()


@dp.callback_query_handler(text='old_building_choice_admin_delete', state=MapNavigationDelete.building)
async def map_nav_admin_state_building2_delete(call: CallbackQuery, state: FSMContext):
    building_data = 'Старое здание'
    async with state.proxy() as data:
        data['building'] = building_data
    await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                text='Выберите этаж в каком хотите удалить кабинет',
                                reply_markup=map_nav_admin_choice_floor_old_delete())
    await MapNavigationDelete.floor.set()
    await call.answer()


@dp.callback_query_handler(lambda floor: floor.data and floor.data.startswith('floor_choice_admin_delete'),
                           state=MapNavigationDelete.floor)
async def map_nav_admin_state_floor_delete(call: CallbackQuery, state: FSMContext):
    floor_number = call.data[-1]
    if floor_number == '1':
        async with state.proxy() as data:
            data['floor'] = "1 этаж"
    if floor_number == '2':
        async with state.proxy() as data:
            data['floor'] = "2 этаж"
    if floor_number == '3':
        async with state.proxy() as data:
            data['floor'] = "3 этаж"
    if floor_number == '4':
        async with state.proxy() as data:
            data['floor'] = "4 этаж"
    if floor_number == '5':
        async with state.proxy() as data:
            data['floor'] = "5 этаж"
    if floor_number == '6':
        async with state.proxy() as data:
            data['floor'] = "6 этаж"
    floor = data['floor']
    building = data['building']
    await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                text='Выберите какой кабинет хотите удалить',
                                reply_markup=await inline_keyboard_cabinets_admin(building, floor))
    await MapNavigationDelete.cabinet.set()
    await call.answer()


@dp.callback_query_handler(cabinet_callback_update.filter(), state=MapNavigationDelete.cabinet)
async def map_nav_admin_state_cabinet_delete(call: CallbackQuery, state: FSMContext, callback_data: dict):
    logging.info(f'User({call.message.chat.id}) нажал на кнопку {call.data}')
    cabinet_name = callback_data.get('cabinet')
    await state.update_data(cabinet=cabinet_name)
    await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                text=f'Удалить <b>{cabinet_name}? </b>',
                                parse_mode='HTML', reply_markup=cancel_or_delete_map_nav_admin())
    await state.reset_state(with_data=False)
    await call.answer()


@dp.callback_query_handler(text='delete_map_navigation_admin', state=None)
async def map_nav_admin_state_delete_final(call: CallbackQuery, state: FSMContext):
    try:
        data = await state.get_data()
        await db.delete_map_nav_description_data(data['building'], data['floor'], data['cabinet'])
        await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                    text=f"✅ Помещение <b>{data['cabinet']}</b> для:\n"
                                         f"<b>{data['building']}</b> <b>{data['floor']}</b> успешно удалено.\n"
                                         "Админ меню карт-навигации",
                                    reply_markup=inline_keyboard_map_nav_admin_menu())
        logging.info(f'User({call.message.chat.id}) удалил информацию кабинета')
        await call.answer()
    except Exception as e:
        await call.message.answer(f'Ошибка описание не отправлено, (Ошибка - {e})')
        print(e)


@dp.callback_query_handler(text='cancel_step_map_nav_admin', state=['*'])
async def callback_inline_cancel_step_map_nav(call: CallbackQuery, state: FSMContext):
    logging.info(f'User({call.message.chat.id}) нажал на кнопку {call.data}')
    await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                text="Админ меню карт-навигации",
                                reply_markup=inline_keyboard_map_nav_admin_menu())
    await state.reset_state()
    await call.answer()
