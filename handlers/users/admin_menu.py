import ast
import logging

from aiogram.utils import exceptions
from aiogram import types
from aiogram.types import CallbackQuery, ContentType
from loader import dp, bot
from keyboards.inline.admin_buttons import inline_keyboard_admin, inline_keyboard_massive_send_all, \
    inline_keyboard_cancel_or_send, inline_keyboard_cancel, cancel_or_send_schedule, inline_keyboard_update_schedule, \
    cancel_or_update_schedule, inline_keyboard_delete_schedule, cancel_or_delete_schedule, \
    cancel_or_send_academic_calendar, cancel_academic_calendar
import asyncio
# Импортирование функций из БД контроллера
from utils import db_api as db
from utils.almaushop_parser import AlmauShop

from utils.delete_messages import bot_delete_messages
from aiogram.dispatcher import FSMContext
from states.admin import SendAll, SendScheduleToBot, UpdateSchedule, DeleteSchedule, SendAcademCalendar

from utils.misc import rate_limit


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


@dp.callback_query_handler(text='send_all', state=None)
async def callback_inline_send_all(call: CallbackQuery):
    logging.info(f'User({call.message.chat.id}) нажал на кнопку 📣 Рассылка')
    await call.message.answer('Напишите текст сообщения для массовой рассылки:')
    await SendAll.message_text.set()


@dp.callback_query_handler(text='add_photo_mass')
async def callback_inline_add_photo_mass(call: CallbackQuery):
    logging.info(f'User({call.message.chat.id}) нажал на кнопку ➕ Добавить фото или документ')
    await bot.send_message(call.message.chat.id, 'Прикрепите фото к сообщению')
    await SendAll.message_photo.set()


@dp.callback_query_handler(text='cancel')
async def callback_inline_cancel(call: CallbackQuery, state: FSMContext):
    logging.info(f'User({call.message.chat.id}) нажал на кнопку ❌ Отмена')
    await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                text='ОТМЕНЕНО')
    await bot_delete_messages(call.message, 3)
    await state.reset_state()


@dp.message_handler(content_types=ContentType.ANY, state=SendAll.message_text)
async def message_send_text(message: types.Message, state: FSMContext):
    if message.content_type == 'text':
        if len(message.text) <= 990:
            await state.update_data(message_text_all=message.text)
            message_txt = 'Ваше сообщение:\n' + message.text + '\n (*ВЫ УВЕРЕНЫ?*)'
            await bot.send_message(message.chat.id, message_txt, reply_markup=inline_keyboard_massive_send_all())
            await state.reset_state(with_data=False)
        else:
            await bot.send_message(message.chat.id,
                                   f'Ваше сообщение содержит больше количество символов = <b>{len(message.text)}</b>. Бот может обработать максимум 1000 символов. Сократите количество и попробуйте снова',
                                   parse_mode='HTML')
    else:
        print(message.content_type)
        await bot.send_message(message.chat.id,
                               'Ошибка - ваще сообщение должно содержать только текст\nНапишите текст сообщения для массовой рассылки:')


@dp.callback_query_handler(text='send_send_to_all')
async def callback_inline_send_send_all(call: CallbackQuery, state: FSMContext):
    logging.info(f'User({call.message.chat.id}) нажал на кнопку "✔ Отправить" всем пользователям')
    request = 0
    data = await state.get_data()
    if len(data) == 2:
        await bot_delete_messages(call.message, 5)
        await bot.delete_message(call.message.chat.id, call.message.message_id)
        await bot.send_message(call.message.chat.id, '<b>Массовая рассылка отправлена:</b>', parse_mode='HTML')
        users = await db.select_users()
        for i in users:
            try:
                try:
                    await bot.send_photo(i, data['photo_id'], caption=data['message_text_all'])
                    # await bot.send_document(i, data['document_id'])
                    # await bot.send_message(i, data['message_text_all'])
                except Exception as e:
                    await bot.send_document(i, data['document_id'], caption=data['message_text_all'])
                    logging.info(e)
                request += 1
                await asyncio.sleep(0.5)
                if request % 30 == 0:
                    await asyncio.sleep(2)
                    request = 0
            except Exception as e:
                logging.info(f'Наверно бот заблокирован {e}')

        await state.reset_state()
    else:
        await bot_delete_messages(call.message, 2)
        await bot.delete_message(call.message.chat.id, call.message.message_id)
        await bot.send_message(call.message.chat.id, '<b>Массовая рассылка отправлена:</b>', parse_mode='HTML')
        users = await db.select_users()
        for i in users:
            try:
                await bot.send_message(i, data['message_text_all'])
                request += 1
                await asyncio.sleep(0.5)
                if request % 30 == 0:
                    await asyncio.sleep(2)
                    request = 0
            except Exception as e:
                logging.info(f'Наверно бот заблокирован - {e}')
        await state.reset_state()


