import logging
from aiogram.utils import exceptions
from aiogram import types
from aiogram.types import CallbackQuery, ContentType, ChatActions
from aiogram.dispatcher import FSMContext
from loader import dp, bot

# Импорт клавиатур
from keyboards.inline import almau_shop_faq_delete_callback, almau_shop_faq_edit_callback, \
    inline_keyboard_almau_shop_admin, \
    inline_keyboard_add_almaushop_faq_or_cancel, inline_keyboard_delete_faq_almaushop, cancel_or_delete_faq_almau_shop, \
    inline_keyboard_edit_faq_almaushop, inline_keyboard_edit_faq_almaushop_choice, \
    inline_keyboard_edit_almaushop_faq_or_cancel, inline_keyboard_edit_button_content_almaushop_or_cancel, \
    inline_keyboard_cancel_almaushop_faq_create, inline_keyboard_cancel_almaushop_faq_update, \
    inline_keyboard_cancel_almaushop_website_contacts

from data.button_names.almaushop_buttons import almaushop_website_button, almaushop_contacts_button

# Импортирование функций из БД контроллера
from utils import db_api as db

# Импорт класса парсеров
from utils.almaushop_parser import AlmauShop, AlmauShopBooks

# Импорт стейтов
from states.admin import CreateFaqAlmauShop, DeleteFaqAlmauShop, EditFaqAlmauShop, EditButtonContentAlmauShop

import aiogram.utils.markdown as fmt
from utils.delete_inline_buttons import delete_inline_buttons_in_dialogue


############### Админ меню для AlmaU Shop ####################
# Парсинг сайта almaushop.kz мерча и загрузка данных в таблицу в БД
@dp.callback_query_handler(text_contains='update_almaushop_merch')
async def callback_inline_update_almaushop_merch(call: CallbackQuery):
    logging.info(
        f'User({call.message.chat.id}) запустил обновление данных таблицы "almau_shop_products" call.data - {call.data}')
    try:
        shop = AlmauShop()
        shop.parse_page(text=shop.load_page())
        await bot.send_message(call.message.chat.id,
                               '🔄 Началось обновление данных в таблице, пожалуйста ожидайте!')
        await db.clear_almaushop_table()
        await bot.send_chat_action(call.message.chat.id, ChatActions.UPLOAD_DOCUMENT)
        for i in shop.result:
            await db.add_almau_shop_data(call.message.chat.id, i.product_name, i.price, i.currency, i.img, i.url)
        await bot.send_message(call.message.chat.id, '✅ Данные в таблице almau shop успешно обновлены')
    except Exception as err:
        logging.exception(err)
        await bot.send_message(call.message.chat.id, '❗ Произошла ошибка')


# Парсинг сайта almaushop.kz/books книг и загрузка данных в таблицу в БД
@dp.callback_query_handler(text_contains='update_almaushop_books')
async def callback_inline_update_almaushop_books(call: CallbackQuery):
    logging.info(
        f'User({call.message.chat.id}) запустил обновление данных таблицы "almau_shop_books" call.data - {call.data}')
    book_shop = AlmauShopBooks()
    book_shop.parse_page(text=book_shop.load_page())
    try:
        await bot.send_message(call.message.chat.id, '🔄 Началось обновление данных в таблице, пожалуйста ожидайте!')
        await db.clear_almaushop_books_table()
        await bot.send_chat_action(call.message.chat.id, ChatActions.UPLOAD_DOCUMENT)
        for i in book_shop.result:
            await db.add_almau_shop_books(call.message.chat.id, i.book_name, i.author_name, i.price, i.currency, i.img,
                                          i.url)
        await bot.send_message(call.message.chat.id, '✅ Данные в таблице almau_shop_books успешно обновлены')
    except Exception as err:
        logging.exception(err)
        await bot.send_message(call.message.chat.id, '❗ Произошла ошибка')
    await call.answer(text='✅ Данные в таблице almau_shop_books успешно обновлены', show_alert=False)


@dp.callback_query_handler(text='add_faq_almaushop', state=None)
async def callback_inline_add_faq_almaushop(call: CallbackQuery, state: FSMContext):
    logging.info(f'User({call.message.chat.id}) нажал на кнопку {call.data}')
    await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                text='Напишите вопрос', reply_markup=inline_keyboard_cancel_almaushop_faq_create())
    await CreateFaqAlmauShop.question.set()
    await call.answer()


