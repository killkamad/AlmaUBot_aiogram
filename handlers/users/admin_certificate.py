import logging
from aiogram.utils import exceptions
from aiogram import types
from aiogram.types import CallbackQuery, ContentType
from aiogram.dispatcher import FSMContext
from loader import dp, bot
from .admin_menu import admin_menu, certificate_admin_menu

# Импорт клавиатур
from keyboards.inline import inline_keyboard_admin, inline_keyboard_cancel_certificate, cancel_or_send_certificate, \
    inline_keyboard_update_certificate, cancel_or_update_certificate, inline_keyboard_delete_certificate, \
    cancel_or_delete_certificate, inline_keyboard_upd_req_certificate, \
    inline_keyboard_del_req_certificate, inline_keyboard_certificate_admin, request_callback, \
    certificate_update_callback, certificate_delete_callback, request_update_callback, request_delete_callback, \
    request_type_callback, inline_keyboard_get_certificate_type, \
    inline_keyboard_on_send_request_certificate

# Импортирование функций из БД контроллера
from utils import db_api as db

# Импорт стейтов
from states.admin import SendCertificate, UpdateCertificate, DeleteCertificate

from utils.misc import rate_limit


@dp.callback_query_handler(request_callback.filter())
async def callback_inline(call: CallbackQuery, callback_data: dict, state: FSMContext):
    logging.info(f'call = {call.data}')
    request_name = callback_data.get('request_name')
    request_id = await db.find_request_id(request_name)
    id_telegram = await db.find_request_id_telegram(request_name)
    await state.update_data(request=request_id)
    await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                text='Выберите заявку:',
                                reply_markup=await inline_keyboard_get_certificate_type(id_telegram))


@dp.callback_query_handler(text='send_certificate_bot', state=None)
async def callback_inline_send_certificate_bot(call: CallbackQuery):
    logging.info(f'User({call.message.chat.id}) нажал на кнопку {call.data}')
    await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                text='Выберите студента запросившего справку:',
                                reply_markup=await inline_keyboard_on_send_request_certificate())


#### ОТМЕНА Отправления справки
@dp.callback_query_handler(text='cancel_load_step')
async def callback_inline_cancel_load_certificate_bot(call: CallbackQuery, state: FSMContext):
    logging.info(f'User({call.message.chat.id}) нажал на кнопку {call.data}')
    users = await db.count_users()
    await certificate_admin_menu(call)
    await state.reset_state()


#### Обновление справки ####
@dp.callback_query_handler(text='update_certificate_bot', state=None)
async def callback_inline_update_certificate_bot(call: CallbackQuery):
    logging.info(f'User({call.message.chat.id}) нажал на кнопку {call.data}')
    await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                text='Выберите студента для изменения:',
                                reply_markup=await inline_keyboard_upd_req_certificate())


@dp.callback_query_handler(request_update_callback.filter())
async def callback_inline(call: CallbackQuery, callback_data: dict, state: FSMContext):
    logging.info(f'call = {call.data}')
    request_name = callback_data.get('request_name')
    request_id = await db.find_request_id(request_name)
    id_telegram = await db.find_request_id_telegram(request_name)
    await state.update_data(request=request_id, id_student=id_telegram)
    await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                text='Выберите справку для изменения:',
                                reply_markup=await inline_keyboard_update_certificate(id_telegram))


#### ОТМЕНА Обновление справки
@dp.callback_query_handler(text='cancel_update_step')
async def callback_inline_cancel_update_certificate_bot(call: CallbackQuery, state: FSMContext):
    logging.info(f'User({call.message.chat.id}) нажал на кнопку {call.data}')
    users = await db.count_users()
    await certificate_admin_menu(call)
    await state.reset_state()


@dp.callback_query_handler(certificate_update_callback.filter(), state=['*'])
async def callback_inline(call: CallbackQuery, callback_data: dict, state: FSMContext):
    logging.info(f'call = {call.data}')
    req_id = callback_data.get('id')
    certificate_button_name = await db.find_certificate_name(req_id)
    await state.update_data(button_name=certificate_button_name, user_id=call.message.chat.id, id_req=req_id)
    await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                text=f'Отправьте файл со справкой для кнопки <b>{certificate_button_name}</b>:',
                                parse_mode='HTML', reply_markup=inline_keyboard_cancel_certificate())
    await UpdateCertificate.send_file.set()


@dp.message_handler(content_types=ContentType.ANY, state=UpdateCertificate.send_file)
async def change_certificate_id(message: types.Message, state: FSMContext):
    await UpdateCertificate.send_file.set()
    if message.content_type == 'document':
        await state.update_data(file_id=message.document.file_id)
        data = await state.get_data()
        txt = f'Наименование справки: <b>{data["button_name"]}</b>'
        try:
            await bot.edit_message_reply_markup(message.chat.id, message.message_id - 1)
            await bot.send_document(message.chat.id, data["file_id"], caption=txt,
                                    reply_markup=cancel_or_update_certificate())
        except:
            await bot.send_document(message.chat.id, data["file_id"], caption=txt,
                                    reply_markup=cancel_or_update_certificate())
        await state.reset_state(with_data=False)
    else:
        try:
            await bot.edit_message_reply_markup(message.chat.id, message.message_id - 1)
            await bot.send_message(message.chat.id,
                                   'Ошибка - вы отправили не документ\nПовторите Отправление файла со справкой',
                                   reply_markup=inline_keyboard_cancel_certificate())
        except:
            await bot.send_message(message.chat.id,
                                   'Ошибка - вы отправили не документ\nПовторите Отправление файла со справкой',
                                   reply_markup=inline_keyboard_cancel_certificate())