# Получение медиа файлы от пользователя для массовой рассылки
@dp.message_handler(content_types=ContentType.ANY, state=SendAll.message_photo)
async def message_send_photo(message: types.Message, state: FSMContext):
    if message.content_type == 'photo':
        await state.update_data(photo_id=message.photo[-1].file_id)
        logging.info(message.photo[-1].file_id)
        data = await state.get_data()
        message_txt = 'Ваше сообщение:\n' + data['message_text_all'] + '\n (*ВЫ УВЕРЕНЫ?*)'
        await bot.send_message(message.chat.id, message_txt, reply_markup=inline_keyboard_cancel_or_send())
        await state.reset_state(with_data=False)
    elif message.content_type == 'document':
        await state.update_data(document_id=message.document.file_id)
        logging.info(message.document.file_id)
        data = await state.get_data()
        message_txt = 'Ваше сообщение:\n' + data['message_text_all'] + '\n (*ВЫ УВЕРЕНЫ?*)'
        await bot.send_message(message.chat.id, message_txt, reply_markup=inline_keyboard_cancel_or_send())
        await state.reset_state(with_data=False)
    else:
        print(message.content_type)
        await bot.send_message(message.chat.id,
                               'Ошибка - отправьте картинку как "Фото", не как "Файл"')


#### Отправка расписания ####
@dp.callback_query_handler(text='send_schedule_bot', state=None)
async def callback_inline_send_schedule_bot(call: CallbackQuery):
    logging.info(f'User({call.message.chat.id}) нажал на кнопку {call.data}')
    await call.message.answer('Напишите название для кнопки, например (3 Курс):', reply_markup=inline_keyboard_cancel())
    await SendScheduleToBot.button_name.set()


#### Обновление расписания ####
@dp.callback_query_handler(text='update_schedule_bot', state=None)
async def callback_inline_update_schedule_bot(call: CallbackQuery):
    logging.info(f'User({call.message.chat.id}) нажал на кнопку {call.data}')
    await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                text='Выберите кнопку для изменения:',
                                reply_markup=await inline_keyboard_update_schedule())
    await UpdateSchedule.button_name.set()


#### ОТМЕНА Обновление расписания
@dp.callback_query_handler(text='cancel_update_step', state=UpdateSchedule.button_name)
async def callback_inline_cancel_update_schedule_bot(call: CallbackQuery, state: FSMContext):
    logging.info(f'User({call.message.chat.id}) нажал на кнопку {call.data}')
    users = await db.count_users()
    await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                text=f'Меню Админа:\n- Количество пользователей = {users}\n'
                                     f'- Рассылка - Разослать сообщение всем пользователям\n'
                                     f'- Отправить расписание - отправить расписание боту',
                                reply_markup=inline_keyboard_admin())
    await state.reset_state()


@dp.callback_query_handler(text_contains="['upd_sch'", state=UpdateSchedule.button_name)
async def callback_inline_update_schedule(call: CallbackQuery, state: FSMContext):
    logging.info(f'User({call.message.chat.id}) нажал на кнопку {call.data}')
    schedule_button_name = ast.literal_eval(call.data)[1]
    await state.update_data(button_name=schedule_button_name, user_id=call.message.chat.id)
    await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                text=f'Отправьте файл с расписанием для кнопки <b>{schedule_button_name}</b>:',
                                parse_mode='HTML')
    await UpdateSchedule.send_file.set()


@dp.message_handler(content_types=ContentType.ANY, state=UpdateSchedule.send_file)
async def change_schedule_id(message: types.Message, state: FSMContext):
    # data = await state.get_data()
    # logging.info(data)
    await UpdateSchedule.send_file.set()
    if message.content_type == 'document':
        await state.update_data(file_id=message.document.file_id)
        data = await state.get_data()
        txt = f'Название кнопки: <b>{data["button_name"]}</b>'
        await bot.send_document(message.chat.id, data["file_id"], caption=txt,
                                reply_markup=cancel_or_update_schedule())
        await state.reset_state(with_data=False)
    else:
        await bot.send_message(message.chat.id,
                               'Ошибка - вы отправили не документ\nПовторите Отправление файла с расписанием',
                               reply_markup=inline_keyboard_cancel())


