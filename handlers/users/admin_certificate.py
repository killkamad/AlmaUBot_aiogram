import ast
import logging
from aiogram.utils import exceptions
from aiogram import types
from aiogram.types import CallbackQuery, ContentType
from aiogram.dispatcher import FSMContext
from loader import dp, bot
from .admin_menu import admin_menu
from utils.delete_messages import bot_delete_messages

# Импорт клавиатур
from keyboards.inline.admin_buttons import inline_keyboard_admin, inline_keyboard_cancel, cancel_or_send_certificate, \
    inline_keyboard_update_certificate, cancel_or_update_certificate, inline_keyboard_delete_certificate, \
    cancel_or_delete_certificate, inline_keyboard_get_request_certificate, inline_keyboard_upd_req_certificate, \
    inline_keyboard_del_req_certificate

# Импортирование функций из БД контроллера
from utils import db_api as db

# Импорт стейтов
from states.admin import SendCertificate, UpdateCertificate, DeleteCertificate

from utils.misc import rate_limit

#### Отправка справки ####
@dp.callback_query_handler(text_contains="['request_call'")
async def callback_inline_send_id(call: CallbackQuery, state: FSMContext):
    logging.info(f'call = {call.data}')
    valueFromCallBack = ast.literal_eval(call.data)[1]
    request_id = await db.find_request_id(valueFromCallBack)
    await state.update_data(request=request_id)
    await bot.send_message(call.message.chat.id, 'Напишите наименование справки, например (Справка в военкомат):',
                           reply_markup=inline_keyboard_cancel())
    await SendCertificate.button_name.set()


@dp.callback_query_handler(text='send_certificate_bot', state=None)
async def callback_inline_send_certificate_bot(call: CallbackQuery):
    logging.info(f'User({call.message.chat.id}) нажал на кнопку {call.data}')
    await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                text='Выберите студента запросившего справку:',
                                reply_markup=await inline_keyboard_get_request_certificate())


#### Обновление справки ####
@dp.callback_query_handler(text='update_certificate_bot', state=None)
async def callback_inline_update_certificate_bot(call: CallbackQuery):
    logging.info(f'User({call.message.chat.id}) нажал на кнопку {call.data}')
    await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                text='Выберите студента для изменения:',
                                reply_markup=await inline_keyboard_upd_req_certificate())


@dp.callback_query_handler(text_contains="['upd_req_std'")
async def callback_inline_send_id(call: CallbackQuery, state: FSMContext):
    logging.info(f'call = {call.data}')
    value = ast.literal_eval(call.data)[1]
    id_telegram = await db.find_request_id_telegram(value)
    valueFromCallBack = ast.literal_eval(call.data)[1]
    request_id = await db.find_request_id(valueFromCallBack)
    await state.update_data(request=request_id)
    await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                text='Выберите справку для изменения:',
                                reply_markup=await inline_keyboard_update_certificate(id_telegram))


#### ОТМЕНА Обновление справки
@dp.callback_query_handler(text='cancel_update_step')
async def callback_inline_cancel_update_certificate_bot(call: CallbackQuery, state: FSMContext):
    logging.info(f'User({call.message.chat.id}) нажал на кнопку {call.data}')
    users = await db.count_users()
    await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                text=f'Меню Админа:\n- Количество пользователей = {users}\n'
                                     f'- Рассылка - Разослать сообщение всем пользователям\n'
                                     f'- Отправить справку - отправить справку боту',
                                reply_markup=inline_keyboard_admin())
    await state.reset_state()


@dp.callback_query_handler(text_contains="['update_certificate'", state=['*'])
async def callback_inline_update_certificate(call: CallbackQuery, state: FSMContext):
    logging.info(f'User({call.message.chat.id}) нажал на кнопку {call.data}')
    value = ast.literal_eval(call.data)[1]
    certificate_button_name = await db.find_certificate_name(value)
    await state.update_data(button_name=certificate_button_name, user_id=call.message.chat.id)
    data = await state.get_data()
    print(data)
    await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                text=f'Отправьте файл со справкой для кнопки <b>{certificate_button_name}</b>:',
                                parse_mode='HTML')
    await UpdateCertificate.send_file.set()


