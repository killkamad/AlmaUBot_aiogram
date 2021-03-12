import logging

from aiogram import types
from aiogram.types import CallbackQuery, ContentType
from aiogram.dispatcher import FSMContext
from loader import dp, bot
from utils import db_api as db
from utils.delete_inline_buttons import delete_inline_buttons_in_dialogue

from keyboards.inline import inline_keyboard_library_first_page_admin, inline_keyboard_library_second_page_admin, \
    inline_keyboard_edit_button_content_library_or_cancel, inline_keyboard_cancel_edit_library_button, \
    inline_keyboard_library_res_admin, inline_keyboard_library_res_edit_admin, cancel_or_add_lib_resource, \
    inline_keyboard_del_lib_res, lib_res_delete_callback, cancel_or_delete_lib_resource, cancel_edit_lib_res

from states.admin import EditButtonContentLibrary, AddLibraryResource, DeleteLibraryResource


@dp.callback_query_handler(text='lib_next_page')
async def library_admin_menu(call: CallbackQuery):
    logging.info(
        f'User({call.message.chat.id}) переход на вторую страницу админ меню Библиотеки, call.data - {call.data}')
    await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                text='Админ меню Библиотека:', reply_markup=inline_keyboard_library_second_page_admin())
    await call.answer()


# -------------------- Добавление электронного ресурса --------------------
@dp.callback_query_handler(text='edit_lib_resource', state=['*'])
async def edit_library_resources(call: CallbackQuery, state: FSMContext):
    logging.info(f'User({call.message.chat.id}) нажал на кнопку {call.data}')
    await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                text='Выберите электронные ресурсы для изменения:',
                                reply_markup=inline_keyboard_library_res_admin())
    await state.reset_state()
    await call.answer()


@dp.callback_query_handler(text='cancel_edit_lib_resource', state=['*'])
async def callback_inlint_resource_cancel(call: CallbackQuery, state: FSMContext):
    logging.info(f'User({call.message.chat.id}) отменил добавление ресурса call.data - {call.data}')
    data = await state.get_data()
    lib_type = data['lib_type']
    await state.reset_state()
    await state.update_data(lib_type=lib_type)
    await bot.delete_message(call.message.chat.id, call.message.message_id)
    await call.message.answer('❌ Добавление ресурса было отменено\n',
                              parse_mode='HTML',
                              reply_markup=inline_keyboard_library_res_edit_admin())
    await AddLibraryResource.lib_type.set()
    await call.answer()


@dp.callback_query_handler(
    text=['edit_library_registration', 'edit_library_free_kz', 'edit_library_free_foreign', 'edit_library_online_libs'])
async def edit_library_free_libs(call: CallbackQuery, state: FSMContext):
    logging.info(f'User({call.message.chat.id}) нажал на кнопку {call.data}')
    if call.data == 'edit_library_registration':
        await state.update_data(lib_type='reg')
        await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                    text='📕 Лицензионные Базы Данных:',
                                    reply_markup=inline_keyboard_library_res_edit_admin())
    elif call.data == 'edit_library_free_kz':
        await state.update_data(lib_type='kz')
        await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                    text='📗 Базы данных свободного доступа(Казахстанские):',
                                    reply_markup=inline_keyboard_library_res_edit_admin())
    elif call.data == 'edit_library_free_foreign':
        await state.update_data(lib_type='foreign')
        await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                    text='📗 Базы данных свободного доступа(Зарубежные):',
                                    reply_markup=inline_keyboard_library_res_edit_admin())
    elif call.data == 'edit_library_online_libs':
        await state.update_data(lib_type='online')
        await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                    text='📗 Онлайн библиотеки:',
                                    reply_markup=inline_keyboard_library_res_edit_admin())
    await AddLibraryResource.lib_type.set()
    await call.answer()