#### Удаление расписания ####
@dp.callback_query_handler(text='delete_schedule_bot', state=None)
async def callback_inline_send_schedule_bot(call: CallbackQuery):
    logging.info(f'User({call.message.chat.id}) нажал на кнопку {call.data}')
    await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                text='Выберите кнопку для удаление:',
                                reply_markup=await inline_keyboard_delete_schedule())
    await DeleteSchedule.button_name.set()


#### ОТМЕНА Удаления расписания
@dp.callback_query_handler(text='cancel_delete_step', state=DeleteSchedule.button_name)
async def callback_inline_cancel_update_schedule_bot(call: CallbackQuery, state: FSMContext):
    logging.info(f'User({call.message.chat.id}) нажал на кнопку {call.data}')
    users = await db.count_users()
    await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                text=f'Меню Админа:\n- Количество пользователей = {users}\n'
                                     f'- Рассылка - Разослать сообщение всем пользователям\n'
                                     f'- Отправить расписание - отправить расписание боту',
                                reply_markup=inline_keyboard_admin())
    await state.reset_state()


@dp.callback_query_handler(text_contains="['del_sch'", state=DeleteSchedule.button_name)
async def callback_inline_update_schedule(call: CallbackQuery, state: FSMContext):
    logging.info(f'User({call.message.chat.id}) нажал на кнопку {call.data}')
    schedule_button_name = ast.literal_eval(call.data)[1]
    await state.update_data(button_name=schedule_button_name, user_id=call.message.chat.id)
    await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                text=f'Вы точно уверены, что хотите удалить кнопку расписания для <b>{schedule_button_name}</b>:',
                                parse_mode='HTML', reply_markup=cancel_or_delete_schedule())
    await DeleteSchedule.confirm_delete.set()


@dp.callback_query_handler(text='cancel_step', state=['*'])
async def callback_inline_cancel_step(call: CallbackQuery, state: FSMContext):
    logging.info(f'User({call.message.chat.id}) нажал на кнопку {call.data}')
    await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                text='<b>Отправка расписания отменена</b>', parse_mode='HTML')
    await state.reset_state()


# Проверка сообщения на текст, если текст, то сохраняет это сообщение и айди в state
@dp.message_handler(content_types=ContentType.ANY, state=SendScheduleToBot.button_name)
async def message_send_button_name(message: types.Message, state: FSMContext):
    if message.content_type == 'text':
        await state.update_data(button_name=message.text.lower(),
                                user_id=message.chat.id)
        await bot.send_message(message.chat.id, 'Отправьте файл с расписанием', reply_markup=inline_keyboard_cancel())
        await SendScheduleToBot.send_file.set()
    else:
        print(message.content_type)
        await bot.send_message(message.chat.id,
                               'Ошибка - название может содержать только текст\nПовторите название для кнопки, например (3 Курс):')


# Проверка если отправлен файл, то сохраняет айди файла в state
@dp.message_handler(content_types=ContentType.ANY, state=SendScheduleToBot.send_file)
async def message_schedule_send_file(message: types.Message, state: FSMContext):
    if message.content_type == 'document':
        await state.update_data(file_id=message.document.file_id)
        data = await state.get_data()
        txt = f'Название кнопки будет: {data["button_name"]}'
        await bot.send_document(message.chat.id, data["file_id"], caption=txt,
                                reply_markup=cancel_or_send_schedule())
        await state.reset_state(with_data=False)
    else:
        await message.answer('Ошибка - вы отправили не документ\nПовторите Отправление файла с расписанием')


# Отправление расписания в базу данных
@dp.callback_query_handler(text='send_schedule', state=None)
async def callback_inline_send_schedule(call: CallbackQuery, state: FSMContext):
    try:
        data = await state.get_data()
        await bot_delete_messages(call.message, 4)
        await db.add_schedule_data(data['user_id'], data['file_id'], data["button_name"])
        await bot.delete_message(call.message.chat.id, call.message.message_id)
        await call.message.answer(f'Расписание для <b>{data["button_name"]}</b> отправлено', parse_mode='HTML')
        logging.info(f'User({call.message.chat.id}) отправил расписание для {data["button_name"]}')
    except Exception as e:
        await call.message.answer(f'Ошибка расписание не отправлено, (Ошибка - {e})')
        print(e)


