import logging
from aiogram.utils import exceptions
from aiogram import types
from aiogram.types import CallbackQuery, ContentType
from aiogram.dispatcher import FSMContext
from loader import dp, bot

# Импорт клавиатур
from keyboards.inline import almau_shop_faq_delete_callback, almau_shop_faq_edit_callback, main_faq_edit_callback, \
    main_faq_delete_callback
from keyboards.inline.admin_buttons import inline_keyboard_almau_shop_admin, \
    inline_keyboard_add_almaushop_faq_or_cancel, inline_keyboard_delete_faq_almaushop, cancel_or_delete_faq_almau_shop, \
    inline_keyboard_edit_faq_almaushop, inline_keyboard_edit_faq_almaushop_choice, \
    inline_keyboard_edit_almaushop_faq_or_cancel, inline_keyboard_edit_button_content_almaushop_or_cancel, \
    inline_keyboard_add_main_faq_or_cancel, inline_keyboard_faq_admin, inline_keyboard_edit_main_faq, \
    inline_keyboard_edit_main_faq_choice, inline_keyboard_edit_main_faq_or_cancel, inline_keyboard_delete_main_faq, \
    cancel_or_delete_main_faq

# Импортирование функций из БД контроллера
from utils import db_api as db

# Импорт класса парсеров
from utils.almaushop_parser import AlmauShop, AlmauShopBooks

# Импорт стейтов
from states.admin import CreateFaqAlmauShop, DeleteFaqAlmauShop, EditFaqAlmauShop, EditButtonContentAlmauShop, \
    CreateMainFaq, EditMainFaq, DeleteMainFaq

from utils.misc import rate_limit


######################### Добавление нового FAQ в главном меню #############################################
@dp.callback_query_handler(text='add_main_faq', state=None)
async def callback_inline_add_main_faq(call: CallbackQuery, state: FSMContext):
    logging.info(f'User({call.message.chat.id}) нажал на кнопку {call.data}')
    await call.message.answer('Напишите вопрос:\n'
                              'Для отмены - /cancel')
    await CreateMainFaq.question.set()


@dp.message_handler(content_types=ContentType.ANY, state=CreateMainFaq.question)
async def callback_inline_add_main_faq_question_step(message: types.Message, state: FSMContext):
    if message.content_type == 'text':
        if len(message.text) <= 300:
            await state.update_data(question=message.text)
            await message.reply('✅ Вопрос получен.\n'
                                'Теперь отправьте ответ:')
            await CreateMainFaq.answer.set()
        else:
            await message.reply(
                f'Ваше сообщение содержит больше количество символов = <b>{len(message.text)}</b>. Ограничение в 300 символов. Сократите количество символов и попробуйте снова',
                parse_mode='HTML')
    else:
        print(message.content_type)
        await message.reply('Ошибка - ваше сообщение должно содержать только текст\n'
                            'Повторите снова')


@dp.message_handler(content_types=ContentType.ANY, state=CreateMainFaq.answer)
async def callback_inline_add_main_faq_answer_step(message: types.Message, state: FSMContext):
    if message.content_type == 'text':
        if len(message.text) <= 4000:
            await state.update_data(answer=message.text)
            await message.reply('✅ Ответ получен.\n')
            data = await state.get_data()
            await message.answer(f'Ваш вопрос - {data["question"]}\n'
                                 f'Ваш ответ - {data["answer"]}\n\n'
                                 f'Сохранить их в F.A.Q?', reply_markup=inline_keyboard_add_main_faq_or_cancel())
            await state.reset_state(with_data=False)
        else:
            await message.reply(
                f'Ваше сообщение содержит больше количество символов = <b>{len(message.text)}</b>. Ограничение в 4000 символов. Сократите количество символов и попробуйте снова',
                parse_mode='HTML')
    else:
        print(message.content_type)
        await message.reply('Ошибка - ваше сообщение должно содержать только текст\n'
                            'Повторите снова')


@dp.callback_query_handler(text='save_main_faq', state=None)
async def callback_inline_add_main_faq(call: CallbackQuery, state: FSMContext):
    logging.info(f'User({call.message.chat.id}) нажал на кнопку {call.data}')
    try:
        data = await state.get_data()
        await db.add_data_main_faq(call.message.chat.id, data['question'], data['answer'])
        await bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id)  # Убирает инлайн клавиатуру
        await bot.send_message(call.message.chat.id,
                               '✅ Успешно сохранен вопрос и ответ для раздела F.A.Q в главном меню')
        await bot.send_message(chat_id=call.message.chat.id,
                               text='Админ меню AlmaU Shop:', reply_markup=inline_keyboard_faq_admin())
        await state.reset_state()
    except Exception as error:
        logging.info(f'Error - {error}')
        await bot.send_message(call.message.chat.id, f'Произошла ошибка - {error}')


