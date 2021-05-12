import logging
from math import ceil

from aiogram import types
from aiogram.types import CallbackQuery, ContentType
from aiogram.dispatcher import FSMContext
from loader import dp, bot

# Импорт клавиатур
from keyboards.inline import main_faq_edit_callback, main_faq_delete_callback, inline_keyboard_add_main_faq_or_cancel, \
    inline_keyboard_faq_admin, inline_keyboard_edit_main_faq, \
    inline_keyboard_edit_main_faq_choice, inline_keyboard_edit_main_faq_or_cancel, inline_keyboard_delete_main_faq, \
    cancel_or_delete_main_faq, inline_keyboard_cancel_faq, inline_keyboard_cancel_faq_edit

# Импортирование функций из БД контроллера
from utils import db_api as db

# Импорт стейтов
from states.admin import CreateMainFaq, EditMainFaq, DeleteMainFaq
import aiogram.utils.markdown as fmt
from utils.delete_inline_buttons import delete_inline_buttons_in_dialogue


######################### Добавление нового FAQ в главном меню #############################################
@dp.callback_query_handler(text='add_main_faq', state=None)
async def callback_inline_add_main_faq(call: CallbackQuery, state: FSMContext):
    logging.info(f'User({call.message.chat.id}) нажал на кнопку {call.data}')
    await bot.edit_message_text(chat_id=call.message.chat.id,
                                message_id=call.message.message_id,
                                text='Напишите вопрос:\n',
                                reply_markup=inline_keyboard_cancel_faq())
    await CreateMainFaq.question.set()
    await call.answer()


@dp.message_handler(content_types=ContentType.ANY, state=CreateMainFaq.question)
async def callback_inline_add_main_faq_question_step(message: types.Message, state: FSMContext):
    await delete_inline_buttons_in_dialogue(message)
    if message.content_type == 'text':
        if len(message.text) <= 300:
            await state.update_data(question=fmt.quote_html(message.text))
            await message.reply('✅ Вопрос получен.\n'
                                'Теперь отправьте ответ:', reply_markup=inline_keyboard_cancel_faq())
            await CreateMainFaq.answer.set()
        else:
            await message.reply(
                f'Ваше сообщение содержит больше количество символов = <b>{len(message.text)}</b>. '
                f'Ограничение в 300 символов. Сократите количество символов и попробуйте снова',
                parse_mode='HTML', reply_markup=inline_keyboard_cancel_faq())
    else:
        await message.reply('Ошибка - ваше сообщение должно содержать только текст\n'
                            'Повторите снова', reply_markup=inline_keyboard_cancel_faq())


@dp.message_handler(content_types=ContentType.ANY, state=CreateMainFaq.answer)
async def callback_inline_add_main_faq_answer_step(message: types.Message, state: FSMContext):
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
                                 f'<i><u>Добавть их в F.A.Q?</u></i>', reply_markup=inline_keyboard_add_main_faq_or_cancel())
            await state.reset_state(with_data=False)
        else:
            await message.reply(
                f'Ваше сообщение содержит больше количество символов = <b>{len(message.text)}</b>. '
                f'Ограничение в 4000 символов. Сократите количество символов и попробуйте снова',
                parse_mode='HTML', reply_markup=inline_keyboard_cancel_faq())
    else:
        await message.reply('Ошибка - ваше сообщение должно содержать только текст\n'
                            'Повторите снова', reply_markup=inline_keyboard_cancel_faq())


@dp.callback_query_handler(text='save_main_faq', state=None)
async def callback_inline_add_main_faq(call: CallbackQuery, state: FSMContext):
    logging.info(f'User({call.message.chat.id}) нажал на кнопку {call.data}')
    try:
        data = await state.get_data()
        await db.add_data_main_faq(call.message.chat.id, data['question'], data['answer'])
        await bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id)  # Убирает инлайн клавиатуру
        await bot.send_message(chat_id=call.message.chat.id,
                               text='✅ Успешно сохранен вопрос и ответ для раздела F.A.Q в главном меню\n'
                                    'Админ меню AlmaU Shop:', reply_markup=inline_keyboard_faq_admin())
        await state.reset_state()
        await call.answer()
    except Exception as error:
        logging.info(f'Error - {error}')
        await bot.send_message(call.message.chat.id, f'Произошла ошибка - {error}')