# Изменение контента кнопок вебсайта и контактов в меню almaushop
@dp.callback_query_handler(text=['edit_website_b_almaushop', 'edit_contacts_b_almaushop'], state=None)
async def edit_button_content_almaushop(call: CallbackQuery, state: FSMContext):
    logging.info(f'User({call.message.chat.id}) нажал на кнопку {call.data}')
    if call.data == 'edit_website_b_almaushop':
        await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                    text=f'Напишите новый текст для кнопки {almaushop_website_button}',
                                    parse_mode='HTML',
                                    reply_markup=inline_keyboard_cancel_almaushop_website_contacts())
        await state.update_data(button_name=almaushop_website_button)
    elif call.data == 'edit_contacts_b_almaushop':
        await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                    text=f'Напишите новый текст для кнопки {almaushop_contacts_button}:',
                                    parse_mode='HTML',
                                    reply_markup=inline_keyboard_cancel_almaushop_website_contacts())
        await state.update_data(button_name=almaushop_contacts_button)
    await EditButtonContentAlmauShop.button_content.set()
    await call.answer()


# @dp.callback_query_handler(text='cancel_almaushop_web_con', state=['*'])
# async def cancel_inline_almaushop_website_contacts(call: CallbackQuery, state: FSMContext):
#     logging.info(f'User({call.message.chat.id}) нажал на кнопку {call.data}')
#     try:
#         await bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id)  # Убирает инлайн клавиатуру
#     except:
#         pass
#     await bot.send_message(chat_id=call.message.chat.id,
#                            text=f'✅ Успешно отменено'
#                                 f'Возврат в Админ меню AlmaU Shop:', reply_markup=inline_keyboard_almau_shop_admin())
#     await state.reset_state()


@dp.message_handler(content_types=ContentType.ANY, state=EditButtonContentAlmauShop.button_content)
async def edit_button_content_almaushop_first_step(message: types.Message, state: FSMContext):
    await delete_inline_buttons_in_dialogue(message)
    if message.content_type == 'text':
        if len(message.text) <= 4000:
            await state.update_data(button_content=message.text)
            await message.reply('✅ Новый текст получен.\n'
                                'Подтвердите изменение',
                                reply_markup=inline_keyboard_edit_button_content_almaushop_or_cancel())
            await EditButtonContentAlmauShop.confirm.set()
        else:
            await message.reply(
                f'Ваше сообщение содержит больше количество символов = <b>{len(message.text)}</b>. '
                f'Ограничение в 4000 символов. Сократите количество символов и попробуйте снова',
                parse_mode='HTML',
                reply_markup=inline_keyboard_cancel_almaushop_website_contacts())
    else:
        await message.reply('Ошибка - ваше сообщение должно содержать только текст\n'
                            'Повторите отправку сообщения',
                            reply_markup=inline_keyboard_cancel_almaushop_website_contacts())


@dp.callback_query_handler(text='edit_button_content_shop', state=EditButtonContentAlmauShop.confirm)
async def edit_button_content_almaushop_last_step(call: CallbackQuery, state: FSMContext):
    logging.info(f'User({call.message.chat.id}) нажал на кнопку {call.data}')
    try:
        data = await state.get_data()
        await db.edit_almau_shop_menu_button(call.message.chat.id, data['button_content'], data['button_name'])
        await bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id)  # Убирает инлайн клавиатуру
        await bot.send_message(chat_id=call.message.chat.id,
                               text=f'✅ Успешно изменен контент для кнопки - "{data["button_name"]}" для раздела AlmaU Shop\n'
                                    f'Админ меню AlmaU Shop:', reply_markup=inline_keyboard_almau_shop_admin())
        await state.reset_state()
        await call.answer(text=f'✅ Успешно изменен контент для кнопки - "{data["button_name"]}"')
    except Exception as error:
        logging.info(f'Error - {error}')
        await bot.send_message(call.message.chat.id, f'Произошла ошибка - {error}')


@dp.callback_query_handler(text='cancel_ed_but_con_shop', state=['*'])
async def edit_button_content_almaushop_last_step_cancel(call: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    logging.info(f'User({call.message.chat.id}) нажал на кнопку {call.data}')
    # await bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id)  # Убирает инлайн клавиатуру
    await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                text=f'❌ Отмена изменения контента для кнопки - "{data["button_name"]}" для раздела AlmaU Shop\n'
                                     f'Админ меню AlmaU Shop:', reply_markup=inline_keyboard_almau_shop_admin())
    await state.reset_state()
    await call.answer(text=f'❌ Отмена изменения контента для кнопки - "{data["button_name"]}"')