@dp.callback_query_handler(text='cancel_main_faq', state=None)
async def callback_inline_cancel_creation_main_faq(call: CallbackQuery, state: FSMContext):
    logging.info(f'User({call.message.chat.id}) нажал на кнопку {call.data}')
    await bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id)  # Убирает инлайн клавиатуру
    await bot.send_message(call.message.chat.id, '❌ Отмена создания вопроса и ответа для F.A.Q в главном меню')
    await bot.send_message(chat_id=call.message.chat.id,
                           text='Админ меню AlmaU Shop:', reply_markup=inline_keyboard_faq_admin())
    await state.reset_state()


######################### КОНЕЦ Добавление нового FAQ в главном меню КОНЕЦ ############################################

######################### Изменение FAQ в главном меню #############################################
@dp.callback_query_handler(text='edit_main_faq', state=None)
async def callback_inline_edit_main_faq(call: CallbackQuery):
    logging.info(f'User({call.message.chat.id}) нажал на кнопку {call.data}')
    await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                text='Выберите кнопку для изменения:',
                                reply_markup=await inline_keyboard_edit_main_faq())
    await EditMainFaq.button_name.set()


@dp.callback_query_handler(main_faq_edit_callback.filter(), state=EditMainFaq.button_name)
async def callback_inline_edit_main_faq_choice_step(call: CallbackQuery, state: FSMContext, callback_data: dict):
    logging.info(f'User({call.message.chat.id}) нажал на кнопку {call.data}')
    id = callback_data.get('callback_id')
    db_request = await db.main_faq_select_question_and_answer(id)
    question = db_request['question']
    answer = db_request['answer']
    await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                text=f'Выберите, что нужно изменить:\n'
                                     f'<u>Вопрос</u> - {question}\n'
                                     f'<u>Ответ</u> - {answer}',
                                reply_markup=inline_keyboard_edit_main_faq_choice(), parse_mode='HTML')
    await state.update_data(question_text=question, answer_text=answer, user_id=call.message.chat.id, faq_id=id)
    await EditMainFaq.choice.set()


@dp.callback_query_handler(text='edit_main_faq_q', state=EditMainFaq.choice)
async def edit_main_faq_choice_step_question(call: CallbackQuery, state: FSMContext):
    logging.info(f'User({call.message.chat.id}) нажал на кнопку {call.data}')
    await bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id)  # Убирает инлайн клавиатуру
    await bot.send_message(chat_id=call.message.chat.id,
                           text='Напишите на какой текст изменить вопрос')
    await EditMainFaq.question_confirm.set()


@dp.message_handler(content_types=ContentType.ANY, state=EditMainFaq.question_confirm)
async def edit_main_faq_choice_step_question_final(message: types.Message, state: FSMContext):
    if message.content_type == 'text':
        if len(message.text) <= 300:
            await state.update_data(selected_item=message.text,
                                    thing_to_change='question_to_change')
            data = await state.get_data()
            await message.answer(f'Ваш новый вопрос - {message.text}\n'
                                 f'для ответа - {data["answer_text"]}\n'
                                 f'<u>(Подтвердите изменение)</u>',
                                 reply_markup=inline_keyboard_edit_main_faq_or_cancel(), parse_mode='HTML')
            await state.reset_state(with_data=False)
        else:
            await message.reply(
                f'Ваше сообщение содержит больше количество символов = <b>{len(message.text)}</b>. Ограничение в 300 символов. Сократите количество символов и попробуйте снова',
                parse_mode='HTML')
    else:
        print(message.content_type)
        await message.reply('Ошибка - ваше сообщение должно содержать только текст\n'
                            'Повторите снова')


@dp.callback_query_handler(text='edit_main_faq_a', state=EditMainFaq.choice)
async def edit_main_faq_choice_step_answer(call: CallbackQuery, state: FSMContext):
    logging.info(f'User({call.message.chat.id}) нажал на кнопку {call.data}')
    await bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id)  # Убирает инлайн клавиатуру
    await bot.send_message(chat_id=call.message.chat.id,
                           text='Напишите на какой текст изменить ответ')
    await EditMainFaq.answer_confirm.set()


