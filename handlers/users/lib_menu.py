import logging
import aiogram.utils.markdown as fmt
from data.config import library_admins
from aiogram.types import CallbackQuery, ContentType
from aiogram import types

from keyboards.default import always_stay_keyboard, keyboard_library, keyboard_library_choice_db, \
    keyboard_library_send_phone
from keyboards.inline import inline_keyboard_menu
from states.library_state import EmailReg
from loader import dp, bot
from keyboards.inline.library_buttons import inline_keyboard_library_registration, inline_keyboard_send_reg_data, \
    inline_keyboard_library_el_res, inline_keyboard_library_base_kaz, inline_keyboard_cancel_lic_db_reg, \
    inline_keyboard_library_base_zarub, inline_keyboard_library_online_bib, inline_keyboard_library_choice_db
# Импортирование функций из БД контроллера
from utils import db_api as db
from utils.misc import rate_limit
from utils.json_loader import json_data
from aiogram.types import ReplyKeyboardRemove

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import aiosmtplib

from aiogram.dispatcher import FSMContext
# Библиотека регулярных выражений
import re

# Патерн регулярного выражения для проверки почты
valid_email_pattern = re.compile('(^|\s)[-a-z0-9_.]+@([-a-z0-9]+\.)+[a-z]{2,6}(\s|$)')


# Создается функция для проверки валидности почты
def is_valid_email(s):
    return valid_email_pattern.match(s) is not None


@rate_limit(1)
@dp.message_handler(
    lambda message: message.text in ['🌐 Вебсайт', '⚡ Электронные ресурсы', '☎ Контакты', '🕐 Время работы',
                                     '🎓 Онлайн курсы', '💳 Потерял(a) ID-карту', '⚠ Правила', '📰 Права читателя',
                                     '🚫 Что не разрешается', '⛔ Ответственность за нарушения'])
async def library_text_buttons_handler(message: types.Message):
    logging.info(f"User({message.chat.id}) нажал на {message.text}")
    # Кнопки БИБЛИОТЕКИ
    if message.text in ['🌐 Вебсайт', '☎ Контакты', '🕐 Время работы',
                        '🎓 Онлайн курсы', '💳 Потерял(a) ID-карту', '⚠ Правила',
                        '📰 Права читателя', '🚫 Что не разрешается', '⛔ Ответственность за нарушения']:
        button_content = await db.select_library_menu_button_content(message.text)
        await bot.send_message(chat_id=message.chat.id, text=button_content)
    elif message.text == '⚡ Электронные ресурсы':
        await bot.send_message(chat_id=message.chat.id,
                               text='Электронные ресурсы\n',
                               reply_markup=inline_keyboard_library_el_res())


@dp.callback_query_handler(text=['library_registration'])
async def callback_library_registration(call: CallbackQuery):
    await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                text='Регистрация на лицензионные базы данных\n'
                                     'Такие как:\n'
                                     '- IPR Books iprbookshop.ru\n'
                                     '- Scopus scopus.com\n'
                                     '- Web of Science webofknowledge.com\n'
                                     '- Образовательная Платформа ЮРАЙТ urait.ru\n'
                                     '- Электронно-Библиотечная Система Polpred polpred.com\n'
                                     '- Республиканская Межвузовская Электронная Библиотека rmebrk.kz',
                                reply_markup=inline_keyboard_library_registration())


# Отмена регистрации на лицензионные БД
@dp.message_handler(text='/cancel', state=[EmailReg.names, EmailReg.email, EmailReg.phone])
async def callback_cancel_lib_reg(message: types.Message, state: FSMContext):
    logging.info(f'User({message.chat.id}) отменил регистрацию на лицензионные БД')
    await bot.send_message(chat_id=message.chat.id, text='Регистрация на лицензионные базы данных была отменена',
                           reply_markup=ReplyKeyboardRemove())
    await bot.send_message(chat_id=message.chat.id,
                           text='Возвращение в меню библиотеки', reply_markup=keyboard_library())
    await state.reset_state()