#### Удаление справки ####
@dp.callback_query_handler(text='delete_certificate_bot', state=None)
async def callback_inline_send_certificate_bot(call: CallbackQuery):
    logging.info(f'User({call.message.chat.id}) нажал на кнопку {call.data}')
    await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                text='Выберите студента:',
                                reply_markup=await inline_keyboard_del_req_certificate())


@dp.callback_query_handler(request_delete_callback.filter())
async def callback_inline(call: CallbackQuery, callback_data: dict, state: FSMContext):
    logging.info(f'call = {call.data}')
    request_name = callback_data.get('request_name')
    request_id = await db.find_request_id(request_name)
    id_telegram = await db.find_request_id_telegram(request_name)
    await state.update_data(request=request_id, id_student=id_telegram)
    await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                text='Выберите справку для удаления:',
                                reply_markup=await inline_keyboard_delete_certificate(id_telegram))


#### ОТМЕНА Удаления справки
@dp.callback_query_handler(text='cancel_delete_step')
async def callback_inline_cancel_delete_certificate_bot(call: CallbackQuery, state: FSMContext):
    logging.info(f'User({call.message.chat.id}) нажал на кнопку {call.data}')
    await certificate_admin_menu(call)
    await state.reset_state()


@dp.callback_query_handler(certificate_delete_callback.filter(), state=['*'])
async def callback_inline(call: CallbackQuery, callback_data: dict, state: FSMContext):
    logging.info(f'call = {call.data}')
    id_request = callback_data.get('id')
    certificate_button_name = await db.find_certificate_name(id_request)
    await state.update_data(button_name=certificate_button_name, user_id=call.message.chat.id, id_req=id_request)
    data = await state.get_data()
    await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                text=f'Вы точно уверены, что хотите удалить кнопку справки для <b>{certificate_button_name}</b>:',
                                parse_mode='HTML', reply_markup=cancel_or_delete_certificate())
    await DeleteCertificate.confirm_delete.set()


@dp.callback_query_handler(text='cancel_step_certificate', state=['*'])
async def callback_inline_cancel_step(call: CallbackQuery, state: FSMContext):
    logging.info(f'User({call.message.chat.id}) нажал на кнопку {call.data}')
    await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                text='<b>❌ Отправка справки отменена</b>\n'
                                     'Возврат в Админ меню Справки:', parse_mode='HTML',
                                reply_markup=inline_keyboard_certificate_admin())
    await state.reset_state()


# Проверка сообщения на текст, если текст, то сохраняет это сообщение и айди в state
@dp.callback_query_handler(request_type_callback.filter(), state=['*'])
async def message_send_button_name(call: CallbackQuery, callback_data: dict, state: FSMContext):
    logging.info(f'call = {call.data}')
    await state.update_data(button_name=call.data[5:], user_id=call.message.chat.id)
    await bot.send_message(chat_id=call.message.chat.id, text='Отправьте файл со справкой', reply_markup=inline_keyboard_cancel_certificate())
    await SendCertificate.send_file.set()


# Проверка если отправлен файл, то сохраняет айди файла в state
@dp.message_handler(content_types=ContentType.ANY, state=SendCertificate.send_file)
async def message_certificate_send_file(message: types.Message, state: FSMContext):
    if message.content_type == 'document':
        await state.update_data(file_id=message.document.file_id, upload=True, request_state=True)
        data = await state.get_data()
        txt = f'Наименование справки будет: {data["button_name"]}\n' \
              f'Номер заявки: {data["request"]}'
        try:
            await bot.edit_message_reply_markup(message.chat.id, message.message_id - 1)
            await bot.send_document(message.chat.id, data["file_id"], caption=txt,
                                    reply_markup=cancel_or_send_certificate())
        except:
            await bot.send_document(message.chat.id, data["file_id"], caption=txt,
                                    reply_markup=cancel_or_send_certificate())
        await state.reset_state(with_data=False)
    else:
        try:
            await bot.edit_message_reply_markup(message.chat.id, message.message_id - 1)
            await bot.send_message(message.chat.id,
                                   'Ошибка - вы отправили не документ\nПовторите Отправление файла со справкой',
                                   reply_markup=inline_keyboard_cancel_certificate())
        except:
            await bot.send_message(message.chat.id,
                                   'Ошибка - вы отправили не документ\nПовторите Отправление файла со справкой',
                                   reply_markup=inline_keyboard_cancel_certificate())