@dp.message_handler(content_types=ContentType.ANY, state=EditMainFaq.answer_confirm)
async def edit_main_faq_choice_step_answer_final(message: types.Message, state: FSMContext):
    if message.content_type == 'text':
        if len(message.text) <= 4000:
            await state.update_data(selected_item=message.text,
                                    thing_to_change='answer_to_change')
            data = await state.get_data()
            await message.answer(f'Ваш новый ответ - {data["selected_item"]}\n'
                                 f'для вопроса - {data["question_text"]}\n'
                                 f'<u>(Подтвердите изменение)</u>',
                                 reply_markup=inline_keyboard_edit_main_faq_or_cancel(), parse_mode='HTML')
            await state.reset_state(with_data=False)
        else:
            await message.reply(
                f'Ваше сообщение содержит больше количество символов = <b>{len(message.text)}</b>. Ограничение в 300 символов. Сократите количество символов и попробуйте снова',
                parse_mode='HTML')
    else:
        print(message.content_type)
        await message.reply('Ошибка - ваше сообщение должно содержать только текст\n'
                            'Повторите снова')


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
        await bot.send_message(call.message.chat.id,
                               '✅ Ваши изменения для раздела F.A.Q главного меню успешно изменены')
        await bot.send_message(chat_id=call.message.chat.id,
                               text='Админ меню F.A.Q:', reply_markup=inline_keyboard_faq_admin())
    except Exception as error:
        logging.info(f'Error - {error}')
        await bot.send_message(call.message.chat.id, f'Произошла ошибка - {error}')


@dp.callback_query_handler(text='edit_main_faq_dec', state=None)
async def edit_main_faq_choice_step_question_final_decline(call: CallbackQuery, state: FSMContext):
    logging.info(f'User({call.message.chat.id}) нажал на кнопку {call.data}')
    await bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id)  # Убирает инлайн клавиатуру
    await bot.send_message(call.message.chat.id, '❌ Отмена изменения вопроса для раздела F.A.Q главного меню')
    await bot.send_message(chat_id=call.message.chat.id,
                           text='Админ меню F.A.Q:', reply_markup=inline_keyboard_faq_admin())
    await state.reset_state()


######################### КОНЕЦ Изменение FAQ в главном меню КОНЕЦ #############################################

######################### Удаление FAQ в главном меню #############################################
@dp.callback_query_handler(text='delete_main_faq', state=None)
async def callback_inline_delete_main_faq(call: CallbackQuery, state: FSMContext):
    logging.info(f'User({call.message.chat.id}) нажал на кнопку {call.data}')
    await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                text='Выберите кнопку для удаление:',
                                reply_markup=await inline_keyboard_delete_main_faq())
    await DeleteMainFaq.question.set()


@dp.callback_query_handler(main_faq_delete_callback.filter(), state=DeleteMainFaq.question)
async def callback_inline_delete_main_faq_final(call: CallbackQuery, state: FSMContext, callback_data: dict):
    logging.info(f'User({call.message.chat.id}) нажал на кнопку {call.data}')
    id = callback_data.get('callback_id')
    question = (await db.main_faq_select_question_and_answer(id))['question']
    await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                text=f'Вы точно уверены, что хотите удалить кнопку <b>{question}</b>:',
                                reply_markup=cancel_or_delete_main_faq())
    await state.update_data(question_text=question, user_id=call.message.chat.id)
    await DeleteMainFaq.confirm_delete.set()


# Удаление FAQ AlmaU Shop из базы данных
@dp.callback_query_handler(text='delete_main_faq', state=DeleteMainFaq.confirm_delete)
async def callback_inline_delete_main_faq_delete_step(call: CallbackQuery, state: FSMContext):
    try:
        data = await state.get_data()
        await db.delete_main_faq_button(data["question_text"])
        await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                    text=f'Указанный F.A.Q - <b>{data["question_text"]}</b> был успешно удален',
                                    parse_mode='HTML')
        await bot.send_message(chat_id=call.message.chat.id,
                               text='Админ меню F.A.Q:', reply_markup=inline_keyboard_faq_admin())
        await state.reset_state()
        logging.info(f'User({call.message.chat.id}) удалил FAQ главного меню для {data["question_text"]}')
    except Exception as e:
        await call.message.answer(f'Ошибка FAQ главного меню не удален, (Ошибка - {e})')
        logging.info(f'Ошибка - {e}')


# отмена
@dp.callback_query_handler(text='cancel_del_main_faq', state=DeleteMainFaq.confirm_delete)
async def callback_inline_cancel_delete_main_faq(call: CallbackQuery, state: FSMContext):
    logging.info(f'User({call.message.chat.id}) нажал на кнопку {call.data}')
    await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                text='❌ Отмена удаления вопроса F.A.Q главного меню')
    await bot.send_message(chat_id=call.message.chat.id,
                           text='Админ меню F.A.Q:', reply_markup=inline_keyboard_faq_admin())
    await state.reset_state()


######################### КОНЕЦ Удаления FAQ в главном меню КОНЕЦ #############################################


#### Возвращение в админ меню FAQ
@dp.callback_query_handler(text='back_to_admin_faq', state=['*'])
async def callback_inline_delete_faq_almaushop_back(call: CallbackQuery, state: FSMContext):
    logging.info(f'User({call.message.chat.id}) нажал на кнопку {call.data}')
    await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                text='Админ меню F.A.Q:', reply_markup=inline_keyboard_faq_admin())
    await state.reset_state()
