import logging
from aiogram import types
from aiogram.types import CallbackQuery, ContentType
from loader import dp, bot
from keyboards.inline.admin_buttons import inline_keyboard_admin, inline_keyboard_massive_send_all, \
    inline_keyboard_cancel_or_send, inline_keyboard_cancel, cancel_or_send_schedule

# Импортирование функций из БД контроллера
from utils import db_api as db

from utils.delete_messages import bot_delete_messages
from aiogram.dispatcher import FSMContext
from states.admin import AdminSendAll, AdminSendScheduleToBot

from utils.misc import rate_limit


@rate_limit(5, 'admin')
@dp.message_handler(commands=['admin'])
async def admin_menu(message):
    try:
        if await db.check_role(message.chat.id, 'admin') == 'admin':
            logging.info(f'Пользователь {message.chat.username} вошел в админ меню')
            users = await db.count_users()
            await bot.send_message(message.chat.id, f'Меню Админа:\n- Количество пользователей = {users}\n'
                                                    f'- Рассылка - Разослать сообщение всем пользователям\n'
                                                    f'- Отправить расписание - отправить расписание боту',
                                   reply_markup=inline_keyboard_admin())
        else:
            await bot.send_message(message.chat.id, 'Недостаточный уровень доступа')
            logging.info(f'Пользователь {message.chat.username} попытался войти в админ меню')
    except Exception as e:
        print(e)


@dp.callback_query_handler(text='send_all', state=None)
async def callback_inline_send_all(call: CallbackQuery):
    await call.message.answer('Напишите текст сообщения для массовой рассылки:')
    await AdminSendAll.message_text.set()


@dp.callback_query_handler(text='add_photo_mass')
async def callback_inline_add_photo_mass(call: CallbackQuery):
    await bot.send_message(call.message.chat.id, 'Прикрепите фото к сообщению')
    await AdminSendAll.message_photo.set()


@dp.callback_query_handler(text='cancel')
async def callback_inline_cancel(call: CallbackQuery, state: FSMContext):
    await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                text='ОТМЕНЕНЕНО')
    await bot_delete_messages(call.message, 3)
    await state.reset_state()


@dp.message_handler(content_types=ContentType.ANY, state=AdminSendAll.message_text)
async def message_send_text(message: types.Message, state: FSMContext):
    if message.content_type == 'text':
        await state.update_data(message_text_all=message.text)
        message_txt = 'Ваше сообщение:\n' + message.text + '\n (*ВЫ УВЕРЕНЫ?*)'
        await bot.send_message(message.chat.id, message_txt, reply_markup=inline_keyboard_massive_send_all())
        await state.reset_state(with_data=False)
    else:
        print(message.content_type)
        await bot.send_message(message.chat.id,
                               'Ошибка - ваще сообщение должно содержать только текст\nНапишите текст сообщения для массовой рассылки:')


@dp.callback_query_handler(text='send_send_to_all')
async def callback_inline_send_send_all(call: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    if len(data) == 2:
        await bot_delete_messages(call.message, 5)
        await bot.delete_message(call.message.chat.id, call.message.message_id)
        await bot.send_message(call.message.chat.id, '<b>Массовая рассылка отправлена:</b>', parse_mode='HTML')
        users = await db.select_users()
        for i in users:
            try:
                await bot.send_photo(i, data['photo_send_all'], caption=data['message_text_all'])
            except Exception as e:
                print('Наверно блокнул бота', e)
        await state.reset_state()
    else:
        await bot_delete_messages(call.message, 2)
        await bot.delete_message(call.message.chat.id, call.message.message_id)
        await bot.send_message(call.message.chat.id, '<b>Массовая рассылка отправлена:</b>', parse_mode='HTML')
        users = await db.select_users()
        for i in users:
            try:
                await bot.send_message(i, data['message_text_all'])
            except Exception as e:
                print('Наверно блокнул бота', e)
        await state.reset_state()


@dp.message_handler(content_types=ContentType.ANY, state=AdminSendAll.message_photo)
async def message_send_photo(message: types.Message, state: FSMContext):
    if message.content_type == 'photo':
        await state.update_data(photo_send_all=message.photo[-1].file_id)
        data = await state.get_data()
        message_txt = 'Ваше сообщение:\n' + data['message_text_all'] + '\n (*ВЫ УВЕРЕНЫ?*)'
        await bot.send_message(message.chat.id, message_txt, reply_markup=inline_keyboard_cancel_or_send())
        await state.reset_state(with_data=False)
    else:
        print(message.content_type)
        await bot.send_message(message.chat.id,
                               'Ошибка - отправьте картинку как "Фото", не как "Файл"')


#### Отправка расписания ####
@dp.callback_query_handler(text='send_schedule_bot', state=None)
async def callback_inline_send_schedule_bot(call: CallbackQuery):
    await call.message.answer('Напишите название для кнопки, например (3 Курс):', reply_markup=inline_keyboard_cancel())
    await AdminSendScheduleToBot.button_name.set()


@dp.callback_query_handler(text='cancel_step', state=['*'])
async def callback_inline_cancel_step(call: CallbackQuery, state: FSMContext):
    await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                text='<b>Отправка расписания отменена</b>', parse_mode='HTML')
    await state.reset_state()


@dp.message_handler(content_types=ContentType.ANY, state=AdminSendScheduleToBot.button_name)
async def message_send_button_name(message: types.Message, state: FSMContext):
    if message.content_type == 'text':
        await state.update_data(button_name=message.text.lower(),
                                user_id=message.chat.id)
        await bot.send_message(message.chat.id, 'Отправьте файл с расписанием', reply_markup=inline_keyboard_cancel())
        await AdminSendScheduleToBot.send_file.set()
    else:
        print(message.content_type)
        await bot.send_message(message.chat.id,
                               'Ошибка - название может содержать только текст\nПовторите название для кнопки, например (3 Курс):')


@dp.message_handler(content_types=ContentType.ANY, state=AdminSendScheduleToBot.send_file)
async def message_schedule_send_file(message: types.Message, state: FSMContext):
    if message.content_type == 'document':
        await state.update_data(file_id=message.document.file_id)
        data = await state.get_data()
        txt = f'Название кнопки будет: {data["button_name"]}'
        await bot.send_document(message.chat.id, data["file_id"], caption=txt,
                                reply_markup=cancel_or_send_schedule())
        await state.reset_state(with_data=False)
    else:
        await message.answer('Ошибка - вы отправили не документ\nПовторите Отправление файла с расписанием')


@dp.callback_query_handler(text='send_schedule', state=None)
async def callback_inline_send_schedule(call: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    await bot_delete_messages(call.message, 4)
    await db.add_schedule_data(data['user_id'], data['file_id'], data["button_name"])
    await bot.delete_message(call.message.chat.id, call.message.message_id)
    await call.message.answer(f'Расписание для <b>{data["button_name"]}</b> отправлено', parse_mode='HTML')


@dp.callback_query_handler(text_contains='cancel_schedule')
async def callback_inline_cancel_schedule(call: CallbackQuery, state: FSMContext):
    await bot_delete_messages(call.message, 4)
    await bot.delete_message(call.message.chat.id, call.message.message_id)
    await call.message.answer('==Отправка отменена==')
    await state.reset_state()