@dp.callback_query_handler(text='cancel_main_faq', state=None)
async def callback_inline_cancel_creation_main_faq(call: CallbackQuery, state: FSMContext):
    logging.info(f'User({call.message.chat.id}) нажал на кнопку {call.data}')
    await bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id)  # Убирает инлайн клавиатуру
    await bot.send_message(chat_id=call.message.chat.id,
                           text='❌ Отмена создания вопроса и ответа для F.A.Q в главном меню\n'
                                'Админ меню AlmaU Shop:', reply_markup=inline_keyboard_faq_admin())
    await state.reset_state()
    await call.answer()


######################### КОНЕЦ Добавление нового FAQ в главном меню КОНЕЦ ############################################

######################### Изменение FAQ в главном меню #############################################
@dp.callback_query_handler(text='edit_main_faq', state=None)
async def callback_inline_edit_main_faq(call: CallbackQuery, state: FSMContext):
    logging.info(f'User({call.message.chat.id}) нажал на кнопку {call.data}')
    await state.update_data(page=0)
    data = await state.get_data()
    await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                text=f'Страница {data["page"] + 1}\n'
                                     'Выберите кнопку для изменения:',
                                reply_markup=await inline_keyboard_edit_main_faq(data["page"]))
    await call.answer()


@dp.callback_query_handler(main_faq_edit_callback.filter())
async def callback_inline_edit_main_faq_choice_step(call: CallbackQuery, state: FSMContext, callback_data: dict):
    logging.info(f'User({call.message.chat.id}) нажал на кнопку {call.data}')
    id = callback_data.get('callback_id')
    db_request = await db.main_faq_select_question_and_answer(id)
    question = db_request['question']
    answer = db_request['answer']
    await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                text=f'Выберите, что нужно изменить:\n'
                                     f'• <b>Вопрос</b>\n'
                                     f'{question}\n\n'
                                     f'• <b>Ответ</b>\n'
                                     f'{answer}',
                                reply_markup=inline_keyboard_edit_main_faq_choice(), parse_mode='HTML')
    await state.update_data(question_text=fmt.quote_html(question), answer_text=fmt.quote_html(answer),
                            user_id=call.message.chat.id, faq_id=id)
    await call.answer()


@dp.callback_query_handler(text='edit_main_faq_q')
async def edit_main_faq_choice_step_question(call: CallbackQuery, state: FSMContext):
    logging.info(f'User({call.message.chat.id}) нажал на кнопку {call.data}')
    await bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id)  # Убирает инлайн клавиатуру
    await bot.send_message(chat_id=call.message.chat.id,
                           text='Напишите на какой текст изменить вопрос',
                           reply_markup=inline_keyboard_cancel_faq_edit())
    await EditMainFaq.question_confirm.set()
    await call.answer()


@dp.message_handler(content_types=ContentType.ANY, state=EditMainFaq.question_confirm)
async def edit_main_faq_choice_step_question_final(message: types.Message, state: FSMContext):
    await delete_inline_buttons_in_dialogue(message)
    if message.content_type == 'text':
        if len(message.text) <= 300:
            await state.update_data(selected_item=fmt.quote_html(message.text),
                                    thing_to_change='question_to_change')
            data = await state.get_data()
            await message.answer(f'• <b>Ваш новый вопрос</b>\n'
                                 f'{message.text}\n\n'
                                 f'• <b>Для ответа</b>\n'
                                 f'{data["answer_text"]}\n\n'
                                 f'<i><u>Подтвердите изменение</u></i>',
                                 reply_markup=inline_keyboard_edit_main_faq_or_cancel(), parse_mode='HTML')
            await state.reset_state(with_data=False)
        else:
            await message.reply(
                f'Ваше сообщение содержит больше количество символов = <b>{len(message.text)}</b>. '
                f'Ограничение в 300 символов. Сократите количество символов и попробуйте снова',
                parse_mode='HTML', reply_markup=inline_keyboard_cancel_faq_edit())
    else:
        await message.reply('Ошибка - ваше сообщение должно содержать только текст\n'
                            'Повторите снова', reply_markup=inline_keyboard_cancel_faq_edit())