@dp.message_handler(content_types=ContentType.ANY, state=CreateFaqAlmauShop.question)
async def callback_inline_add_faq_almaushop_question_step(message: types.Message, state: FSMContext):
    # await state.update_data(file_id=message.document.file_id, user_id=message.chat.id)
    # data = await state.get_data()
    await delete_inline_buttons_in_dialogue(message)
    if message.content_type == 'text':
        if len(message.text) <= 300:
            await state.update_data(question=fmt.quote_html(message.text))
            await message.reply('✅ Вопрос получен.\n'
                                'Теперь отправьте ответ:', reply_markup=inline_keyboard_cancel_almaushop_faq_create())
            await CreateFaqAlmauShop.answer.set()
        else:
            await message.reply(
                f'Ваше сообщение содержит больше количество символов = <b>{len(message.text)}</b>. '
                f'Ограничение в 300 символов. Сократите количество символов и попробуйте снова',
                parse_mode='HTML', reply_markup=inline_keyboard_cancel_almaushop_faq_create())
    else:
        # print(message.content_type)
        await message.reply('Ошибка - ваше сообщение должно содержать только текст\n'
                            'Повторите снова', reply_markup=inline_keyboard_cancel_almaushop_faq_create())


@dp.message_handler(content_types=ContentType.ANY, state=CreateFaqAlmauShop.answer)
async def callback_inline_add_faq_almaushop_answer_step(message: types.Message, state: FSMContext):
    # await state.update_data(file_id=message.document.file_id, user_id=message.chat.id)
    # data = await state.get_data()
    await delete_inline_buttons_in_dialogue(message)
    if message.content_type == 'text':
        if len(message.text) <= 4000:
            await state.update_data(answer=fmt.quote_html(message.text))
            await message.reply('✅ Ответ получен.\n')
            data = await state.get_data()
            await message.answer(f'• <b>Ваш вопрос</b>\n'
                                 f'{data["question"]}\n\n'
                                 f'• <b>Ваш ответ</b>\n'
                                 f'{data["answer"]}\n\n'
                                 f'<i><u>Добавть их в F.A.Q?</u></i>',
                                 reply_markup=inline_keyboard_add_almaushop_faq_or_cancel())
            await state.reset_state(with_data=False)
        else:
            await message.reply(
                f'Ваше сообщение содержит больше количество символов = <b>{len(message.text)}</b>. '
                f'Ограничение в 4000 символов. Сократите количество символов и попробуйте снова',
                parse_mode='HTML')
    else:
        # print(message.content_type)
        await message.reply('Ошибка - ваше сообщение должно содержать только текст\n'
                            'Повторите снова', reply_markup=inline_keyboard_cancel_almaushop_faq_create())


@dp.callback_query_handler(text='save_faq_almaushop', state=None)
async def callback_inline_add_faq_almaushop(call: CallbackQuery, state: FSMContext):
    logging.info(f'User({call.message.chat.id}) нажал на кнопку {call.data}')
    try:
        data = await state.get_data()
        await db.add_almau_shop_faq(call.message.chat.id, data['question'], data['answer'])
        await bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id)  # Убирает инлайн клавиатуру
        await bot.send_message(chat_id=call.message.chat.id,
                               text='✅ Успешно сохранен вопрос и ответ для раздела F.A.Q AlmaU Shop\n'
                                    'Админ меню AlmaU Shop:', reply_markup=inline_keyboard_almau_shop_admin())
        await state.reset_state()
    except Exception as error:
        logging.info(f'Error - {error}')
        await bot.send_message(call.message.chat.id, f'Произошла ошибка - {error}')
    await call.answer(text='✅ Успешно сохранено')


@dp.callback_query_handler(text='cancel_almaushop_faq', state=None)
async def callback_inline_cancel_faq_almaushop(call: CallbackQuery, state: FSMContext):
    logging.info(f'User({call.message.chat.id}) нажал на кнопку {call.data}')
    await bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id)  # Убирает инлайн клавиатуру
    await bot.send_message(chat_id=call.message.chat.id,
                           text='❌ Отмена создания вопроса и ответа для раздела F.A.Q AlmaU Shop\n'
                                'Админ меню AlmaU Shop:', reply_markup=inline_keyboard_almau_shop_admin())
    await state.reset_state()
    await call.answer(text='❌ Отмена создания')