@dp.callback_query_handler(text='add_resource', state=AddLibraryResource.lib_type)
async def add_library_resource(call: CallbackQuery, state: FSMContext):
    logging.info(f'User({call.message.chat.id}) нажал на кнопку {call.data}')
    await bot.delete_message(call.message.chat.id, call.message.message_id)
    await bot.send_message(call.message.chat.id, 'Напишите название электронного ресурса:',
                           reply_markup=cancel_edit_lib_res())
    await AddLibraryResource.button_name.set()
    await call.answer()


@dp.message_handler(content_types=ContentType.ANY, state=AddLibraryResource.button_name)
async def add_library_resource(message: types.Message, state: FSMContext):
    await delete_inline_buttons_in_dialogue(message)
    async with state.proxy() as data:
        data['button_name'] = message.text
    await message.reply('Введите ссылку на электронный ресурс:', reply_markup=cancel_edit_lib_res())
    await AddLibraryResource.lib_url.set()


@dp.message_handler(content_types=ContentType.ANY, state=AddLibraryResource.lib_url)
async def add_library_resource(message: types.Message, state: FSMContext):
    await delete_inline_buttons_in_dialogue(message)
    async with state.proxy() as data:
        data['lib_url'] = message.text
    data = await state.get_data()
    text = f'{data["button_name"]}, '
    await bot.send_message(chat_id=message.chat.id,
                           text=f'Название ресурса: <b>{data["button_name"]}</b>\n'
                                f'Ссылка на ресурс: {data["lib_url"]}\n',
                           parse_mode="HTML",
                           reply_markup=cancel_or_add_lib_resource())


@dp.callback_query_handler(text='add_lib_resource', state=['*'])
async def add_lib_resource_to_db(call: CallbackQuery, state: FSMContext):
    try:
        data = await state.get_data()
        await db.add_lib_resource(call.message.chat.id, data["button_name"], data["lib_url"], data["lib_type"])
        try:
            await bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id)
            await bot.send_message(call.message.chat.id, 'Ресурс успешно добавлен',
                                   reply_markup=inline_keyboard_library_res_admin())
        except:
            await bot.send_message(call.message.chat.id, 'Ресурс успешно добавлен',
                                   reply_markup=inline_keyboard_library_res_admin())
        await state.reset_state()
        await call.answer()
    except Exception as e:
        await call.message.answer(f'Ошибка ресурс не добавлен, (Ошибка - {e})')
        print(e)


@dp.callback_query_handler(text='cancel_add_lib_resource', state=['*'])
async def add_lib_resource_to_db(call: CallbackQuery, state: FSMContext):
    logging.info(f'User({call.message.chat.id}) отменил добавление ресурса call.data - {call.data}')
    data = await state.get_data()
    lib_type = data['lib_type']
    await state.reset_state()
    await state.update_data(lib_type=lib_type)
    await bot.delete_message(call.message.chat.id, call.message.message_id)
    await call.message.answer('❌ Добавление ресурса было отменено',
                              parse_mode='HTML',
                              reply_markup=inline_keyboard_library_res_edit_admin())
    await AddLibraryResource.lib_type.set()
    await call.answer()


# -------------------- Конец добавление электронного ресурса --------------------


# --------------------- Удаление электронного ресурса ---------------------
@dp.callback_query_handler(text='delete_resource', state=AddLibraryResource.lib_type)
async def del_library_resource(call: CallbackQuery, state: FSMContext):
    logging.info(f'User({call.message.chat.id}) нажал на кнопку {call.data}')
    data = await state.get_data()
    await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                text='Выберите ресурс для удаления:',
                                reply_markup=await inline_keyboard_del_lib_res(data["lib_type"]))
    await call.answer()


@dp.callback_query_handler(text='back_del_lib_resource', state=['*'])
async def callback_inlint_resource_cancel(call: CallbackQuery, state: FSMContext):
    logging.info(f'User({call.message.chat.id}) отменил добавление ресурса call.data - {call.data}')
    await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                text='Возврат в изменение электронных ресурсов',
                                reply_markup=inline_keyboard_library_res_edit_admin())
    await call.answer()


