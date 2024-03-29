import asyncio
import logging
from aiogram import types
from aiogram.types import CallbackQuery, ContentType
from aiogram.dispatcher import FSMContext
from loader import dp, bot
from .admin_menu import schedule_admin_menu
from utils import delete_inline_buttons
# Импорт клавиатур
from keyboards.inline import inline_keyboard_cancel_schedule, cancel_or_send_schedule, \
    inline_keyboard_update_schedule, cancel_or_update_schedule, inline_keyboard_delete_schedule, \
    cancel_or_delete_schedule, schedule_update_callback, schedule_delete_callback, inline_keyboard_schedule_admin

# Импортирование функций из БД контроллера
from utils import db_api as db

# Импорт стейтов
from states.admin import SendScheduleToBot, UpdateSchedule, DeleteSchedule

import aiogram.utils.markdown as fmt
from utils.delete_inline_buttons import delete_inline_buttons_in_dialogue


#### Отправка расписания ####
@dp.callback_query_handler(text='send_schedule_bot', state=None)
async def callback_inline_send_schedule_bot(call: CallbackQuery):
    logging.info(f'User({call.message.chat.id}) нажал на кнопку {call.data}')
    await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                text='Напишите название для кнопки, например (3 Курс):',
                                reply_markup=inline_keyboard_cancel_schedule())
    await SendScheduleToBot.button_name.set()
    await call.answer()


#### Обновление расписания ####
@dp.callback_query_handler(text='update_schedule_bot', state=None)
async def callback_inline_update_schedule_bot(call: CallbackQuery):
    logging.info(f'User({call.message.chat.id}) нажал на кнопку {call.data}')
    await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                text='Выберите кнопку для изменения:',
                                reply_markup=await inline_keyboard_update_schedule())
    await call.answer()


#### Удаление расписания ####
@dp.callback_query_handler(text='delete_schedule_bot', state=None)
async def callback_inline_delete_schedule_bot(call: CallbackQuery):
    logging.info(f'User({call.message.chat.id}) нажал на кнопку {call.data}')
    await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                text='Выберите кнопку для удаления:',
                                reply_markup=await inline_keyboard_delete_schedule())
    await call.answer()


#### ОТМЕНА Обновление расписания
@dp.callback_query_handler(text='cancel_update_step')
async def callback_inline_cancel_update_schedule_bot(call: CallbackQuery, state: FSMContext):
    logging.info(f'User({call.message.chat.id}) нажал на кнопку {call.data}')
    await schedule_admin_menu(call)
    await state.reset_state()
    await call.answer()


# Нажатие на одну из кнопок с названием расписания, для обновления
@dp.callback_query_handler(schedule_update_callback.filter())
async def callback_inline_update_schedule(call: CallbackQuery, state: FSMContext, callback_data: dict):
    logging.info(f'User({call.message.chat.id}) нажал на кнопку {call.data}')
    schedule_id = callback_data.get('schedule_id')
    schedule_name = await db.find_schedule_name_by_id(schedule_id)
    await state.update_data(button_name=schedule_name, user_id=call.message.chat.id)
    await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                text=f'Отправьте файл с расписанием для кнопки <b>{schedule_name}</b>:',
                                parse_mode='HTML',
                                reply_markup=inline_keyboard_cancel_schedule())
    await UpdateSchedule.send_file.set()
    await call.answer()


@dp.message_handler(content_types=ContentType.ANY, state=UpdateSchedule.send_file)
async def change_schedule_id(message: types.Message, state: FSMContext):
    await delete_inline_buttons_in_dialogue(message)
    if message.content_type == 'document':
        await state.update_data(file_id=message.document.file_id)
        data = await state.get_data()
        txt = f'Название кнопки:\n' \
              f'<b>{data["button_name"]}</b>\n\n' \
              f'<i><u>Вы уверены?</u></i>'
        await bot.send_document(message.chat.id, data["file_id"], caption=txt,
                                reply_markup=cancel_or_update_schedule())
        await state.reset_state(with_data=False)
    else:
        await bot.send_message(message.chat.id,
                               'Ошибка - вы отправили не документ\n'
                               'Повторите Отправление файла с расписанием',
                               reply_markup=inline_keyboard_cancel_schedule())