# Отравка клавиатуры для выбора базы данных для регистрации
@dp.callback_query_handler(text='library_registration_button', state=None)
async def callback_library_registration_button(call: CallbackQuery):
    await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                text='Регистрация проводится путем отправки данных в библиотеку ALMAU.\n'
                                     'Если вы не можете отправить данные через бота, то вы можете зарегестроваться через сайт lib.almau.edu.kz/page/9 \n'
                                     'Выберите базу данных на которую хотите зарегистрироваться',
                                disable_web_page_preview=True,
                                reply_markup=inline_keyboard_library_choice_db())
    # await call.message.answer('Выберите базу данных на которую хотите зарегистрироваться\n',
    #                           reply_markup=keyboard_library_choice_db())
    # await EmailReg.bookbase.set()


# Сохранение выбранной базы данных и запрос ФИО
# @dp.message_handler(
#     lambda message: message.text in ['IPR Books', 'Scopus', 'Web of Science', 'ЮРАЙТ', 'Polpred', 'РМЭБ'],
#     state=EmailReg.bookbase)
@dp.callback_query_handler(text=['IPR Books', 'Scopus', 'Web of Science', 'ЮРАЙТ', 'Polpred', 'РМЭБ'])
async def callback_process_name(call: CallbackQuery, state: FSMContext):
    try:
        await bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id)
    except:
        pass
    async with state.proxy() as data:
        data['book_database'] = call.data
    await bot.edit_message_text(chat_id=call.message.chat.id,
                                message_id=call.message.message_id,
                                text=f"Вы выбрали '{call.data}'.\n"
                                     f"Напишите ваше ФИО",
                                reply_markup=inline_keyboard_cancel_lic_db_reg())
    await EmailReg.names.set()


# Сохранение ФИО и запрос Email
@dp.message_handler(state=EmailReg.names)
async def callback_process_email(message: types.Message, state: FSMContext):
    try:
        await bot.edit_message_reply_markup(message.chat.id, message.message_id - 1)
    except:
        pass
    async with state.proxy() as data:
        data['names'] = fmt.quote_html(message.text)
    await message.reply("Напишите ваш Email", reply_markup=inline_keyboard_cancel_lic_db_reg())
    await EmailReg.email.set()


# Сохранение Email и запрос номера телефона
@dp.message_handler(content_types=ContentType.TEXT, state=EmailReg.email)
async def callback_process_phone(message: types.Message, state: FSMContext):
    try:
        await bot.edit_message_reply_markup(message.chat.id, message.message_id - 1)
    except:
        pass
    if "@" in message.text:
        email = message.text.strip()
        if is_valid_email(email):
            async with state.proxy() as data:
                data['email'] = message.text
            await message.reply("Отправьте свой номер телефона", reply_markup=keyboard_library_send_phone())
            await EmailReg.phone.set()
        else:
            await message.reply("Неверный формат электронной почты, напишите правильно почту!",
                                reply_markup=inline_keyboard_cancel_lic_db_reg())
    else:
        await message.reply("Неверный формат электронной почты, напишите правильно почту!",
                            reply_markup=inline_keyboard_cancel_lic_db_reg())


# Сохранение Номера телефона и показ всех записанных данных, с вариантами 'отправить' или 'отменить'
@dp.message_handler(content_types=ContentType.CONTACT, state=EmailReg.phone)
async def send_license_db_reg_data_to_email(message: types.Message, state: FSMContext):
    if message.chat.id == message.contact.user_id:
        logging.info(f"User({message.chat.id}) ввел правильный номер")
        await message.reply("Номер телефона получен", reply_markup=ReplyKeyboardRemove())
        phone = message.contact.phone_number
        if phone.startswith("+"):
            phone = phone
        else:
            phone = f"+{phone}"
        async with state.proxy() as data:
            data['phone'] = phone
        message_txt = f"Ваши данные:\n" \
                      f"ФИО: {data['names']}\n" \
                      f"Ваш email: {data['email']}\n" \
                      f"Ваш телефон: {data['phone']}\n" \
                      f"Желаемая база регистрации: {data['book_database']}"
        await bot.send_message(message.chat.id, message_txt, reply_markup=inline_keyboard_send_reg_data())
        await state.reset_state(with_data=False)
    else:
        logging.info(f"User({message.chat.id}) ввел не правильный номер")
        await message.answer("Вы отправили не свой номер", reply_markup=ReplyKeyboardRemove())
        await message.answer("Повторите отправку номера с помощью кнопки ниже",
                             reply_markup=keyboard_library_send_phone())