@dp.callback_query_handler(text='edit_main_faq_a')
async def edit_main_faq_choice_step_answer(call: CallbackQuery, state: FSMContext):
    logging.info(f'User({call.message.chat.id}) нажал на кнопку {call.data}')
    await bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id)  # Убирает инлайн клавиатуру
    await bot.send_message(chat_id=call.message.chat.id,
                           text='Напишите на какой текст изменить ответ',
                           reply_markup=inline_keyboard_cancel_faq_edit())
    await EditMainFaq.answer_confirm.set()
    await call.answer()


@dp.message_handler(content_types=ContentType.ANY, state=EditMainFaq.answer_confirm)
async def edit_main_faq_choice_step_answer_final(message: types.Message, state: FSMContext):
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
                                 reply_markup=inline_keyboard_edit_main_faq_or_cancel(), parse_mode='HTML')
            await state.reset_state(with_data=False)
        else:
            await message.reply(
                f'Ваше сообщение содержит больше количество символов = <b>{len(message.text)}</b>. '
                f'Ограничение в 300 символов. Сократите количество символов и попробуйте снова',
                parse_mode='HTML', reply_markup=inline_keyboard_cancel_faq_edit())
    else:
        await message.reply('Ошибка - ваше сообщение должно содержать только текст\n'
                            'Повторите снова', reply_markup=inline_keyboard_cancel_faq_edit())


@dp.callback_query_handler(text='edit_main_faq_conf', state=None)
async def edit_main_faq_choice_step_question_final_save(call: CallbackQuery, state: FSMContext):
    logging.info(f'User({call.message.chat.id}) нажал на кнопку {call.data}')
    try:
        data = await state.get_data()
        if data['thing_to_change'] == 'question_to_change':
            await db.edit_main_faq_question(data['user_id'], data['selected_item'], data['faq_id'])
            await state.reset_state()
        elif data['thing_to_change'] == 'answer_to_change':
            await db.edit_main_faq_answer(data['user_id'], data['selected_item'], data['faq_id'])
            await state.reset_state()
        await bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id)  # Убирает инлайн клавиатуру
        await bot.send_message(chat_id=call.message.chat.id,
                               text='✅ Ваши изменения для раздела F.A.Q главного меню успешно сохранены\n'
                                    'Админ меню F.A.Q:', reply_markup=inline_keyboard_faq_admin())
        await call.answer()
    except Exception as error:
        logging.info(f'Error - {error}')
        await bot.send_message(call.message.chat.id, f'Произошла ошибка - {error}')


@dp.callback_query_handler(text='edit_main_faq_dec', state=None)
async def edit_main_faq_choice_step_question_final_decline(call: CallbackQuery, state: FSMContext):
    logging.info(f'User({call.message.chat.id}) нажал на кнопку {call.data}')
    await bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id)  # Убирает инлайн клавиатуру
    await bot.send_message(chat_id=call.message.chat.id,
                           text='❌ Отмена изменения вопроса для раздела F.A.Q главного меню\n'
                                'Админ меню F.A.Q:', reply_markup=inline_keyboard_faq_admin())
    await state.reset_state()
    await call.answer()


