import logging

from aiogram import types
from aiogram.types import CallbackQuery, ContentType
from aiogram.dispatcher import FSMContext
from loader import dp, bot
from utils import db_api as db
from utils.delete_inline_buttons import delete_inline_buttons_in_dialogue
from states.admin import AddCertificateInstruction, EditButtonContentCertificate, DeleteCertificateInstruction, \
    AddDocumentCertificate

from .admin_menu import certificate_admin_menu

from keyboards.inline import cancel_edit_instruction, cancel_add_instruction_or_add_file, \
    inline_keyboard_certificate_admin, \
    inline_keyboard_upd_instruction, inline_keyboard_del_instruction, cancel_or_update_instruction, \
    cancel_or_delete_instruction, cancel_or_add_instruction, inline_keyboard_add_doc_instruction, \
    cancel_add_doc_instruction, cancel_or_add_doc_instruction

from keyboards.inline.callback_datas import instruction_update_callback, instruction_delete_callback, \
    instruction_add_doc_callback


@dp.callback_query_handler(text='send_instruction_bot')
async def callback_inline_send_certificate_bot(call: CallbackQuery):
    logging.info(f'User({call.message.chat.id}) нажал на кнопку {call.data}')
    await bot.delete_message(call.message.chat.id, call.message.message_id)
    await bot.send_message(call.message.chat.id, 'Напишите наименование инструкции:',
                           reply_markup=cancel_edit_instruction())
    await AddCertificateInstruction.button_name.set()
    await call.answer()


@dp.message_handler(content_types=ContentType.ANY, state=AddCertificateInstruction.button_name)
async def add_library_resource(message: types.Message, state: FSMContext):
    await delete_inline_buttons_in_dialogue(message)
    async with state.proxy() as data:
        data['button_name'] = message.text
    await message.reply('Напишите тест инструкции:', reply_markup=cancel_edit_instruction())
    await AddCertificateInstruction.button_content.set()


@dp.message_handler(content_types=ContentType.ANY, state=AddCertificateInstruction.button_content)
async def add_library_resource(message: types.Message, state: FSMContext):
    await delete_inline_buttons_in_dialogue(message)
    async with state.proxy() as data:
        data['button_content'] = message.text
    data = await state.get_data()
    text = f'Наименование инструкции: <b>{data["button_name"]}</b>\n' \
           f'Инструкция: {data["button_content"]}\n'
    await bot.send_message(chat_id=message.chat.id,
                           text=text,
                           parse_mode="HTML",
                           reply_markup=cancel_add_instruction_or_add_file())


@dp.callback_query_handler(text='add_document_certificate', state=AddCertificateInstruction.button_content)
async def add_file_instruction(call: CallbackQuery, state: FSMContext):
    await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                text="Отправьте документ который нужно прикрепить к инструкции:",
                                reply_markup=cancel_edit_instruction())
    await AddCertificateInstruction.button_file.set()


@dp.message_handler(content_types=ContentType.ANY, state=AddCertificateInstruction.button_file)
async def get_file_instruction(message: types.Message, state: FSMContext):
    await delete_inline_buttons_in_dialogue(message)
    if message.content_type == 'document':
        async with state.proxy() as data:
            data['button_file'] = message.document.file_id
        data = await state.get_data()
        text = f'Наименование инструкции: <b>{data["button_name"]}</b>\n' \
               f'Инструкция: {data["button_content"]}\n'
        data = await state.get_data()
        await message.answer(text)
        await bot.send_document(message.chat.id, data["button_file"], reply_markup=cancel_or_add_instruction())
        await state.reset_state(with_data=False)
    else:
        await message.reply('Вы должны отправить документ.\n'
                            'Попробуйте снова')


@dp.callback_query_handler(text='send_instruction', state=['*'])
async def add_instruction_to_db(call: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    try:
        if len(data) > 2:
            await db.add_instruction_with_document(call.message.chat.id, data["button_name"], data["button_content"],
                                                   data["button_file"])
            await bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id)
            await bot.send_message(call.message.chat.id, 'Инструкция успешно добавлена',
                                   reply_markup=inline_keyboard_certificate_admin())
        else:
            await db.add_instruction(call.message.chat.id, data["button_name"], data["button_content"])
            await bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id)
            await bot.send_message(call.message.chat.id, 'Инструкция успешно добавлена',
                                   reply_markup=inline_keyboard_certificate_admin())
        await state.reset_state()
        await call.answer()
    except Exception as e:
        await call.message.answer(f'Ошибка инструкция не добавлена, (Ошибка - {e})')
        logging.info(f'(Ошибка - {e})')


@dp.callback_query_handler(text_contains='cancel_instruction', state=['*'])
async def callback_inline_cancel_certificate(call: CallbackQuery, state: FSMContext):
    logging.info(f'User({call.message.chat.id}) отменил отправку инструкции call.data - {call.data}')
    # await bot_delete_messages(call.message, 4)
    await bot.delete_message(call.message.chat.id, call.message.message_id)
    await call.message.answer('<b>Отправка инструкции отменена</b>\n'
                              'Возврат в Админ меню Справки:',
                              parse_mode='HTML',
                              reply_markup=inline_keyboard_certificate_admin())
    await state.reset_state()
    await call.answer()