# Отправление справки в базу данных
@dp.callback_query_handler(text='send_certificate', state=None)
async def callback_inline_send_certificate(call: CallbackQuery, state: FSMContext):
    try:
        data = await state.get_data()
        await db.add_certificate_data(data['user_id'], data['request'], data['file_id'], data['button_name'], data['upload'])
        await db.mark_as_loaded_request(data['request'], data['request_state'])
        logging.info(f'User({call.message.chat.id}) отправил справку для {data["button_name"]}')
        try:
            await bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id)
            await bot.send_message(call.message.chat.id, f'Справка для <b>{data["button_name"]}</b> отправлена\n'
                                   'Выберите студента запросившего справку:',
                                   parse_mode='HTML',
                                   reply_markup=await inline_keyboard_on_send_request_certificate())
        except:
            await bot.send_message(call.message.chat.id, f'Справка для <b>{data["button_name"]}</b> отправлена\n'
                                   'Выберите студента запросившего справку:',
                                   parse_mode='HTML',
                                   reply_markup=await inline_keyboard_on_send_request_certificate())
    except Exception as e:
        await call.message.answer(f'Ошибка справка не отправлена, (Ошибка - {e})')
        print(e)


# Успешное обновление справки в базе данных
@dp.callback_query_handler(text='update_certificate_button', state=None)
async def callback_inline_send_certificate(call: CallbackQuery, state: FSMContext):
    try:
        data = await state.get_data()
        await db.update_certificate_data(data['user_id'], data['request'], data['file_id'], data["id_req"])
        logging.info(f'User({call.message.chat.id}) обновил справку для {data["button_name"]}')
        try:
            await bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id)
            await bot.send_message(call.message.chat.id,
                                   f'Справка для <b>{data["button_name"]}</b> успешно обновлена\n'
                                   'Выберите студента для изменения:',
                                   parse_mode='HTML',
                                   reply_markup=await inline_keyboard_upd_req_certificate())
        except:
            await bot.send_message(call.message.chat.id,
                                   f'Справка для <b>{data["button_name"]}</b> успешно обновлена\n'
                                   'Выберите студента для изменения:',
                                   parse_mode='HTML',
                                   reply_markup=await inline_keyboard_upd_req_certificate())
    except Exception as e:
        await call.message.answer(f'Ошибка справка не обновлена, (Ошибка - {e})')
        logging.info(f'Ошибка - {e}')


# Удаление справки из базы данных
@dp.callback_query_handler(text='delete_certificate_button', state=DeleteCertificate.confirm_delete)
async def callback_inline_send_certificate(call: CallbackQuery, state: FSMContext):
    try:
        data = await state.get_data()
        print(data['id_student'])
        await db.delete_certificate_button(data["id_req"])
        await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                    text=f'Справка для <b>{data["button_name"]}</b> успешно удалена из базы данных\n'
                                    'Выберите справку для удаления',
                                    parse_mode='HTML',
                                    reply_markup=await inline_keyboard_delete_certificate(data['id_student']))
        await state.reset_state()
        logging.info(f'User({call.message.chat.id}) удалил справку для {data["button_name"]}')
    except Exception as e:
        await call.message.answer(f'Ошибка справка не удалена, (Ошибка - {e})')
        logging.info(f'Ошибка - {e}')


@dp.callback_query_handler(text_contains='cancel_certificate')
async def callback_inline_cancel_certificate(call: CallbackQuery, state: FSMContext):
    logging.info(f'User({call.message.chat.id}) отменил отправку справки call.data - {call.data}')
    # await bot_delete_messages(call.message, 4)
    await bot.delete_message(call.message.chat.id, call.message.message_id)
    await call.message.answer('<b>Отправка справки отменена</b>\n'
                              'Возврат в Админ меню Справки:',
                              parse_mode='HTML',
                              reply_markup=inline_keyboard_certificate_admin())
    await state.reset_state()


@dp.callback_query_handler(text_contains='cancel_update_certificate')
async def callback_inline_cancel_update_certificate(call: CallbackQuery, state: FSMContext):
    logging.info(f'User({call.message.chat.id}) отменил обновления справки call.data - {call.data}')
    # await bot_delete_messages(call.message, 2)
    await bot.delete_message(call.message.chat.id, call.message.message_id)
    await call.message.answer('<b>Обновление | Изменение отменено</b>\n'
                              'Возврат в Админ меню Справки:',
                              parse_mode='HTML',
                              reply_markup=inline_keyboard_certificate_admin())
    await state.reset_state()


@dp.callback_query_handler(text_contains='cancel_delete_certificate', state=DeleteCertificate.confirm_delete)
async def callback_inline_cancel_delete_certificate(call: CallbackQuery, state: FSMContext):
    logging.info(f'User({call.message.chat.id}) отменил удаление справки call.data - {call.data}')
    await bot.delete_message(call.message.chat.id, call.message.message_id)
    await call.message.answer('<b>Удаление отменено</b>\n'
                              'Возврат в Админ меню Справки:',
                              parse_mode='HTML',
                              reply_markup=inline_keyboard_certificate_admin())
    await state.reset_state()