# FAQ кнопки вперед и назад для EDIT
@dp.callback_query_handler(text=["main_faq_prev_edit", "main_faq_next_edit"])
async def edit_main_menu_faq_next_prev(call: CallbackQuery, state: FSMContext):
    logging.info(f"User({call.message.chat.id}) enter {call.data}")
    data = await state.get_data()
    max_pages = (ceil(await db.main_faq_count() / 10))
    if call.data == "main_faq_next_edit" and (data['page'] + 1 < max_pages):
        await state.update_data(page=(data['page'] + 1))
        data = await state.get_data()
        await bot.edit_message_text(chat_id=call.message.chat.id,
                                    message_id=call.message.message_id,
                                    text=f'F.A.Q Страница {data["page"] + 1}\n'
                                         f'Выберите кнопку для изменения:',
                                    reply_markup=await inline_keyboard_edit_main_faq(data["page"]))
    elif call.data == "main_faq_prev_edit" and (data['page'] != 0):
        await state.update_data(page=(data['page'] - 1))
        data = await state.get_data()
        await bot.edit_message_text(chat_id=call.message.chat.id,
                                    message_id=call.message.message_id,
                                    text=f'F.A.Q Страница {data["page"] + 1}\n'
                                         f'Выберите кнопку для изменения:',
                                    reply_markup=await inline_keyboard_edit_main_faq(data["page"]))


######################### КОНЕЦ Изменение FAQ в главном меню КОНЕЦ #############################################

######################### Удаление FAQ в главном меню #############################################
@dp.callback_query_handler(text='delete_main_faq', state=None)
async def callback_inline_delete_main_faq(call: CallbackQuery, state: FSMContext):
    logging.info(f'User({call.message.chat.id}) нажал на кнопку {call.data}')
    await state.update_data(page=0)
    data = await state.get_data()
    await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                text=f'Страница {data["page"] + 1}\n'
                                     f'Выберите кнопку для удаление:',
                                reply_markup=await inline_keyboard_delete_main_faq(data['page']))
    await call.answer()


@dp.callback_query_handler(main_faq_delete_callback.filter())
async def callback_inline_delete_main_faq_final(call: CallbackQuery, state: FSMContext, callback_data: dict):
    logging.info(f'User({call.message.chat.id}) нажал на кнопку {call.data}')
    id = callback_data.get('callback_id')
    question = (await db.main_faq_select_question_and_answer(id))['question']
    text_delete = f"Вы хотите удалить кнопку F.A.Q\n" \
                  f"<b>{question}</b>\n\n" \
                  f"<i><u>Вы уверены?</u></i>"
    await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                text=text_delete,
                                reply_markup=cancel_or_delete_main_faq())
    await state.update_data(question_text=fmt.quote_html(question), user_id=call.message.chat.id)
    await DeleteMainFaq.confirm_delete.set()
    await call.answer()


# Удаление FAQ из базы данных
@dp.callback_query_handler(text='delete_main_faq', state=DeleteMainFaq.confirm_delete)
async def callback_inline_delete_main_faq_delete_step(call: CallbackQuery, state: FSMContext):
    try:
        data = await state.get_data()
        await db.delete_main_faq_button(data["question_text"])
        await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                    text=f'✅ Указанный F.A.Q - "<b>{data["question_text"]}</b>" был успешно удален.\n'
                                         f'Возвращение в Админ меню F.A.Q:',
                                    reply_markup=inline_keyboard_faq_admin(),
                                    parse_mode='HTML')
        await state.reset_state()
        logging.info(f'User({call.message.chat.id}) удалил FAQ главного меню для {data["question_text"]}')
        await call.answer()
    except Exception as e:
        await call.message.answer(f'Ошибка FAQ главного меню не удален, (Ошибка - {e})')
        logging.info(f'Ошибка - {e}')