@dp.callback_query_handler(text='cancel_step_almaushop_faq', state=['*'])
async def callback_inline_cancel_faq_almaushop(call: CallbackQuery, state: FSMContext):
    logging.info(f'User({call.message.chat.id}) нажал на кнопку {call.data}')
    await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                text='<b>❌ Создание F.A.Q успешно отменено</b>\n'
                                     'Возврат в Админ меню AlmaU Shop:',
                                parse_mode='HTML',
                                reply_markup=inline_keyboard_almau_shop_admin())
    await state.reset_state()
    await call.answer(text='❌ успешно отменено')


# Отмена изменения в AlmaU Shop FAQ и возврат к выбору изменения вопроса или ответа
@dp.callback_query_handler(text='cancel_almaushop_faq_update', state=['*'])
async def callback_inline_cancel_faq_almaushop_update(call: CallbackQuery, state: FSMContext):
    logging.info(f'User({call.message.chat.id}) нажал на кнопку {call.data}')
    data = await state.get_data()
    await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                text=f'Выберите, что нужно изменить:\n'
                                     f'• <b>Вопрос</b>\n'
                                     f'{data["question_text"]}\n\n'
                                     f'• <b>Ответ</b>\n'
                                     f'{data["answer_text"]}',
                                reply_markup=inline_keyboard_edit_faq_almaushop_choice(), parse_mode='HTML')
    await state.reset_state(with_data=False)
    await call.answer()


#### Удаление FAQ AlmaU Shop ####
@dp.callback_query_handler(text='delete_faq_almaushop', state=None)
async def callback_inline_delete_faq_almaushop(call: CallbackQuery, state: FSMContext):
    logging.info(f'User({call.message.chat.id}) нажал на кнопку {call.data}')
    await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                text='Выберите кнопку для удаление:',
                                reply_markup=await inline_keyboard_delete_faq_almaushop())
    await call.answer()
    # await DeleteFaqAlmauShop.question.set()


#### Возвращение в админ меню Almau Shop - ОТМЕНА Удаления faq
@dp.callback_query_handler(text='back_to_almaushop_admin', state=['*'])
async def callback_inline_delete_faq_almaushop_back(call: CallbackQuery, state: FSMContext):
    logging.info(f'User({call.message.chat.id}) нажал на кнопку {call.data}')
    await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                text='Админ меню AlmaU Shop:', reply_markup=inline_keyboard_almau_shop_admin())
    await state.reset_state()
    await call.answer()


#### Возвращение в меню изменения FAQ Almau Shop
@dp.callback_query_handler(text='back_to_almaushop_admin_faq', state=['*'])
async def callback_inline_delete_faq_almaushop_back(call: CallbackQuery, state: FSMContext):
    await state.reset_state()
    await callback_inline_edit_faq_almaushop(call)
    await call.answer()


@dp.callback_query_handler(almau_shop_faq_delete_callback.filter(), state=None)
async def callback_inline_delete_faq_almaushop_final(call: CallbackQuery, state: FSMContext, callback_data: dict):
    logging.info(f'User({call.message.chat.id}) нажал на кнопку {call.data}')
    id = callback_data.get('callback_id')
    question = await db.almaushop_faq_find_question(id)
    text_delete = f"Вы хотите удалить кнопку F.A.Q\n" \
                  f"<b>{question}</b>\n\n" \
                  f"<i><u>Вы уверены?</u></i>"
    await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                text=text_delete,
                                reply_markup=cancel_or_delete_faq_almau_shop())
    await state.update_data(question_text=fmt.quote_html(question), user_id=call.message.chat.id)
    await DeleteFaqAlmauShop.confirm_delete.set()
    await call.answer()


