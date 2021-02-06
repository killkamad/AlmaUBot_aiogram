import logging
import asyncio
from aiogram.utils import exceptions
from aiogram import types
from aiogram.types import CallbackQuery, ContentType
from aiogram.dispatcher import FSMContext
from loader import dp, bot
from utils.delete_messages import bot_delete_messages

# Импорт клавиатур
from keyboards.inline.admin_buttons import inline_keyboard_massive_send_all, inline_keyboard_cancel_or_send

# Импортирование функций из БД контроллера
from utils import db_api as db

# Импорт стейтов
from states.admin import SendAll

from utils.misc import rate_limit


@dp.callback_query_handler(text='send_all', state=None)
async def callback_inline_send_all(call: CallbackQuery):
    logging.info(f'User({call.message.chat.id}) нажал на кнопку 📣 Рассылка')
    await call.message.answer('Напишите текст сообщения для массовой рассылки:')
    await SendAll.message_text.set()


@dp.callback_query_handler(text='add_photo_mass')
async def callback_inline_add_photo_mass(call: CallbackQuery):
    logging.info(f'User({call.message.chat.id}) нажал на кнопку ➕ Добавить фото или документ')
    await bot.send_message(call.message.chat.id, 'Прикрепите фото к сообщению')
    await SendAll.message_photo.set()


@dp.callback_query_handler(text='cancel_massive_sending')
async def callback_inline_cancel(call: CallbackQuery, state: FSMContext):
    logging.info(f'User({call.message.chat.id}) нажал на кнопку ❌ Отмена')
    await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                text='ОТМЕНЕНО')
    await bot_delete_messages(call.message, 3)
    await state.reset_state()


@dp.message_handler(content_types=ContentType.ANY, state=SendAll.message_text)
async def message_send_text(message: types.Message, state: FSMContext):
    if message.content_type == 'text':
        if len(message.text) <= 990:
            await state.update_data(message_text_all=message.text)
            message_txt = 'Ваше сообщение:\n' + message.text + '\n (*ВЫ УВЕРЕНЫ?*)'
            await bot.send_message(message.chat.id, message_txt, reply_markup=inline_keyboard_massive_send_all())
            await state.reset_state(with_data=False)
        else:
            await bot.send_message(message.chat.id,
                                   f'Ваше сообщение содержит больше количество символов = <b>{len(message.text)}</b>. Бот может обработать максимум 1000 символов. Сократите количество и попробуйте снова',
                                   parse_mode='HTML')
    else:
        print(message.content_type)
        await bot.send_message(message.chat.id,
                               'Ошибка - ваше сообщение должно содержать только текст\nНапишите текст сообщения для массовой рассылки:')


@dp.callback_query_handler(text='send_send_to_all')
async def callback_inline_send_send_all(call: CallbackQuery, state: FSMContext):
    logging.info(f'User({call.message.chat.id}) нажал на кнопку "✔ Отправить" всем пользователям')
    request = 0
    data = await state.get_data()
    if len(data) == 2:
        await bot_delete_messages(call.message, 5)
        await bot.delete_message(call.message.chat.id, call.message.message_id)
        await bot.send_message(call.message.chat.id, '<b>Массовая рассылка отправлена:</b>', parse_mode='HTML')
        users = await db.select_users()
        for i in users:
            try:
                try:
                    await bot.send_photo(i, data['photo_id'], caption=data['message_text_all'])
                    # await bot.send_document(i, data['document_id'])
                    # await bot.send_message(i, data['message_text_all'])
                except Exception as e:
                    await bot.send_document(i, data['document_id'], caption=data['message_text_all'])
                    logging.info(e)
                request += 1
                await asyncio.sleep(0.5)
                if request % 30 == 0:
                    await asyncio.sleep(2)
                    request = 0
            except Exception as e:
                logging.info(f'Наверно бот заблокирован {e}')

        await state.reset_state()
    else:
        await bot_delete_messages(call.message, 2)
        await bot.delete_message(call.message.chat.id, call.message.message_id)
        await bot.send_message(call.message.chat.id, '<b>Массовая рассылка отправлена:</b>', parse_mode='HTML')
        users = await db.select_users()
        for i in users:
            try:
                await bot.send_message(i, data['message_text_all'])
                request += 1
                await asyncio.sleep(0.5)
                if request % 30 == 0:
                    await asyncio.sleep(2)
                    request = 0
            except Exception as e:
                logging.info(f'Наверно бот заблокирован - {e}')
        await state.reset_state()


# Получение медиа файлы от пользователя для массовой рассылки
@dp.message_handler(content_types=ContentType.ANY, state=SendAll.message_photo)
async def message_send_photo(message: types.Message, state: FSMContext):
    if message.content_type == 'photo':
        await state.update_data(photo_id=message.photo[-1].file_id)
        logging.info(message.photo[-1].file_id)
        data = await state.get_data()
        message_txt = 'Ваше сообщение:\n' + data['message_text_all'] + '\n (*ВЫ УВЕРЕНЫ?*)'
        await bot.send_message(message.chat.id, message_txt, reply_markup=inline_keyboard_cancel_or_send())
        await state.reset_state(with_data=False)
    elif message.content_type == 'document':
        await state.update_data(document_id=message.document.file_id)
        logging.info(message.document.file_id)
        data = await state.get_data()
        message_txt = 'Ваше сообщение:\n' + data['message_text_all'] + '\n (*ВЫ УВЕРЕНЫ?*)'
        await bot.send_message(message.chat.id, message_txt, reply_markup=inline_keyboard_cancel_or_send())
        await state.reset_state(with_data=False)
    else:
        print(message.content_type)
        await bot.send_message(message.chat.id,
                               'Ошибка - отправьте картинку как "Фото", не как "Файл"')
