import logging

# Импорт библиотек aiogram
from aiogram.utils import exceptions
from aiogram import types
from aiogram.types import CallbackQuery, ContentType
from aiogram.dispatcher import FSMContext

from loader import dp, bot

# Импорт клавиатур
from keyboards.inline import inline_keyboard_users_admin_roles, inline_keyboard_users_admin, \
    inline_keyboard_users_admin_roles_accept_decline, inline_keyboard_select_last_ten_users, back_to_last_ten_users, \
    inline_keyboard_cancel_users_role_change
from keyboards.inline.callback_datas import last_ten_users_callback

# Импортирование функций из БД контроллера
from utils import db_api as db

# Импорт стейтов
from states.admin import UpdateUserRole
import aiogram.utils.markdown as fmt
from utils.misc import rate_limit
from utils.delete_inline_buttons import delete_inline_buttons_in_dialogue


@dp.callback_query_handler(text='edit_users_role', state=None)
async def callback_inline_edit_users_role(call: CallbackQuery):
    logging.info(f'User({call.message.chat.id}) нажал на кнопку {call.data}')
    await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                text='- Для успешного изменения роли, пользователь должен зарегистрировать свой номер командой /phone_reg .\n'
                                     '- Если пользователь зарегистрировал свой номер отправте его номер телефона с плюсом например(+77073040120), Или отправте как контакт (нажав на скрепку слева снизу вашего смартфона):\n',
                                reply_markup=inline_keyboard_cancel_users_role_change())
    await UpdateUserRole.phone.set()
    await call.answer()


@dp.message_handler(content_types=ContentType.CONTACT, state=UpdateUserRole.phone)
async def register_user_phone_next(message: types.Message, state: FSMContext):
    await delete_inline_buttons_in_dialogue(message)
    logging.info(f"User({message.chat.id}) ввел правильный номер {message.contact.phone_number}")
    phone = message.contact.phone_number
    if phone.startswith("+"):
        phone = phone
    else:
        phone = f"+{phone}"
    if await db.check_phone_in_users(phone):
        role_at_the_moment = await db.check_role_for_admin(phone)
        await message.reply(f"✅ Номер телефона получен.\n"
                            f"В данный момент этот пользователь имеет роль - {role_at_the_moment}\n"
                            f"Выберите роль, на которую вы хотите изменить:",
                            reply_markup=inline_keyboard_users_admin_roles())
        await state.update_data(phone=phone, role_at_the_moment=role_at_the_moment)
        await UpdateUserRole.role.set()
    else:
        await message.reply('В базе данных нету пользователя с таким номером телефона.\n'
                            'Пусть данный пользователь повторно пройдет регистрацию номера в боте с помощью команды - /phone_reg',
                            reply_markup=inline_keyboard_cancel_users_role_change())


@dp.message_handler(content_types=ContentType.ANY, state=UpdateUserRole.phone)
async def callback_inline_edit_users_role_phone(message: types.Message, state: FSMContext):
    await delete_inline_buttons_in_dialogue(message)
    logging.info(message.text)
    if message.content_type == 'text':
        if len(message.text) == 12:
            if await db.check_phone_in_users(message.text):
                role_at_the_moment = await db.check_role_for_admin(message.text)
                await message.reply(f"✅ Номер телефона получен.\n"
                                    f"В данный момент этот пользователь имеет роль - {role_at_the_moment}\n"
                                    f"Выберите роль, на которую вы хотите изменить:",
                                    reply_markup=inline_keyboard_users_admin_roles())
                await state.update_data(phone=message.text, role_at_the_moment=role_at_the_moment)
                await UpdateUserRole.role.set()
            else:
                await message.reply('В базе данных нету пользователя с таким номером телефона.\n'
                                    'Пусть данный пользователь повторно пройдет регистрацию номера в боте с помощью команды - /phone_reg',
                                    reply_markup=inline_keyboard_cancel_users_role_change())
        else:
            await message.reply(
                f'Вы отправили не правильный номер, номер должен иметь 12 символов включая знак "+", отправленный номер содержит = <b>{len(message.text)}</b> символов.\n'
                f'Попробуйте снова отправить номер',
                parse_mode='HTML',
                reply_markup=inline_keyboard_cancel_users_role_change())
    else:
        await message.reply(f'Ошибка ваше тип сообщения = {message.content_type}\n'
                            f'Ваше сообщение должно содержать только текст\n'
                            'Повторите снова',
                            reply_markup=inline_keyboard_cancel_users_role_change())