@dp.callback_query_handler(text='cancel_edit_instruction', state=['*'])
async def add_instruction_to_db(call: CallbackQuery, state: FSMContext):
    logging.info(f'User({call.message.chat.id}) отменил изменение инструкции call.data - {call.data}')
    data = await state.get_data()
    await state.reset_state()
    await bot.delete_message(call.message.chat.id, call.message.message_id)
    await call.message.answer('❌ Добавление инструкции было отменено',
                              parse_mode='HTML',
                              reply_markup=inline_keyboard_certificate_admin())
    await call.answer()


@dp.callback_query_handler(text='cancel_update_step_cert')
async def callback_inline_cancel_update_certificate_bot(call: CallbackQuery, state: FSMContext):
    logging.info(f'User({call.message.chat.id}) нажал на кнопку {call.data}')
    await certificate_admin_menu(call)
    await state.reset_state()
    await call.answer()


@dp.callback_query_handler(text='update_instruction_bot', state=None)
async def callback_instruction_button(call: CallbackQuery):
    await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                text='Выберите инструкцию для изменения:',
                                reply_markup=await inline_keyboard_upd_instruction())
    await call.answer()


@dp.callback_query_handler(text='add_doc_instruction_bot', state=None)
async def add_doc_instruction_bot(call: CallbackQuery):
    await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                text='Выберите инструкцию к которой нужно прикрепить документ:',
                                reply_markup=await inline_keyboard_add_doc_instruction())
    await call.answer()


@dp.callback_query_handler(instruction_update_callback.filter())
async def callback_inline(call: CallbackQuery, callback_data: dict, state: FSMContext):
    logging.info(f'call = {call.data}')
    id = callback_data.get('id')
    await state.update_data(button_name=id)
    await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                text='Напишите инструкцию:', reply_markup=cancel_edit_instruction())
    await EditButtonContentCertificate.button_content.set()
    await call.answer()


@dp.message_handler(content_types=ContentType.ANY, state=EditButtonContentCertificate.button_content)
async def edit_button_content_instruction(message: types.Message, state: FSMContext):
    await delete_inline_buttons_in_dialogue(message)
    if message.content_type == 'text':
        if len(message.text) <= 4000:
            await state.update_data(button_content=message.text)
            await message.reply('✅ Новый текст получен.\n\n'
                                '<i><u>Подтвердите изменение</u></i>',
                                reply_markup=cancel_or_update_instruction(),
                                parse_mode="HTML")
            await EditButtonContentCertificate.confirm.set()
        else:
            await message.reply(
                f'Ваше сообщение содержит больше количество символов = <b>{len(message.text)}</b>. Ограничение в 4000 символов. Сократите количество символов и попробуйте снова',
                parse_mode='HTML')
    else:
        await message.reply('Ошибка - ваше сообщение должно содержать только текст\n'
                            'Повторите отправку сообщения',
                            reply_markup=cancel_or_update_instruction())


@dp.callback_query_handler(text='update_instruction_button', state=EditButtonContentCertificate.confirm)
async def callback_inline_upd_instruction(call: CallbackQuery, state: FSMContext):
    try:
        data = await state.get_data()
        await db.update_instruction_data(data["button_name"], data['button_content'])
        logging.info(f'User({call.message.chat.id}) обновил инструкции для {data["button_name"]}')
        try:
            await bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id)
            await bot.send_message(call.message.chat.id,
                                   f'Инструкция успешно обновлена\n'
                                   f'Выберите инструкцию для изменения',
                                   parse_mode='HTML',
                                   reply_markup=await inline_keyboard_upd_instruction())
        except Exception as error:
            logging.error(f'Произошла ошибка - {error}')
            await bot.send_message(call.message.chat.id, f'Произошла ошибка - {error}')
        await state.reset_state()
        await call.answer()
    except Exception as e:
        await call.message.answer(f'Ошибка инструкция не обновлена, (Ошибка - {e})')
        logging.info(f'Ошибка - {e}')


@dp.callback_query_handler(text_contains='cancel_update_instruction', state=EditButtonContentCertificate.confirm)
async def callback_inline_cancel_update_certificate(call: CallbackQuery, state: FSMContext):
    logging.info(f'User({call.message.chat.id}) отменил обновления инструкции call.data - {call.data}')
    # await bot_delete_messages(call.message, 2)
    await bot.delete_message(call.message.chat.id, call.message.message_id)
    await call.message.answer('<b>Обновление | Изменение отменено</b>\n'
                              'Возврат в Админ меню Справки:',
                              parse_mode='HTML',
                              reply_markup=inline_keyboard_certificate_admin())
    await state.reset_state()
    await call.answer()


