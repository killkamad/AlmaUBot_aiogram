import logging
from aiogram.utils import exceptions
from aiogram import types
from aiogram.types import CallbackQuery, ContentType
from aiogram.dispatcher import FSMContext
from loader import dp, bot
from utils.delete_messages import bot_delete_messages

# Импорт клавиатур
from keyboards.inline.admin_buttons import inline_keyboard_admin, cancel_or_send_academic_calendar, \
    cancel_academic_calendar, inline_keyboard_almau_shop_admin, inline_keyboard_schedule_admin

# Импортирование функций из БД контроллера
from utils import db_api as db

# Импорт стейтов
from states.admin import SendAcademCalendar

from utils.misc import rate_limit


# Вход в главное админ меню
@rate_limit(5, 'admin')
@dp.message_handler(commands=['admin'])
async def admin_menu(message):
    try:
        if await db.check_role(message.chat.id, 'admin') == 'admin':
            logging.info(f'User({message.chat.id}) вошел в админ меню')
            users = await db.count_users()
            await bot.send_message(message.chat.id, f'Меню Админа:\nКоличество пользователей = {users}\n',
                                   reply_markup=inline_keyboard_admin())
        else:
            await bot.send_message(message.chat.id, 'Недостаточный уровень доступа')
            logging.info(f'User({message.chat.id}) попытался войти в админ меню')
    except Exception as e:
        logging.info(f'Ошибка - {e}')


# Выход из любого state командой /cancel
@dp.message_handler(commands=['cancel'], state=['*'])
async def cancel_from_anywhere(message: types.Message, state: FSMContext):
    await bot.send_message(message.chat.id, 'Успешно отменено')
    await state.reset_state()


# Переход в Админ меню для Расписания
@dp.callback_query_handler(text_contains='schedule_admin_menu')
async def schedule_admin_menu(call: CallbackQuery):
    logging.info(f'User({call.message.chat.id}) вошел в админ меню Расписания, call.data - {call.data}')
    await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                text='Админ меню Расписания:', reply_markup=inline_keyboard_schedule_admin())


# Переход Админ меню для Almau shop
@dp.callback_query_handler(text_contains='almaushop_admin_menu')
async def almaushop_admin_menu(call: CallbackQuery):
    logging.info(f'User({call.message.chat.id}) вошел в админ меню AlmaU Shop, call.data - {call.data}')
    await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                text='Админ меню AlmaU Shop:', reply_markup=inline_keyboard_almau_shop_admin())


############## Академ календарь ####################################################################################
# Запрос академ календаря
@dp.callback_query_handler(text='send_academic_calendar', state=None)
async def callback_send_academic_calendar(call: CallbackQuery):
    logging.info(f'User({call.message.chat.id}) нажал на кнопку {call.data}')
    await call.message.answer('Отправьте файл академического календаря', reply_markup=cancel_academic_calendar())
    await SendAcademCalendar.send_file.set()


# Проверка академ календаря на то что он файл
@dp.message_handler(content_types=ContentType.ANY, state=SendAcademCalendar.send_file)
async def message_academic_calendar_send_file(message: types.Message, state: FSMContext):
    if message.content_type == 'document':
        await state.update_data(file_id=message.document.file_id, user_id=message.chat.id)
        data = await state.get_data()
        await bot.send_document(message.chat.id, data["file_id"], caption="Отправить этот документ?",
                                reply_markup=cancel_or_send_academic_calendar())
        await state.reset_state(with_data=False)
    else:
        await message.answer('Ошибка - вы отправили не документ\nПовторите Отправление файла')


# Отправка академ календаря в базу данных
@dp.callback_query_handler(text='send_academic_calendar_to_base', state=None)
async def callback_inline_send_academic_calendar(call: CallbackQuery, state: FSMContext):
    try:
        data = await state.get_data()
        # await bot_delete_messages(call.message, 2)
        await db.add_academic_calendar_data(data['user_id'], data['file_id'])
        await bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id)
        # await bot.delete_message(call.message.chat.id, call.message.message_id)
        await call.message.answer('<b>Академический календарь</b> отправлен', parse_mode='HTML')
        logging.info(f'User({call.message.chat.id}) отправил академ календарь')
    except Exception as e:
        await call.message.answer(f'Ошибка Академический календарь не отправлен, (Ошибка - {e})')
        print(e)


# Отмена первого шага отправки календаря
@dp.callback_query_handler(text='cancel_step_academic_calendar', state=['*'])
async def callback_inline_cancel_step_academic_calendar(call: CallbackQuery, state: FSMContext):
    logging.info(f'User({call.message.chat.id}) нажал на кнопку {call.data}')
    await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                text='<b>Отправка Академического календаря отменена</b>', parse_mode='HTML')
    await state.reset_state()


# Отмена отправки календаря
@dp.callback_query_handler(text_contains='cancel_academic_calendar')
async def callback_inline_cancel_acdemic_calendar(call: CallbackQuery, state: FSMContext):
    logging.info(f'User({call.message.chat.id}) отменил отправку Академического календаря call.data - {call.data}')
    await bot_delete_messages(call.message, 4)
    await bot.delete_message(call.message.chat.id, call.message.message_id)
    await call.message.answer('<b>Отправка Академического календаря отменена</b>', parse_mode='HTML')
    await state.reset_state()


############## КОНЕЦ Академ календарь КОНЕЦ ###########################################################################

# Кнопка возвращения из админ меню almaushop и расписания обратно в главное админ меню
@dp.callback_query_handler(text_contains='back_to_admin_menu')
async def callback_inline_back_to_admin_menu(call: CallbackQuery):
    try:
        if await db.check_role(call.message.chat.id, 'admin') == 'admin':
            logging.info(f'User({call.message.chat.id}) вернулся в админ меню')
            users = await db.count_users()
            await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                        text=f'Меню Админа:\nКоличество пользователей = {users}\n',
                                        reply_markup=inline_keyboard_admin())
        else:
            await bot.send_message(call.message.chat.id, 'Недостаточный уровень доступа')
            logging.info(f'User({call.message.chat.id}) попытался войти в админ меню')
    except Exception as e:
        logging.info(f'Ошибка - {e}')
