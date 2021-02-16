import logging
import asyncio
from aiogram.utils import exceptions
from aiogram import types
from aiogram.types import CallbackQuery, ContentType
from aiogram.dispatcher import FSMContext

from .admin_menu import admin_menu
from loader import dp, bot
from utils.delete_messages import bot_delete_messages

# Импорт клавиатур
from keyboards.inline import inline_keyboard_mass_mailing_send_or_attach, inline_keyboard_cancel_or_send

# Импортирование функций из БД контроллера
from utils import db_api as db

# Импорт стейтов
from states.admin import MassMailSending

from utils.misc import rate_limit


@dp.callback_query_handler(text='send_all', state=None)
async def callback_inline_send_all(call: CallbackQuery):
    logging.info(f'User({call.message.chat.id}) нажал на кнопку 📣 Рассылка - {call.data}')
    await call.message.answer('Напишите текст сообщения для массовой рассылки:')
    await MassMailSending.message_text.set()


@dp.message_handler(content_types=ContentType.ANY, state=MassMailSending.message_text)
async def message_send_text(message: types.Message, state: FSMContext):
    if message.content_type == 'text':
        if len(message.text) <= 4000:
            await state.update_data(message_text_all=message.text)
            message_txt = 'Ваше сообщение:\n' + message.text + '\n <i><u>ВЫ УВЕРЕНЫ?</u></i>'
            await bot.send_message(message.chat.id, message_txt,
                                   parse_mode='HTML',
                                   reply_markup=inline_keyboard_mass_mailing_send_or_attach())
            await state.reset_state(with_data=False)
        else:
            await bot.send_message(message.chat.id,
                                   f'Ваше сообщение содержит <b>{len(message.text)}</b> символов. Бот может обработать максимум 4000 символов. Сократите количество и попробуйте снова',
                                   parse_mode='HTML')
    else:
        print(message.content_type)
        await bot.send_message(message.chat.id,
                               'Ошибка - ваше сообщение должно содержать только текст\nНапишите текст сообщения для массовой рассылки:')


@dp.callback_query_handler(text='attach_pic_or_doc')
async def callback_inline_attach_pic_or_doc(call: CallbackQuery):
    logging.info(f'User({call.message.chat.id}) нажал на кнопку ➕ Добавить фото или документ - {call.data}')
    await bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id)  # Убирает инлайн клавиатуру
    await bot.send_message(call.message.chat.id, 'Прикрепите фото или файл к рассылке:')
    await MassMailSending.message_attached.set()


# Получение медиа файлы от пользователя для массовой рассылки
@dp.message_handler(content_types=ContentType.ANY, state=MassMailSending.message_attached)
async def message_send_photo(message: types.Message, state: FSMContext):
    if message.content_type == 'photo':
        await state.update_data(content_type="photo", file_id=message.photo[-1].file_id)
        # logging.info(message.photo[-1].file_id)
        data = await state.get_data()
        message_txt = 'Ваше сообщение:\n' + data['message_text_all'] + '\n <i><u>ВЫ УВЕРЕНЫ?</u></i>'
        await message.reply(message_txt, parse_mode='HTML', reply_markup=inline_keyboard_cancel_or_send())
        await state.reset_state(with_data=False)
    elif message.content_type == 'document':
        await state.update_data(content_type="document", file_id=message.document.file_id)
        # logging.info(message.document.file_id)
        data = await state.get_data()
        message_txt = 'Ваше сообщение:\n' + data['message_text_all'] + '\n <i><u>ВЫ УВЕРЕНЫ?</u></i>'
        await message.reply(message_txt, parse_mode='HTML', reply_markup=inline_keyboard_cancel_or_send())
        await state.reset_state(with_data=False)
    elif message.content_type == 'voice':
        await state.update_data(content_type="voice", file_id=message.voice.file_id)
        # logging.info(message.voice.file_id)
        data = await state.get_data()
        message_txt = 'Ваше сообщение:\n' + data['message_text_all'] + '\n <i><u>ВЫ УВЕРЕНЫ?</u></i>'
        await message.reply(message_txt, parse_mode='HTML', reply_markup=inline_keyboard_cancel_or_send())
        await state.reset_state(with_data=False)
    else:
        logging.info(f'Message type - {message.content_type}')
        await bot.send_message(message.chat.id,
                               'Ошибка - отправьте картинку как "Фото", не как "Файл"')


@dp.callback_query_handler(text='send_send_to_all')
async def callback_inline_send_send_all(call: CallbackQuery, state: FSMContext):
    logging.info(f'User({call.message.chat.id}) нажал на кнопку "✔ Отправить" всем пользователям - {call.data}')
    request = 0
    data = await state.get_data()
    if len(data) > 2:
        await bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id)  # Убирает инлайн клавиатуру
        await bot.send_message(call.message.chat.id,
                               '<b>🔄 Началась массовая рассылка, это может занять некоторое время.</b>',
                               parse_mode='HTML')
        await admin_menu(call.message)
        all_users = await db.select_users()
        for user in all_users:
            try:
                if data['content_type'] == "photo":
                    if len(data['message_text_all']) <= 1023:
                        await bot.send_photo(user, data['file_id'], caption=data['message_text_all'])
                    else:
                        await bot.send_message(user, data['message_text_all'], parse_mode='HTML')
                        await bot.send_photo(user, data['file_id'])
                elif data['content_type'] == "document":
                    if len(data['message_text_all']) <= 1023:
                        await bot.send_document(user, data['file_id'], caption=data['message_text_all'])
                    else:
                        await bot.send_message(user, data['message_text_all'], parse_mode='HTML')
                        await bot.send_document(user, data['file_id'])
                elif data['content_type'] == "voice":
                    if len(data['message_text_all']) <= 1023:
                        await bot.send_voice(user, data['file_id'], caption=data['message_text_all'])
                    else:
                        await bot.send_message(user, data['message_text_all'], parse_mode='HTML')
                        await bot.send_voice(user, data['file_id'])
                request += 1
                await asyncio.sleep(0.5)
                if request % 30 == 0:
                    await asyncio.sleep(2)
                    request = 0
            except Exception as e:
                pass
                # logging.info(f'Наверно бот заблокирован {e}')
        await bot.send_message(call.message.chat.id,
                               '<b>✅ Массовая рассылка закончила отправку сообщений.</b>',
                               parse_mode='HTML')
        await state.reset_state()
    else:
        await bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id)  # Убирает инлайн клавиатуру
        await bot.send_message(call.message.chat.id,
                               '<b>🔄 Началась массовая рассылка, это может занять некоторое время.</b>',
                               parse_mode='HTML')
        await admin_menu(call.message)
        all_users = await db.select_users()
        for user in all_users:
            try:
                await bot.send_message(user, data['message_text_all'], parse_mode='HTML')
                request += 1
                await asyncio.sleep(0.5)
                if request % 30 == 0:
                    await asyncio.sleep(2)
                    request = 0
            except Exception as e:
                # logging.info(f'Наверно бот заблокирован - {e}')
                pass
        await bot.send_message(call.message.chat.id,
                               '<b>✅ Массовая рассылка закончила отправку сообщений.</b>',
                               parse_mode='HTML')
        await state.reset_state()


@dp.callback_query_handler(text='cancel_massive_sending')
async def callback_inline_cancel(call: CallbackQuery, state: FSMContext):
    logging.info(f'User({call.message.chat.id}) нажал на кнопку ❌ Отмена - {call.data}')
    await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                text='✅ Массовая рассылка успешно отменена')
    await admin_menu(call.message)
    await state.reset_state()