@dp.message_handler(content_types=ContentType.ANY, state=UpdateCertificate.send_file)
async def change_certificate_id(message: types.Message, state: FSMContext):
    await UpdateCertificate.send_file.set()
    if message.content_type == 'document':
        await state.update_data(file_id=message.document.file_id)
        data = await state.get_data()
        txt = f'Наименование справки: <b>{data["button_name"]}</b>'
        await bot.send_document(message.chat.id, data["file_id"], caption=txt,
                                reply_markup=cancel_or_update_certificate())
        await state.reset_state(with_data=False)
    else:
        await bot.send_message(message.chat.id,
                               'Ошибка - вы отправили не документ\nПовторите Отправление файла со справкой',
                               reply_markup=inline_keyboard_cancel())


#### Удаление справки ####
@dp.callback_query_handler(text='delete_certificate_bot', state=None)
async def callback_inline_send_certificate_bot(call: CallbackQuery):
    logging.info(f'User({call.message.chat.id}) нажал на кнопку {call.data}')
    await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                text='Выберите студента:',
                                reply_markup=await inline_keyboard_del_req_certificate())


@dp.callback_query_handler(text_contains="['del_req_std'")
async def callback_inline_send_id(call: CallbackQuery, state: FSMContext):
    logging.info(f'call = {call.data}')
    value = ast.literal_eval(call.data)[1]
    id_telegram = await db.find_request_id_telegram(value)
    valueFromCallBack = ast.literal_eval(call.data)[1]
    request_id = await db.find_request_id(valueFromCallBack)
    await state.update_data(request=request_id)
    await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                text='Выберите справку для удаления:',
                                reply_markup=await inline_keyboard_delete_certificate(id_telegram))


#### ОТМЕНА Удаления справки
@dp.callback_query_handler(text='cancel_delete_step')
async def callback_inline_cancel_update_certificate_bot(call: CallbackQuery, state: FSMContext):
    logging.info(f'User({call.message.chat.id}) нажал на кнопку {call.data}')
    users = await db.count_users()
    await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                text=f'Меню Админа:\n- Количество пользователей = {users}\n'
                                     f'- Рассылка - Разослать сообщение всем пользователям\n'
                                     f'- Отправить справку - отправить справку боту',
                                reply_markup=inline_keyboard_admin())
    await state.reset_state()


@dp.callback_query_handler(text_contains="['delete_certificate'", state=['*'])
async def callback_inline_update_certificate(call: CallbackQuery, state: FSMContext):
    logging.info(f'User({call.message.chat.id}) нажал на кнопку {call.data}')
    value = ast.literal_eval(call.data)[1]
    certificate_button_name = await db.find_certificate_name(value)
    await state.update_data(button_name=certificate_button_name, user_id=call.message.chat.id)
    await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                text=f'Вы точно уверены, что хотите удалить кнопку справки для <b>{certificate_button_name}</b>:',
                                parse_mode='HTML', reply_markup=cancel_or_delete_certificate())
    await DeleteCertificate.confirm_delete.set()


@dp.callback_query_handler(text='cancel_step', state=['*'])
async def callback_inline_cancel_step(call: CallbackQuery, state: FSMContext):
    logging.info(f'User({call.message.chat.id}) нажал на кнопку {call.data}')
    await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                text='<b>Отправка справки отменена</b>', parse_mode='HTML')
    await state.reset_state()


# Проверка сообщения на текст, если текст, то сохраняет это сообщение и айди в state
@dp.message_handler(content_types=ContentType.ANY, state=SendCertificate.button_name)
async def message_send_button_name(message: types.Message, state: FSMContext):
    if message.content_type == 'text':
        await state.update_data(button_name=message.text,
                                user_id=message.chat.id)
        await bot.send_message(message.chat.id, 'Отправьте файл со справкой', reply_markup=inline_keyboard_cancel())
        await SendCertificate.send_file.set()
    else:
        print(message.content_type)
        await bot.send_message(message.chat.id,
                               'Ошибка - название может содержать только текст\nПовторите наименование справки, например (Справка в военкомат):')