# Хендлер для ролей
@dp.callback_query_handler(text=['admin_role', 'library_admin_role', 'marketing_admin_role', 'advisor_role'],
                           state=UpdateUserRole.role)
async def callback_inline_edit_users_role_giving(call: CallbackQuery, state: FSMContext):
    logging.info(f'User({call.message.chat.id}) нажал на кнопку {call.data}')
    data = await state.get_data()
    user_role = ''
    if call.data == "admin_role":
        await state.update_data(role='admin')
        user_role = 'admin'
    if call.data == "library_admin_role":
        await state.update_data(role='library_admin')
        user_role = 'library_admin'
    if call.data == "marketing_admin_role":
        await state.update_data(role='marketing_admin')
        user_role = 'marketing_admin'
    if call.data == "advisor_role":
        await state.update_data(role='advisor_admin')
        user_role = 'advisor_admin'
    message_text = f'Подтвердите изменение роли для пользователя {data["phone"]}\n' \
                   f'Роль - {data["role_at_the_moment"]}, будет изменена на {user_role} ↘'
    await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                text=message_text, reply_markup=inline_keyboard_users_admin_roles_accept_decline())
    await UpdateUserRole.confirm.set()
    await call.answer()


@dp.callback_query_handler(text='admin_role_edit_accept', state=UpdateUserRole.confirm)
async def callback_inline_edit_users_role_giving_accept(call: CallbackQuery, state: FSMContext):
    logging.info(f'User({call.message.chat.id}) нажал на кнопку {call.data}')
    data = await state.get_data()
    await db.edit_user_role(data["role"], data["phone"])
    text = f'Успешно изменена роль пользователю с номером {data["phone"]} на роль - {data["role"]}'
    await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=text)
    await bot.send_message(chat_id=call.message.chat.id, text='Админ меню Пользователи:',
                           reply_markup=inline_keyboard_users_admin())
    await state.reset_state()
    await call.answer()


# Хендлер для отмены выдачи роли
@dp.callback_query_handler(text=['cancel_role_choice', 'admin_role_edit_decline'], state=['*'])
async def callback_inline_edit_users_role_cancel(call: CallbackQuery, state: FSMContext):
    logging.info(f'User({call.message.chat.id}) нажал на кнопку {call.data}')
    await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                text='Обновление роли отменено, возвращение в Админ меню пользователи\n'
                                     'Админ меню Пользователи:', reply_markup=inline_keyboard_users_admin())
    await state.reset_state()
    await call.answer()


@dp.callback_query_handler(text='back_to_users_admin', state=None)
async def callback_inline_last_ten_users_db(call: CallbackQuery):
    logging.info(f'User({call.message.chat.id}) нажал на кнопку {call.data}')
    await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                text='Админ меню Пользователи:', reply_markup=inline_keyboard_users_admin())
    await call.answer()


#################################### ВЫВОД 10 последний человек ####################################
@dp.callback_query_handler(text=['show_ten_last_users', 'back_to_last_ten_users'], state=None)
async def callback_inline_last_ten_users_db(call: CallbackQuery):
    logging.info(f'User({call.message.chat.id}) нажал на кнопку {call.data}')
    await bot.edit_message_text(chat_id=call.message.chat.id,
                                message_id=call.message.message_id,
                                text='10 Последний пользователей',
                                reply_markup=await inline_keyboard_select_last_ten_users())
    await call.answer()


@dp.callback_query_handler(last_ten_users_callback.filter(), state=None)
async def callback_inline_edit_main_faq_choice_step(call: CallbackQuery, callback_data: dict):
    logging.info(f'User({call.message.chat.id}) нажал на кнопку {call.data}')
    idt = callback_data.get('telegram_id')
    db_find_user = await db.find_user_by_telegram_id(idt)
    date_time = db_find_user["date_time"].strftime("%d-%m-%Y")
    text = f'<i>Телефон</i> - {fmt.quote_html(db_find_user["phone"])},\n' \
           f'<i>ID</i> - {fmt.quote_html(db_find_user["idt"])},\n' \
           f'<i>Username</i> - {fmt.quote_html(db_find_user["username"])},\n' \
           f'<i>Имя</i> - {fmt.quote_html(db_find_user["lastname"])},\n' \
           f'<i>Фамилия</i> - {fmt.quote_html(db_find_user["firstname"])},\n' \
           f'<i>Роль</i> - {fmt.quote_html(db_find_user["role"])},\n' \
           f'<i>Дата присоединения</i> - {date_time}'
    await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                text=text,
                                reply_markup=back_to_last_ten_users(), parse_mode='HTML')
    await call.answer()