# Успешное обновление расписания в базе данных
@dp.callback_query_handler(text='update_schedule_button', state=None)
async def callback_inline_send_schedule(call: CallbackQuery, state: FSMContext):
    try:
        data = await state.get_data()
        await bot_delete_messages(call.message, 2)
        await db.update_schedule_data(data['user_id'], data['file_id'], data["button_name"])
        await bot.delete_message(call.message.chat.id, call.message.message_id)
        await call.message.answer(f'Расписание для <b>{data["button_name"]}</b> успешно обновлено', parse_mode='HTML')
        logging.info(f'User({call.message.chat.id}) обновил расписание для {data["button_name"]}')
        users = await db.select_users()
        for i in users:
            try:
                await bot.send_message(i, f'Внимание, расписание для <b>{data["button_name"]}</b> было обновлено',
                                       parse_mode='HTML')
            except Exception as e:
                logging.info(f'Наверно бот заблокирован {e}')
        await admin_menu(call.message)

    except Exception as e:
        await call.message.answer(f'Ошибка расписание не обновлено, (Ошибка - {e})')
        logging.info(f'Ошибка - {e}')


# Удаление расписания из базы данных
@dp.callback_query_handler(text='delete_schedule_button', state=DeleteSchedule.confirm_delete)
async def callback_inline_send_schedule(call: CallbackQuery, state: FSMContext):
    try:
        data = await state.get_data()
        # await bot_delete_messages(call.message, 4)
        await db.delete_schedule_button(data["button_name"])
        # await bot.delete_message(call.message.chat.id, call.message.message_id)
        await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                    text=f'Расписание для <b>{data["button_name"]}</b> успешно удалено из базы данных',
                                    parse_mode='HTML')
        await admin_menu(call.message)
        # await call.message.answer(f'Расписание для <b>{data["button_name"]}</b> успешно удалено из базы данных',
        #                           parse_mode='HTML')
        await state.reset_state()
        logging.info(f'User({call.message.chat.id}) удалил расписание для {data["button_name"]}')
    except Exception as e:
        await call.message.answer(f'Ошибка расписание не удалено, (Ошибка - {e})')
        logging.info(f'Ошибка - {e}')


@dp.callback_query_handler(text_contains='cancel_schedule')
async def callback_inline_cancel_schedule(call: CallbackQuery, state: FSMContext):
    logging.info(f'User({call.message.chat.id}) отменил отправку расписания call.data - {call.data}')
    await bot_delete_messages(call.message, 4)
    await bot.delete_message(call.message.chat.id, call.message.message_id)
    await call.message.answer('<b>Отправка расписания отменена</b>', parse_mode='HTML')
    await state.reset_state()


@dp.callback_query_handler(text_contains='cancel_update_schedule')
async def callback_inline_cancel_update_schedule(call: CallbackQuery, state: FSMContext):
    logging.info(f'User({call.message.chat.id}) отменил обновления расписания call.data - {call.data}')
    await bot_delete_messages(call.message, 2)
    await bot.delete_message(call.message.chat.id, call.message.message_id)
    await call.message.answer('<b>Обновление|Изменение отменено</b>', parse_mode='HTML')
    await admin_menu(call.message)
    await state.reset_state()


@dp.callback_query_handler(text_contains='cancel_delete_schedule', state=DeleteSchedule.confirm_delete)
async def callback_inline_cancel_delete_schedule(call: CallbackQuery, state: FSMContext):
    logging.info(f'User({call.message.chat.id}) отменил удаление расписания call.data - {call.data}')
    await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                text='<b>Удаление отмененено</b>', parse_mode='HTML')
    # await call.message.answer('<b>Удаление отмененено</b>', parse_mode='HTML')
    await admin_menu(call.message)
    await state.reset_state()


# Парсинг сайта almaushop.kz и загрузка данных в таблицу в БД
@dp.callback_query_handler(text_contains='update_almaushop_data')
async def callback_inline_update_almaushop_data(call: CallbackQuery):
    logging.info(f'User({call.message.chat.id}) запустил обновление данных таблицы almaushop call.data - {call.data}')
    shop = AlmauShop()
    shop.parse_page(text=shop.load_page())
    try:
        await db.clear_almaushop_table()
        for i in shop.result:
            await db.add_almau_shop_data(call.message.chat.id, i.product_name, i.price, i.currency, i.img, i.url)
        await bot.send_message(call.message.chat.id, 'Данные в таблице almau shop обновлены')
    except Exception as err:
        logging.exception(err)
        await bot.send_message(call.message.chat.id, 'Произошла ошибка')


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