# Удаление FAQ AlmaU Shop из базы данных
@dp.callback_query_handler(text='delete_faq_almaushop_final', state=DeleteFaqAlmauShop.confirm_delete)
async def callback_inline_send_schedule(call: CallbackQuery, state: FSMContext):
    try:
        data = await state.get_data()
        await db.delete_faq_almaushop_button(data["question_text"])
        await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                    text=f'✅ Указанный F.A.Q - <b>{data["question_text"]}</b> был успешно удален\n'
                                         f'Админ меню AlmaU Shop:',
                                    parse_mode='HTML',
                                    reply_markup=inline_keyboard_almau_shop_admin())
        await state.reset_state()
        logging.info(f'User({call.message.chat.id}) удалил FAQ Almau Shop для {data["question_text"]}')
        await call.answer(text='✅ успешно удалено')
    except Exception as e:
        await call.message.answer(f'Ошибка FAQ Almau Shop не удалено, (Ошибка - {e})')
        logging.info(f'Ошибка - {e}')
        await call.answer()


@dp.callback_query_handler(text='edit_faq_almaushop', state=None)
async def callback_inline_edit_faq_almaushop(call: CallbackQuery):
    logging.info(f'User({call.message.chat.id}) нажал на кнопку {call.data}')
    await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                text='Выберите кнопку для изменения:',
                                reply_markup=await inline_keyboard_edit_faq_almaushop())
    await call.answer()


@dp.callback_query_handler(almau_shop_faq_edit_callback.filter(), state=None)
async def callback_inline_edit_faq_almaushop_choice_step(call: CallbackQuery, state: FSMContext, callback_data: dict):
    logging.info(f'User({call.message.chat.id}) нажал на кнопку {call.data}')
    id = callback_data.get('callback_id')
    db_request = await db.almaushop_faq_find_question_and_answer(id)
    question = db_request['question']
    answer = db_request['answer']
    await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                text=f'Выберите, что нужно изменить:\n'
                                     f'• <b>Вопрос</b>\n'
                                     f'{question}\n\n'
                                     f'• <b>Ответ</b>\n'
                                     f'{answer}',
                                reply_markup=inline_keyboard_edit_faq_almaushop_choice(), parse_mode='HTML')
    await state.update_data(question_text=fmt.quote_html(question), answer_text=fmt.quote_html(answer),
                            user_id=call.message.chat.id, faq_id=id)
    await call.answer()


@dp.callback_query_handler(text='edit_faq_shop_q')
async def edit_faq_almaushop_choice_step_question(call: CallbackQuery, state: FSMContext):
    logging.info(f'User({call.message.chat.id}) нажал на кнопку {call.data}')
    await bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id)  # Убирает инлайн клавиатуру
    await bot.send_message(chat_id=call.message.chat.id,
                           text='Напишите на какой текст изменить вопрос',
                           reply_markup=inline_keyboard_cancel_almaushop_faq_update())
    await EditFaqAlmauShop.question_confirm.set()
    await call.answer()


@dp.callback_query_handler(text='edit_faq_shop_a')
async def edit_faq_almaushop_choice_step_answer(call: CallbackQuery, state: FSMContext):
    logging.info(f'User({call.message.chat.id}) нажал на кнопку {call.data}')
    await bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id)  # Убирает инлайн клавиатуру
    await bot.send_message(chat_id=call.message.chat.id,
                           text='Напишите на какой текст изменить ответ',
                           reply_markup=inline_keyboard_cancel_almaushop_faq_update())
    await EditFaqAlmauShop.answer_confirm.set()
    await call.answer()


@dp.message_handler(content_types=ContentType.ANY, state=EditFaqAlmauShop.question_confirm)
async def edit_faq_almaushop_choice_step_question_final(message: types.Message, state: FSMContext):
    await delete_inline_buttons_in_dialogue(message)
    if message.content_type == 'text':
        if len(message.text) <= 300:
            await state.update_data(selected_item=fmt.quote_html(message.text),
                                    thing_to_change='question_to_change')
            data = await state.get_data()
            await message.answer(f'• <b>Ваш новый вопрос</b>\n'
                                 f'{data["selected_item"]}\n\n'
                                 f'• <b>Для ответа</b>\n'
                                 f'{data["answer_text"]}\n\n'
                                 f'<i><u>Подтвердите изменение</u></i>',
                                 reply_markup=inline_keyboard_edit_almaushop_faq_or_cancel(), parse_mode='HTML')
            await state.reset_state(with_data=False)
        else:
            await message.reply(
                f'Ваше сообщение содержит больше количество символов = <b>{len(message.text)}</b>. '
                f'Ограничение в 300 символов. Сократите количество символов и попробуйте снова',
                parse_mode='HTML',
                reply_markup=inline_keyboard_cancel_almaushop_faq_update())
    else:
        # print(message.content_type)
        await message.reply('Ошибка - ваше сообщение должно содержать только текст\n'
                            'Повторите снова', reply_markup=inline_keyboard_cancel_almaushop_faq_update())