#### ОТМЕНА Удаления расписания
@dp.callback_query_handler(text='cancel_delete_step', state=None)
async def callback_inline_cancel_update_schedule_bot(call: CallbackQuery, state: FSMContext):
    logging.info(f'User({call.message.chat.id}) нажал на кнопку {call.data}')
    await schedule_admin_menu(call)
    await state.reset_state()
    await call.answer()


# Нажатие на одну из кнопок с названием расписания, для удаления
@dp.callback_query_handler(schedule_delete_callback.filter(), state=None)
async def callback_inline_update_schedule(call: CallbackQuery, state: FSMContext, callback_data: dict):
    logging.info(f'User({call.message.chat.id}) нажал на кнопку {call.data}')
    schedule_id = callback_data.get('schedule_id')
    schedule_name = await db.find_schedule_name_by_id(schedule_id)
    text_delete = f"Вы хотите удалить кнопку с расписанием\n" \
                  f"<b>{schedule_name}</b>\n\n" \
                  f"<i><u>Вы уверены?</u></i>"
    await state.update_data(button_name=schedule_name, user_id=call.message.chat.id)
    await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                text=text_delete,
                                parse_mode='HTML',
                                reply_markup=cancel_or_delete_schedule())
    await DeleteSchedule.confirm_delete.set()
    await call.answer()


@dp.callback_query_handler(text='cancel_step_schedule', state=['*'])
async def callback_inline_cancel_step(call: CallbackQuery, state: FSMContext):
    logging.info(f'User({call.message.chat.id}) нажал на кнопку {call.data}')
    await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                text='<b>❌ Отправка расписания успешно отменена</b>\n'
                                     'Возврат в Админ меню Расписания:',
                                parse_mode='HTML',
                                reply_markup=inline_keyboard_schedule_admin())
    await state.reset_state()
    await call.answer()


# Проверка сообщения на текст, если текст, то сохраняет это сообщение и айди в state
@dp.message_handler(content_types=ContentType.ANY, state=SendScheduleToBot.button_name)
async def message_send_button_name(message: types.Message, state: FSMContext):
    await delete_inline_buttons_in_dialogue(message)
    if message.content_type == 'text':
        if len(message.text) <= 28:
            await state.update_data(button_name=fmt.quote_html(message.text.lower()),
                                    user_id=message.chat.id)
            await message.reply('Отправьте файл с расписанием', reply_markup=inline_keyboard_cancel_schedule())
            await SendScheduleToBot.send_file.set()
        else:
            await bot.send_message(message.chat.id,
                                   f'Ваше сообщение содержит {len(message.text)}, максимально допустимое значание 28',
                                   reply_markup=inline_keyboard_cancel_schedule())
    else:
        print(message.content_type)
        await bot.send_message(message.chat.id,
                               'Ошибка - название может содержать только текст\n'
                               'Повторите название для кнопки, например (3 Курс):',
                               reply_markup=inline_keyboard_cancel_schedule())


# Проверка если отправлен файл, то сохраняет айди файла в state
@dp.message_handler(content_types=ContentType.ANY, state=SendScheduleToBot.send_file)
async def message_schedule_send_file(message: types.Message, state: FSMContext):
    await delete_inline_buttons_in_dialogue(message)
    if message.content_type == 'document':
        await state.update_data(file_id=message.document.file_id)
        data = await state.get_data()
        txt = f'Название кнопки: {data["button_name"]}'
        await bot.send_document(message.chat.id, data["file_id"], caption=txt,
                                reply_markup=cancel_or_send_schedule())
        await state.reset_state(with_data=False)
    else:
        await bot.send_message(message.chat.id,
                               'Ошибка - вы отправили не документ\nПовторите Отправление файла с расписанием',
                               reply_markup=inline_keyboard_cancel_schedule())


# Отправление расписания в базу данных
@dp.callback_query_handler(text='send_schedule', state=None)
async def callback_inline_send_schedule(call: CallbackQuery, state: FSMContext):
    try:
        data = await state.get_data()
        await db.add_schedule_data(data['user_id'], data['file_id'], data["button_name"])
        await bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id)
        await call.message.answer(f'✅ Расписание для <b>{data["button_name"]}</b> успешно сохранено.\n'
                                  f'Админ меню Расписания:',
                                  parse_mode='HTML',
                                  reply_markup=inline_keyboard_schedule_admin())
        logging.info(f'User({call.message.chat.id}) отправил расписание для {data["button_name"]}')
        await call.answer()
    except Exception as e:
        await call.message.answer(f'Ошибка расписание не отправлено, (Ошибка - {e})')