@dp.callback_query_handler(lib_res_delete_callback.filter(), state=['*'])
async def del_library_resource(call: CallbackQuery, callback_data: dict, state: FSMContext):
    logging.info(f'call = {call.data}')
    data = callback_data.get('id')
    await state.update_data(id=data)
    await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                text=f'Вы действительно хотите удалить данный ресурс?',
                                reply_markup=cancel_or_delete_lib_resource())
    await DeleteLibraryResource.confirm_delete.set()
    await call.answer()


@dp.callback_query_handler(text='del_lib_resource', state=DeleteLibraryResource.confirm_delete)
async def del_library_resource(call: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    try:
        await db.delete_library_resource(data["id"])
        await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                    text=f'Ресурс успешно удален из базы данных\n',
                                    parse_mode='HTML',
                                    reply_markup=inline_keyboard_library_res_admin())
        await state.reset_state()
        logging.info(f'User({call.message.chat.id}) удалил ресурс {data["id"]}')
        await call.answer()
    except Exception as e:
        await call.message.answer(f'Ошибка справка не удалена, (Ошибка - {e})')
        logging.info(f'Ошибка - {e}')


@dp.callback_query_handler(text_contains='cancel_del_lib_resource', state=DeleteLibraryResource.confirm_delete)
async def callback_inlint_del_resource_cancel(call: CallbackQuery, state: FSMContext):
    logging.info(f'User({call.message.chat.id}) отменил удаление ресурса call.data - {call.data}')
    data = await state.get_data()
    lib_type = data['lib_type']
    await state.reset_state()
    await state.update_data(lib_type=lib_type)
    await bot.delete_message(call.message.chat.id, call.message.message_id)
    await call.message.answer('❌ Удаление ресурса было отменено',
                              parse_mode='HTML',
                              reply_markup=inline_keyboard_library_res_edit_admin())
    await AddLibraryResource.lib_type.set()
    await call.answer()


# --------------------- Конец удаление электронного ресурса ---------------------


@dp.callback_query_handler(text=['edit_lib_website', 'edit_lib_contacts', 'edit_lib_work_hours',
                                 'edit_lib_courses', 'edit_lib_idcard', 'edit_lib_rules',
                                 'edit_lib_rights', 'edit_lib_unallow', 'edit_lib_respons'],
                           state=None)
async def edit_button_content_library(call: CallbackQuery, state: FSMContext):
    logging.info(f'User({call.message.chat.id}) нажал на кнопку {call.data}')
    if call.data == 'edit_lib_website':
        await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                    text='Напишите новый текст для кнопки 🌐 Вебсайт:',
                                    reply_markup=inline_keyboard_cancel_edit_library_button())
        await state.update_data(button_name='🌐 Вебсайт')
    elif call.data == 'edit_lib_contacts':
        await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                    text='Напишите новый текст для кнопки ☎ Контакты:',
                                    reply_markup=inline_keyboard_cancel_edit_library_button())
        await state.update_data(button_name='☎ Контакты')
    elif call.data == 'edit_lib_work_hours':
        await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                    text='Напишите новый текст для кнопки 🕐 Время работы:',
                                    reply_markup=inline_keyboard_cancel_edit_library_button())
        await state.update_data(button_name='🕐 Время работы')
    elif call.data == 'edit_lib_courses':
        await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                    text='Напишите новый текст для кнопки 🎓 Онлайн курсы:',
                                    reply_markup=inline_keyboard_cancel_edit_library_button())
        await state.update_data(button_name='🎓 Онлайн курсы')
    elif call.data == 'edit_lib_idcard':
        await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                    text='Напишите новый текст для кнопки 💳 Потерял(a) ID-карту:',
                                    reply_markup=inline_keyboard_cancel_edit_library_button())
        await state.update_data(button_name='💳 Потерял(a) ID-карту')
    elif call.data == 'edit_lib_rules':
        await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                    text='Напишите новый текст для кнопки ⚠ Правила:',
                                    reply_markup=inline_keyboard_cancel_edit_library_button())
        await state.update_data(button_name='⚠ Правила')
    elif call.data == 'edit_lib_rights':
        await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                    text='Напишите новый текст для кнопки 📰 Права читателя:',
                                    reply_markup=inline_keyboard_cancel_edit_library_button())
        await state.update_data(button_name='📰 Права читателя')
    elif call.data == 'edit_lib_unallow':
        await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                    text='Напишите новый текст для кнопки 🚫 Что не разрешается:',
                                    reply_markup=inline_keyboard_cancel_edit_library_button())
        await state.update_data(button_name='🚫 Что не разрешается')
    elif call.data == 'edit_lib_respons':
        await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                    text='Напишите новый текст для кнопки ⛔ Ответственность за нарушения:',
                                    reply_markup=inline_keyboard_cancel_edit_library_button())
        await state.update_data(button_name='⛔ Ответственность за нарушения')
    await EditButtonContentLibrary.button_content.set()
    await call.answer()