@dp.callback_query_handler(text='delete_instruction_bot', state=None)
async def callback_instruction_button(call: CallbackQuery):
    await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                text='Выберите инструкцию для удаления:',
                                reply_markup=await inline_keyboard_del_instruction())
    await call.answer()


@dp.callback_query_handler(text='cancel_delete_step_cert')
async def callback_inline_cancel_delete_certificate_bot(call: CallbackQuery, state: FSMContext):
    logging.info(f'User({call.message.chat.id}) нажал на кнопку {call.data}')
    await certificate_admin_menu(call)
    await state.reset_state()
    await call.answer()


@dp.callback_query_handler(instruction_delete_callback.filter(), state=['*'])
async def callback_inline(call: CallbackQuery, callback_data: dict, state: FSMContext):
    logging.info(f'call = {call.data}')
    id = callback_data.get('id')
    await state.update_data(button_name=id)
    await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                text=f'Вы точно уверены, что хотите удалить эту инструкцию?:',
                                parse_mode='HTML', reply_markup=cancel_or_delete_instruction())
    await DeleteCertificateInstruction.confirm_delete.set()
    await call.answer()


@dp.callback_query_handler(text='delete_instruction_button', state=DeleteCertificateInstruction.confirm_delete)
async def callback_inline_send_certificate(call: CallbackQuery, state: FSMContext):
    try:
        data = await state.get_data()
        await db.delete_instruction_button(data["button_name"])
        await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                    text=f'Инструкция успешно удалена из базы данных\n'
                                         'Выберите инструкция для удаления',
                                    parse_mode='HTML',
                                    reply_markup=await inline_keyboard_del_instruction())
        await state.reset_state(with_data=False)
        logging.info(f'User({call.message.chat.id}) удалил инструкцию для {data["button_name"]}')
        await call.answer()
    except Exception as e:
        await call.message.answer(f'Ошибка инструкция не удалена, (Ошибка - {e})')
        logging.info(f'Ошибка - {e}')


@dp.callback_query_handler(text_contains='cancel_delete_instruction', state=DeleteCertificateInstruction.confirm_delete)
async def callback_inline_cancel_delete_certificate(call: CallbackQuery, state: FSMContext):
    logging.info(f'User({call.message.chat.id}) отменил удаление инструкции call.data - {call.data}')
    await bot.delete_message(call.message.chat.id, call.message.message_id)
    await call.message.answer('<b>Удаление отменено</b>\n'
                              'Возврат в Админ меню Справки:',
                              parse_mode='HTML',
                              reply_markup=inline_keyboard_certificate_admin())
    await state.reset_state()
    await call.answer()


@dp.callback_query_handler(instruction_add_doc_callback.filter())
async def callback_inline_instruction_add_doc(call: CallbackQuery, callback_data: dict, state: FSMContext):
    logging.info(f'call = {call.data}')
    id = callback_data.get('id')
    await state.update_data(button_id=id)
    await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                text="Отправьте документ который нужно прикрепить к инструкции:",
                                parse_mode='HTML',
                                reply_markup=cancel_add_doc_instruction())
    await AddDocumentCertificate.button_file.set()
    await call.answer()


@dp.message_handler(content_types=ContentType.ANY, state=AddDocumentCertificate.button_file)
async def callback_inline_instruction_get_doc(message: types.Message, state: FSMContext):
    await delete_inline_buttons_in_dialogue(message)
    if message.content_type == 'document':
        await state.update_data(button_file=message.document.file_id)
        data = await state.get_data()
        data_db = await db.select_instruction_all(data['button_id'])
        text = f'Наименование инструкции к которой будет прикреплен документ: <b>{data_db["button_name"]}</b>\n'
        data = await state.get_data()
        await message.answer(text)
        await bot.send_document(message.chat.id, data["button_file"], reply_markup=cancel_or_add_doc_instruction())
        await state.reset_state(with_data=False)
    else:
        await message.reply('Вы должны отправить документ.\n'
                            'Попробуйте снова')


@dp.callback_query_handler(text='add_doc_instruction', state=['*'])
async def add_instruction_to_db(call: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    try:
        await db.add_instruction_document(data["button_id"], data["button_file"])
        await bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id)
        await bot.send_message(call.message.chat.id, 'К инструкции успешно прикреплен документ!',
                               reply_markup=inline_keyboard_certificate_admin())
        await state.reset_state()
        await call.answer()
    except Exception as e:
        await call.message.answer(f'Ошибка инструкция не добавлена, (Ошибка - {e})')
        logging.info(f'(Ошибка - {e})')


@dp.callback_query_handler(text='cancel_add_doc_instruction', state=['*'])
async def add_instruction_to_db(call: CallbackQuery, state: FSMContext):
    logging.info(f'User({call.message.chat.id}) отменил изменение инструкции call.data - {call.data}')
    await state.reset_state()
    await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                text='❌ Добавление документа к инструкции было отменено',
                                parse_mode='HTML',
                                reply_markup=inline_keyboard_certificate_admin())
    await call.answer()