@dp.message_handler(content_types=ContentType.ANY, state=EditFaqAlmauShop.answer_confirm)
async def edit_faq_almaushop_choice_step_answer_final(message: types.Message, state: FSMContext):
    await delete_inline_buttons_in_dialogue(message)
    if message.content_type == 'text':
        if len(message.text) <= 4000:
            await state.update_data(selected_item=fmt.quote_html(message.text),
                                    thing_to_change='answer_to_change')
            data = await state.get_data()
            await message.answer(f'• <b>Ваш новый ответ</b>\n'
                                 f'{data["selected_item"]}\n\n'
                                 f'• <b>Для вопроса</b>\n'
                                 f'{data["question_text"]}\n\n'
                                 f'<i><u>Подтвердите изменение</u></i>',
                                 reply_markup=inline_keyboard_edit_almaushop_faq_or_cancel(), parse_mode='HTML')
            await state.reset_state(with_data=False)
        else:
            await message.reply(
                f'Ваше сообщение содержит больше количество символов = <b>{len(message.text)}</b>. '
                f'Ограничение в 4000 символов. Сократите количество символов и попробуйте снова',
                parse_mode='HTML',
                reply_markup=inline_keyboard_cancel_almaushop_faq_update())
    else:
        # print(message.content_type)
        await message.reply('Ошибка - ваше сообщение должно содержать только текст\n'
                            'Повторите снова',
                            reply_markup=inline_keyboard_cancel_almaushop_faq_update())


@dp.callback_query_handler(text='edit_faq_shop_conf', state=None)
async def edit_faq_almaushop_choice_step_question_final_save(call: CallbackQuery, state: FSMContext):
    logging.info(f'User({call.message.chat.id}) нажал на кнопку {call.data}')
    try:
        data = await state.get_data()
        if data['thing_to_change'] == 'question_to_change':
            await db.edit_almau_shop_faq_question(data['user_id'], data['selected_item'], data['faq_id'])
        elif data['thing_to_change'] == 'answer_to_change':
            await db.edit_almau_shop_faq_answer(data['user_id'], data['selected_item'], data['faq_id'])
        await bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id)  # Убирает инлайн клавиатуру
        await bot.send_message(chat_id=call.message.chat.id,
                               text='✅ Ваши изменения для раздела F.A.Q AlmaU Shop успешно сохранены\n'
                                    'Админ меню AlmaU Shop:', reply_markup=inline_keyboard_almau_shop_admin())
        await state.reset_state()
        await call.answer(text='✅ успешно изменено')
    except Exception as error:
        logging.info(f'Error - {error}')
        await bot.send_message(call.message.chat.id, f'Произошла ошибка - {error}')
        await call.answer()


@dp.callback_query_handler(text='edit_faq_shop_dec', state=None)
async def edit_faq_almaushop_choice_step_question_final_decline(call: CallbackQuery, state: FSMContext):
    logging.info(f'User({call.message.chat.id}) нажал на кнопку {call.data}')
    try:
        await bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id)  # Убирает инлайн клавиатуру
    except:
        pass
    await bot.send_message(chat_id=call.message.chat.id,
                           text='❌ Отмена изменения вопроса для раздела F.A.Q AlmaU Shop\n'
                                'Админ меню AlmaU Shop:', reply_markup=inline_keyboard_almau_shop_admin())
    await state.reset_state()
    await call.answer(text='❌ Отменено')


@dp.callback_query_handler(text='cancel_del_faq_almaushop', state=DeleteFaqAlmauShop.confirm_delete)
async def callback_inline_cancel_faq_almaushop(call: CallbackQuery, state: FSMContext):
    logging.info(f'User({call.message.chat.id}) нажал на кнопку {call.data}')
    data = await state.get_data()
    await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                text=f'❌ Отмена удаления F.A.Q ({data["question_text"]})\n'
                                     f'Админ меню AlmaU Shop:', reply_markup=inline_keyboard_almau_shop_admin())
    await state.reset_state()
    await call.answer(text='❌ Отменено')
############### Админ меню для AlmaU Shop конец ####################