# отмена
@dp.callback_query_handler(text='cancel_del_main_faq', state=DeleteMainFaq.confirm_delete)
async def callback_inline_cancel_delete_main_faq(call: CallbackQuery, state: FSMContext):
    logging.info(f'User({call.message.chat.id}) нажал на кнопку {call.data}')
    await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                text='❌ Отмена удаления вопроса F.A.Q главного меню.\n'
                                     'Возвращение в Админ меню F.A.Q:', reply_markup=inline_keyboard_faq_admin())
    await state.reset_state()
    await call.answer()


# FAQ кнопки вперед и назад для DELETE
@dp.callback_query_handler(text=["main_faq_prev_delete", "main_faq_next_delete"])
async def delete_main_menu_faq_next_prev(call: CallbackQuery, state: FSMContext):
    logging.info(f"User({call.message.chat.id}) enter {call.data}")
    data = await state.get_data()
    max_pages = (ceil(await db.main_faq_count() / 10))
    if call.data == "main_faq_next_delete" and (data['page'] + 1 < max_pages):
        await state.update_data(page=(data['page'] + 1))
        data = await state.get_data()
        await bot.edit_message_text(chat_id=call.message.chat.id,
                                    message_id=call.message.message_id,
                                    text=f'F.A.Q Страница {data["page"] + 1}\n'
                                         f'Выберите кнопку для удаление:',
                                    reply_markup=await inline_keyboard_delete_main_faq(data['page']))
    elif call.data == "main_faq_prev_delete" and (data['page'] != 0):
        await state.update_data(page=(data['page'] - 1))
        data = await state.get_data()
        await bot.edit_message_text(chat_id=call.message.chat.id,
                                    message_id=call.message.message_id,
                                    text=f'F.A.Q Страница {data["page"] + 1}\n'
                                         f'Выберите кнопку для удаление:',
                                    reply_markup=await inline_keyboard_delete_main_faq(data['page']))


######################### КОНЕЦ Удаления FAQ в главном меню КОНЕЦ #############################################


#### Возвращение в админ меню FAQ
@dp.callback_query_handler(text='back_to_admin_faq', state=['*'])
async def callback_inline_back_to_admin_faq(call: CallbackQuery, state: FSMContext):
    logging.info(f'User({call.message.chat.id}) нажал на кнопку {call.data}')
    await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                text='Админ меню F.A.Q:', reply_markup=inline_keyboard_faq_admin())
    await state.reset_state()
    await call.answer()


#### Возвращение к кнопкам изменить в админ меню FAQ
@dp.callback_query_handler(text='back_to_admin_edit_faq', state=['*'])
async def callback_inline_back_to_admin_edit_faq(call: CallbackQuery, state: FSMContext):
    logging.info(f'User({call.message.chat.id}) нажал на кнопку {call.data}')
    data = await state.get_data()
    await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                text='Выберите кнопку для изменения:',
                                reply_markup=await inline_keyboard_edit_main_faq(data['page']))
    await call.answer()


@dp.callback_query_handler(text='cancel_step_faq', state=['*'])
async def callback_inline_cancel_step_faq(call: CallbackQuery, state: FSMContext):
    logging.info(f'User({call.message.chat.id}) нажал на кнопку {call.data}')
    await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                text='<b>❌ Успешно отменено</b>\n'
                                     'Возврат в Админ меню F.A.Q:',
                                parse_mode='HTML',
                                reply_markup=inline_keyboard_faq_admin())
    await state.reset_state()
    await call.answer()


@dp.callback_query_handler(text='cancel_step_faq_edit', state=['*'])
async def callback_inline_cancel_step_faq_edit(call: CallbackQuery, state: FSMContext):
    logging.info(f'User({call.message.chat.id}) нажал на кнопку {call.data}')
    data = await state.get_data()
    await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                text=f'Выберите, что нужно изменить:\n'
                                     f'<u>Вопрос</u> - {data["question_text"]}\n'
                                     f'<u>Ответ</u> - {data["answer_text"]}',
                                reply_markup=inline_keyboard_edit_main_faq_choice(), parse_mode='HTML')
    await state.reset_state(with_data=False)
    await call.answer()