# Если пользователь нажал кнопку Отмена происходит отмена и возвращение в меню библиотеки
@dp.callback_query_handler(text='SendDataCancel', state=['*'])
async def send_license_db_reg_data_to_email_cancel(call: CallbackQuery, state: FSMContext):
    logging.info(f'User({call.message.chat.id}) отменил регистрацию в БД библиотеки - {call.data}')
    await bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id)  # Убирает инлайн клавиатуру
    # Добовляет alert вверху экрана
    await bot.answer_callback_query(callback_query_id=call.id, show_alert=False, text="Запрос на регистрацию отменен")
    await bot.send_message(chat_id=call.message.chat.id,
                           text='Регистрация Отменена\n'
                                'Возвращение в меню библиотеки', reply_markup=keyboard_library())
    await state.reset_state()


# Handler для кнопки возврат в ЭЛЕКТРОННЫЕ РЕСУРСЫ
@dp.callback_query_handler(text='back_to_library_el_res')
async def callback_el_res(call: CallbackQuery):
    await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                text='Электронные ресурсы\n',
                                reply_markup=inline_keyboard_library_el_res())


# Handler для кнопки возврат в 📕 Лицензионные Базы Данных
@dp.callback_query_handler(text='back_to_lic_db_reg', state=['*'])
async def callback_license_db_inline_menu(call: CallbackQuery, state: FSMContext):
    await state.reset_state()
    await callback_library_registration(call)


# Handler для остальных кнопок баз данных
@dp.callback_query_handler(text=['library_free_kaz', 'library_free_zarub', 'library_online_librares'])
async def callback_el_res_choice(call: CallbackQuery):
    # logging.info(f'call = {call.data}')
    if call.data == "library_free_kaz":
        text = "Базы данных свободного доступа(Казахстанские)"
        await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                    text=text,
                                    reply_markup=inline_keyboard_library_base_kaz())
    elif call.data == "library_free_zarub":
        text = "Базы данных свободного доступа(Зарубежные)"
        await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                    text=text,
                                    reply_markup=inline_keyboard_library_base_zarub())
    elif call.data == "library_online_librares":
        text = "Онлайн Библиотеки"
        await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                    text=text,
                                    reply_markup=inline_keyboard_library_online_bib())


@dp.callback_query_handler(text='SendEmailToLibrary')
async def send_email_to_library_and_notification(call: CallbackQuery, state: FSMContext):
    logging.info(f"User({call.message.chat.id}) отправил запрос на регистрацию")
    data = await state.get_data()
    await db.add_lib_reg_request_data(call.message.chat.id, data['names'], data['phone'], data['email'],
                                      data['book_database'])
    email_message = MIMEMultipart("alternative")
    email_message["From"] = "almaubot@gmail.com"
    email_message["To"] = "killka_m@mail.ru"
    # email_message["To"] = "lib@almau.edu.kz"
    email_message["Subject"] = "Регистрация на лицензионные базы с телеграм бота"
    sending_message = MIMEText(
        f"<html>"
        f"<body>"
        f"<h1>"
        f"Запрос на регистрацию на лицензионные базы <br/> <br/>"
        f"Регистрационные данные: <br/>"
        f"ФИО - {data['names']} <br/> "
        f"Email - {data['email']} <br/> "
        f"Телефон - {data['phone']}  <br/> "
        f"База Данных - {data['book_database']}"
        f"</h1>"
        f"</body>"
        f"</html>",
        "html", "utf-8"
    )

    email_message.attach(sending_message)
    await aiosmtplib.send(email_message,
                          hostname="smtp.gmail.com",
                          port=587,
                          start_tls=True,
                          # recipients=["killka_m@mail.ru"],
                          username="almaubot@gmail.com",
                          password="mjykwcchpvduwcjy")
    await bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id)  # Убирает инлайн клавиатуру
    await bot.answer_callback_query(callback_query_id=call.id, show_alert=False, text="Запрос успешно отправлен")
    await bot.send_message(chat_id=call.message.chat.id,
                           text='Запрос на регистрацию успешно отправлен, ожидайте ответа на указанную почту',
                           reply_markup=keyboard_library())
    # for admin in library_admins:
    #     try:
    #         await bot.send_message(admin, f"Пришла заявка на регистрацию:\n"
    #                                       f"ФИО - {data['names']}\n"
    #                                       f"Email - {data['email']}\n"
    #                                       f"Телефон - {data['phone']}\n"
    #                                       f"База Данных - {data['book_database']}")
    #     except Exception as err:
    #         logging.exception(err)