@dp.message_handler(content_types=ContentType.ANY, state=EditButtonContentLibrary.button_content)
async def edit_button_content_library_text(message: types.Message, state: FSMContext):
    await delete_inline_buttons_in_dialogue(message)
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
                            'Повторите отправку сообщения',
                            reply_markup=inline_keyboard_cancel_edit_library_button())


@dp.callback_query_handler(text='cancel_edit_lib_button', state=['*'])
async def edit_button_content_library_cancel(call: CallbackQuery, state: FSMContext):
    logging.info(f'User({call.message.chat.id}) нажал на кнопку {call.data}')
    try:
        data = await state.get_data()
        # await bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id)  # Убирает инлайн клавиатуру
        await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                    text=f'❌ Отмена изменения контента кнопки - "{data["button_name"]}" для раздела Библиотека\n'
                                         'Возврат в Админ меню Библиотека:',
                                    reply_markup=inline_keyboard_library_first_page_admin())
        await state.reset_state()
        await call.answer()
    except Exception as error:
        logging.info(f'Error - {error}')
        await bot.send_message(call.message.chat.id, f'Произошла ошибка - {error}')


@dp.callback_query_handler(text='edit_lib_content', state=EditButtonContentLibrary.confirm)
async def edit_button_content_library_confirm(call: CallbackQuery, state: FSMContext):
    logging.info(f'User({call.message.chat.id}) нажал на кнопку {call.data}')
    try:
        data = await state.get_data()
        await db.edit_library_menu_button(call.message.chat.id, data['button_name'], data['button_content'])
        # await bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id)
        await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                    text=f'✅ Успешно изменен контент для кнопки - "{data["button_name"]}" для раздела Библиотека\n'
                                         'Админ меню Библиотека:',
                                    reply_markup=inline_keyboard_library_first_page_admin())
        await state.reset_state()
        await call.answer()
    except Exception as error:
        logging.info(f'Error - {error}')
        await bot.send_message(call.message.chat.id, f'Произошла ошибка - {error}')


@dp.callback_query_handler(text='cancel_edit_lib_content', state=EditButtonContentLibrary.confirm)
async def edit_button_content_library_cancel(call: CallbackQuery, state: FSMContext):
    logging.info(f'User({call.message.chat.id}) нажал на кнопку {call.data}')
    try:
        data = await state.get_data()
        # await bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id)  # Убирает инлайн клавиатуру
        await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                    text=f'❌ Отмена изменения контента для кнопки - "{data["button_name"]}" для раздела Библиотека\n'
                                         'Возврат в Админ меню Библиотека:',
                                    reply_markup=inline_keyboard_library_first_page_admin())
        await state.reset_state()
        await call.answer()
    except Exception as error:
        logging.info(f'Error - {error}')
        await bot.send_message(call.message.chat.id, f'Произошла ошибка - {error}')