# Проверка если отправлен файл, то сохраняет айди файла в state
@dp.message_handler(content_types=ContentType.ANY, state=SendCertificate.send_file)
async def message_certificate_send_file(message: types.Message, state: FSMContext):
    if message.content_type == 'document':
        await state.update_data(file_id=message.document.file_id)
        data = await state.get_data()
        txt = f'Наименование справки будет: {data["button_name"]}\n' \
              f'Номер заявки: {data["request"]}'
        await bot.send_document(message.chat.id, data["file_id"], caption=txt,
                                reply_markup=cancel_or_send_certificate())
        await state.reset_state(with_data=False)
    else:
        await message.answer('Ошибка - вы отправили не документ\nПовторите Отправление файла со справкой')


# Отправление справки в базу данных
@dp.callback_query_handler(text='send_certificate', state=None)
async def callback_inline_send_certificate(call: CallbackQuery, state: FSMContext):
    try:
        data = await state.get_data()
        await bot_delete_messages(call.message, 4)
        await db.add_certificate_data(data['user_id'], data['request'], data['file_id'], data['button_name'])
        await bot.delete_message(call.message.chat.id, call.message.message_id)
        await call.message.answer(f'Справка для <b>{data["button_name"]}</b> отправлена', parse_mode='HTML')
        logging.info(f'User({call.message.chat.id}) отправил справку для {data["button_name"]}')
        await admin_menu(call.message)
    except Exception as e:
        await call.message.answer(f'Ошибка справка не отправлена, (Ошибка - {e})')
        print(e)


# Успешное обновление справки в базе данных
@dp.callback_query_handler(text='update_certificate_button', state=None)
async def callback_inline_send_certificate(call: CallbackQuery, state: FSMContext):
    try:
        data = await state.get_data()
        await bot_delete_messages(call.message, 2)
        await db.update_certificate_data(data['user_id'], data['request'], data['file_id'], data["button_name"])
        await bot.delete_message(call.message.chat.id, call.message.message_id)
        await call.message.answer(f'Справка для <b>{data["button_name"]}</b> успешно обновлена', parse_mode='HTML')
        logging.info(f'User({call.message.chat.id}) обновил справку для {data["button_name"]}')
        await admin_menu(call.message)

    except Exception as e:
        await call.message.answer(f'Ошибка справка не обновлена, (Ошибка - {e})')
        logging.info(f'Ошибка - {e}')


# Удаление справки из базы данных
@dp.callback_query_handler(text='delete_certificate_button', state=DeleteCertificate.confirm_delete)
async def callback_inline_send_certificate(call: CallbackQuery, state: FSMContext):
    try:
        data = await state.get_data()
        await db.delete_certificate_button(data["button_name"])
        await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                    text=f'Справка для <b>{data["button_name"]}</b> успешно удалена из базы данных',
                                    parse_mode='HTML')
        await admin_menu(call.message)
        await state.reset_state()
        logging.info(f'User({call.message.chat.id}) удалил справку для {data["button_name"]}')
    except Exception as e:
        await call.message.answer(f'Ошибка справка не удалена, (Ошибка - {e})')
        logging.info(f'Ошибка - {e}')


@dp.callback_query_handler(text_contains='cancel_certificate')
async def callback_inline_cancel_certificate(call: CallbackQuery, state: FSMContext):
    logging.info(f'User({call.message.chat.id}) отменил отправку справки call.data - {call.data}')
    await bot_delete_messages(call.message, 4)
    await bot.delete_message(call.message.chat.id, call.message.message_id)
    await call.message.answer('<b>Отправка справки отменена</b>', parse_mode='HTML')
    await state.reset_state()


@dp.callback_query_handler(text_contains='cancel_update_certificate')
async def callback_inline_cancel_update_certificate(call: CallbackQuery, state: FSMContext):
    logging.info(f'User({call.message.chat.id}) отменил обновления справки call.data - {call.data}')
    await bot_delete_messages(call.message, 2)
    await bot.delete_message(call.message.chat.id, call.message.message_id)
    await call.message.answer('<b>Обновление|Изменение отменено</b>', parse_mode='HTML')
    await admin_menu(call.message)
    await state.reset_state()


@dp.callback_query_handler(text_contains='cancel_delete_certificate', state=DeleteCertificate.confirm_delete)
async def callback_inline_cancel_delete_certificate(call: CallbackQuery, state: FSMContext):
    logging.info(f'User({call.message.chat.id}) отменил удаление справки call.data - {call.data}')
    await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                text='<b>Удаление отменено</b>', parse_mode='HTML')
    await admin_menu(call.message)
    await state.reset_state()
