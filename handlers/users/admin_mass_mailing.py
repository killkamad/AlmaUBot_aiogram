import logging
import asyncio
from aiogram import types
from aiogram.types import CallbackQuery, ContentType, ChatActions
from aiogram.dispatcher import FSMContext

from .admin_menu import admin_menu
from loader import dp, bot

# Импорт клавиатур
from keyboards.inline import inline_keyboard_mass_mailing_send_or_attach, inline_keyboard_cancel_or_send, \
    inline_keyboard_cancel_mass_mailing

# Импортирование функций из БД контроллера
from utils import db_api as db

# Импорт стейтов
from states.admin import MassMailSending

import aiogram.utils.markdown as fmt
from utils.delete_inline_buttons import delete_inline_buttons_in_dialogue


@dp.callback_query_handler(text='send_all', state=None)
async def callback_inline_send_all(call: CallbackQuery):
    logging.info(f'User({call.message.chat.id}) нажал на кнопку 📣 Рассылка - {call.data}')
    await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                text='Напишите текст сообщения для массовой рассылки:',
                                reply_markup=inline_keyboard_cancel_mass_mailing())
    await MassMailSending.message_text.set()
    await call.answer()


@dp.message_handler(content_types=ContentType.ANY, state=MassMailSending.message_text)
async def message_send_text(message: types.Message, state: FSMContext):
    await delete_inline_buttons_in_dialogue(message)
    if message.content_type == 'text':
        if len(message.text) <= 4000:
            await state.update_data(message_text_all=fmt.quote_html(message.text))
            message_txt = f'• <b>Ваше сообщение:</b>\n' \
                          f'{fmt.quote_html(message.text)}\n\n' \
                          f'<i><u>Вы уверены?</u></i>'
            await bot.send_message(message.chat.id, message_txt,
                                   parse_mode='HTML',
                                   reply_markup=inline_keyboard_mass_mailing_send_or_attach())
            await state.reset_state(with_data=False)
        else:
            await bot.send_message(message.chat.id,
                                   f'Ваше сообщение содержит <b>{len(message.text)}</b> символов. Бот может обработать максимум 4000 символов. Сократите количество и попробуйте снова',
                                   parse_mode='HTML', reply_markup=inline_keyboard_cancel_mass_mailing())
    else:
        await bot.send_message(message.chat.id,
                               'Ошибка - ваше сообщение должно содержать только текст\nНапишите текст сообщения для массовой рассылки:',
                               reply_markup=inline_keyboard_cancel_mass_mailing())


@dp.callback_query_handler(text='attach_pic_or_doc')
async def callback_inline_attach_pic_or_doc(call: CallbackQuery):
    logging.info(f'User({call.message.chat.id}) нажал на кнопку ➕ Добавить фото или документ - {call.data}')
    await bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id)  # Убирает инлайн клавиатуру
    await bot.send_message(call.message.chat.id, 'Прикрепите к рассылке фото/документ/голосовое сообщение',
                           reply_markup=inline_keyboard_cancel_mass_mailing())
    await MassMailSending.message_attached.set()
    await call.answer()


# Получение медиа файлы от пользователя для массовой рассылки
@dp.message_handler(content_types=ContentType.ANY, state=MassMailSending.message_attached)
async def message_send_photo(message: types.Message, state: FSMContext):
    await delete_inline_buttons_in_dialogue(message)
    if message.content_type == 'photo':
        await state.update_data(content_type="photo", file_id=message.photo[-1].file_id)
        # logging.info(message.photo[-1].file_id)
        data = await state.get_data()
        message_txt = f'• <b>Ваше сообщение:</b>\n' \
                      f'{data["message_text_all"]}\n\n' \
                      f'<i><u>Вы уверены?</u></i>'
        await message.reply(message_txt, parse_mode='HTML', reply_markup=inline_keyboard_cancel_or_send())
        await state.reset_state(with_data=False)
    elif message.content_type == 'document':
        await state.update_data(content_type="document", file_id=message.document.file_id)
        # logging.info(message.document.file_id)
        data = await state.get_data()
        message_txt = f'• <b>Ваше сообщение:</b>\n' \
                      f'{data["message_text_all"]}\n\n' \
                      f'<i><u>Вы уверены?</u></i>'
        await message.reply(message_txt, parse_mode='HTML', reply_markup=inline_keyboard_cancel_or_send())
        await state.reset_state(with_data=False)
    elif message.content_type == 'voice':
        await state.update_data(content_type="voice", file_id=message.voice.file_id)
        # logging.info(message.voice.file_id)
        data = await state.get_data()
        message_txt = f'• <b>Ваше сообщение:</b>\n' \
                      f'{data["message_text_all"]}\n\n' \
                      f'<i><u>Вы уверены?</u></i>'
        await message.reply(message_txt, parse_mode='HTML', reply_markup=inline_keyboard_cancel_or_send())
        await state.reset_state(with_data=False)
    else:
        logging.info(f'Message type - {message.content_type}')
        await bot.send_message(message.chat.id,
                               'Ошибка, не допустимый формат данных\n'
                               'Бот поддерживает следующие типы данных:"Фото", "Документ", "Голосовое сообщение"',
                               reply_markup=inline_keyboard_cancel_mass_mailing())


@dp.callback_query_handler(text='send_send_to_all')
async def callback_inline_send_send_all(call: CallbackQuery, state: FSMContext):
    logging.info(f'User({call.message.chat.id}) нажал на кнопку "✔ Отправить" всем пользователям - {call.data}')
    request = 0
    data = await state.get_data()
    if len(data) > 2:
        await bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id)  # Убирает инлайн клавиатуру
        await bot.send_message(call.message.chat.id,
                               '<b>🔄 Началась массовая рассылка, это может занять некоторое время...</b>',
                               parse_mode='HTML')
        await admin_menu(call.message)
        all_users = await db.select_users()
        await bot.send_chat_action(call.message.chat.id, ChatActions.TYPING)
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
        await call.answer()
    else:
        await bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id)  # Убирает инлайн клавиатуру
        await bot.send_message(call.message.chat.id,
                               '<b>🔄 Началась массовая рассылка, это может занять некоторое время.</b>',
                               parse_mode='HTML')
        await admin_menu(call.message)
        all_users = await db.select_users()
        await bot.send_chat_action(call.message.chat.id, ChatActions.TYPING)
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
        await call.answer()


@dp.callback_query_handler(text=['cancel_massive_sending', 'cancel_mass_mailing'], state=['*'])
async def callback_inline_cancel(call: CallbackQuery, state: FSMContext):
    logging.info(f'User({call.message.chat.id}) нажал на кнопку ❌ Отмена - {call.data}')
    await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                text='✅ Массовая рассылка успешно отменена')
    await admin_menu(call.message)
    await state.reset_state()
    await call.answer()
