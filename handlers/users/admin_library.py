import logging

from aiogram.utils import exceptions
from aiogram import types
from aiogram.types import CallbackQuery, ContentType
from aiogram.dispatcher import FSMContext
from loader import dp, bot
from utils.delete_messages import bot_delete_messages
from utils import db_api as db

from keyboards.inline import inline_keyboard_library_first_page_admin, inline_keyboard_library_second_page_admin, \
    inline_keyboard_edit_button_content_library_or_cancel

from states.admin import EditButtonContentLibrary


@dp.callback_query_handler(text='lib_next_page')
async def library_admin_menu(call: CallbackQuery):
    logging.info(
        f'User({call.message.chat.id}) переход на вторую страницу админ меню Библиотеки, call.data - {call.data}')
    await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                text='Админ меню Библиотека:', reply_markup=inline_keyboard_library_second_page_admin())
    await call.answer()


@dp.callback_query_handler(text=['edit_lib_website', 'edit_lib_contacts', 'edit_lib_work_hours',
                                 'edit_lib_courses', 'edit_lib_idcard', 'edit_lib_rules',
                                 'edit_lib_rights', 'edit_lib_unallow', 'edit_lib_respons'],
                           state=None)
async def edit_button_content_library(call: CallbackQuery, state: FSMContext):
    logging.info(f'User({call.message.chat.id}) нажал на кнопку {call.data}')
    if call.data == 'edit_lib_website':
        await call.message.answer('Напишите новый текст для кнопки 🌐 Вебсайт:\n'
                                  'Для отмены - /cancel')
        await state.update_data(button_name='🌐 Вебсайт')
    elif call.data == 'edit_lib_contacts':
        await call.message.answer('Напишите новый текст для кнопки ☎ Контакты:\n'
                                  'Для отмены - /cancel')
        await state.update_data(button_name='☎ Контакты')
    elif call.data == 'edit_lib_work_hours':
        await call.message.answer('Напишите новый текст для кнопки 🕐 Время работы:\n'
                                  'Для отмены - /cancel')
        await state.update_data(button_name='🕐 Время работы')
    elif call.data == 'edit_lib_courses':
        await call.message.answer('Напишите новый текст для кнопки 🎓 Онлайн курсы:\n'
                                  'Для отмены - /cancel')
        await state.update_data(button_name='🎓 Онлайн курсы')
    elif call.data == 'edit_lib_idcard':
        await call.message.answer('Напишите новый текст для кнопки 💳 Потерял(a) ID-карту:\n'
                                  'Для отмены - /cancel')
        await state.update_data(button_name='💳 Потерял(a) ID-карту')
    elif call.data == 'edit_lib_rules':
        await call.message.answer('Напишите новый текст для кнопки ⚠ Правила:\n'
                                  'Для отмены - /cancel')
        await state.update_data(button_name='⚠ Правила')
    elif call.data == 'edit_lib_rights':
        await call.message.answer('Напишите новый текст для кнопки 📰 Права читателя:\n'
                                  'Для отмены - /cancel')
        await state.update_data(button_name='📰 Права читателя')
    elif call.data == 'edit_lib_unallow':
        await call.message.answer('Напишите новый текст для кнопки 🚫 Что не разрешается:\n'
                                  'Для отмены - /cancel')
        await state.update_data(button_name='🚫 Что не разрешается')
    elif call.data == 'edit_lib_respons':
        await call.message.answer('Напишите новый текст для кнопки ⛔ Ответственность за нарушения:\n'
                                  'Для отмены - /cancel')
        await state.update_data(button_name='⛔ Ответственность за нарушения')
    await EditButtonContentLibrary.button_content.set()
    await call.answer()


@dp.message_handler(content_types=ContentType.ANY, state=EditButtonContentLibrary.button_content)
async def edit_button_content_library_text(message: types.Message, state: FSMContext):
    if message.content_type == 'text':
        if len(message.text) <= 4000:
            await state.update_data(button_content=message.text)
            await message.reply('✅ Новый текст получен.\n'
                                'Подтвердите изменение',
                                reply_markup=inline_keyboard_edit_button_content_library_or_cancel())
            await EditButtonContentLibrary.confirm.set()
        else:
            await message.reply(
                f'Ваше сообщение содержит больше количество символов = <b>{len(message.text)}</b>. Ограничение в 4000 символов. Сократите количество символов и попробуйте снова',
                parse_mode='HTML')
    else:
        await message.reply('Ошибка - ваше сообщение должно содержать только текст\n'
                            'Повторите отправку сообщения')


@dp.callback_query_handler(text='edit_lib_button', state=EditButtonContentLibrary.confirm)
async def edit_button_content_library_confirm(call: CallbackQuery, state: FSMContext):
    logging.info(f'User({call.message.chat.id}) нажал на кнопку {call.data}')
    try:
        data = await state.get_data()
        await db.edit_library_menu_button(call.message.chat.id, data['button_name'], data['button_content'])
        await bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id)
        await bot.send_message(call.message.chat.id,
                               f'✅ Успешно изменен контент для кнопки - {data["button_name"]} для раздела Библиотека')
        await bot.send_message(chat_id=call.message.chat.id,
                               text='Админ меню Библиотека:', reply_markup=inline_keyboard_library_first_page_admin())
        await state.reset_state()
        await call.answer()
    except Exception as error:
        logging.info(f'Error - {error}')
        await bot.send_message(call.message.chat.id, f'Произошла ошибка - {error}')


@dp.callback_query_handler(text='cancel_edit_lib_button', state=EditButtonContentLibrary.confirm)
async def edit_button_content_library_cancel(call: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    logging.info(f'User({call.message.chat.id}) нажал на кнопку {call.data}')
    await bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id)  # Убирает инлайн клавиатуру
    await bot.send_message(call.message.chat.id,
                           f'❌ Отмена изменения контента для кнопки - {data["button_name"]} для раздела Библиотека')
    await bot.send_message(chat_id=call.message.chat.id,
                           text='Админ меню Библиотека:', reply_markup=inline_keyboard_library_first_page_admin())
    await state.reset_state()
    await call.answer()