# Успешное обновление расписания в базе данных
@dp.callback_query_handler(text='update_schedule_button', state=None)
async def callback_inline_send_schedule(call: CallbackQuery, state: FSMContext):
    request = 0
    try:
        data = await state.get_data()
        await db.update_schedule_data(data['user_id'], data['file_id'], data["button_name"])
        await bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id)
        await call.message.answer(f'✅ Расписание для <b>{data["button_name"]}</b> успешно обновлено.\n'
                                  f'Админ меню Расписания:',
                                  parse_mode='HTML',
                                  reply_markup=inline_keyboard_schedule_admin())
        logging.info(f'User({call.message.chat.id}) обновил расписание для {data["button_name"]}')
        users = await db.select_users()
        for i in users:
            try:
                await bot.send_message(i, f'Внимание, расписание для <b>{data["button_name"]}</b> было обновлено',
                                       parse_mode='HTML')
                request += 1
                await asyncio.sleep(0.5)
                if request % 30 == 0:
                    await asyncio.sleep(2)
                    request = 0
            except Exception as e:
                pass
                # logging.info(f'Ошибка Бот заблокирован {e}')
    except Exception as e:
        await call.message.answer(f'Ошибка расписание не обновлено, (Ошибка - {e})')
        logging.info(f'Ошибка - {e}')
    await call.answer()


# Удаление расписания из базы данных
@dp.callback_query_handler(text='delete_schedule_button', state=DeleteSchedule.confirm_delete)
async def callback_inline_send_schedule(call: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    await db.delete_schedule_button(data["button_name"])
    await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                text=f'✅ Расписание для <b>{data["button_name"]}</b> успешно удалено из базы данных.\n'
                                     f'Выберите кнопку для удаление:',
                                reply_markup=await inline_keyboard_delete_schedule())
    await state.reset_state()
    logging.info(f'User({call.message.chat.id}) удалил расписание для {data["button_name"]}')
    await call.answer()


@dp.callback_query_handler(text_contains='cancel_schedule')
async def callback_inline_cancel_schedule(call: CallbackQuery, state: FSMContext):
    logging.info(f'User({call.message.chat.id}) отменил отправку расписания call.data - {call.data}')
    await bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id)
    await bot.send_message(chat_id=call.message.chat.id,
                           text='<b>❌ Отправка расписания успешно отменена</b>\n'
                                'Возврат в Админ меню Расписания:',
                           parse_mode='HTML',
                           reply_markup=inline_keyboard_schedule_admin())
    await state.reset_state()
    await call.answer()


@dp.callback_query_handler(text_contains='cancel_update_schedule')
async def callback_inline_cancel_update_schedule(call: CallbackQuery, state: FSMContext):
    logging.info(f'User({call.message.chat.id}) отменил обновления расписания call.data - {call.data}')
    await bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id)
    await bot.send_message(chat_id=call.message.chat.id,
                           text='<b>❌ Обновление|Изменение отменено</b>\n'
                                'Возврат в Админ меню Расписания:',
                           parse_mode='HTML',
                           reply_markup=inline_keyboard_schedule_admin())
    await state.reset_state()
    await call.answer()


@dp.callback_query_handler(text_contains='cancel_delete_schedule', state=DeleteSchedule.confirm_delete)
async def callback_inline_cancel_delete_schedule(call: CallbackQuery, state: FSMContext):
    logging.info(f'User({call.message.chat.id}) отменил удаление расписания call.data - {call.data}')
    await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                text='<b>❌ Удаление отмененено</b>\n'
                                     'Возврат в Админ меню Расписания:',
                                parse_mode='HTML',
                                reply_markup=inline_keyboard_schedule_admin())
    # await call.message.answer('<b>Удаление отмененено</b>', parse_mode='HTML')
    # await admin_menu(call.message)
    await state.reset_state()
    await call.answer()
