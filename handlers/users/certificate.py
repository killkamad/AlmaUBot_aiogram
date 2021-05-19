import logging
import re
import aiosmtplib
import aiogram.utils.markdown as fmt
from aiogram import types
from aiogram.types import CallbackQuery, ContentType, ReplyKeyboardRemove, ChatActions
from aiogram.dispatcher import FSMContext

from loader import dp, bot

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# Импорт клавиатур
from keyboards.inline import inline_keyboard_get_certificate, inline_keyboard_send_req_data, certificate_callback, \
    inline_keyboard_cancel_request
from keyboards.default import keyboard_request_send_phone, keyboard_certificate_type, \
    keyboard_feedback_send_phone, always_stay_menu_keyboard
from utils import db_api as db
from utils.delete_inline_buttons import delete_inline_buttons_in_dialogue
# Импорт стейтов
from states.request_state import CertificateRequest


# Патерн регулярного выражения для проверки почты
valid_email_pattern = re.compile('(^|\s)[-a-z0-9_.]+@([-a-z0-9]+\.)+[a-z]{2,6}(\s|$)')


# Создается функция для проверки валидности почты
def is_valid_email(s):
    return valid_email_pattern.match(s) is not None


# # Список залитых индивидуальных справок студента
# @dp.callback_query_handler(text='complete_certificates')
# async def callback_inline_completes(call: CallbackQuery):
#     logging.info(f"User({call.message.chat.id}) вошел в Готовые справки")
#     await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
#                                 text='Готовые справки:',
#                                 reply_markup=await inline_keyboard_get_certificate(call.message.chat.id))
#     await call.answer()


@dp.callback_query_handler(text='certificate_inst')
async def callback_inline_certificate_instructions(call: CallbackQuery):
    logging.info(f"User({call.message.chat.id}) вошел в Готовые справки")
    await bot.send_message(chat_id=call.message.chat.id,
                                text=f'Инструкция по заполнению заявок на справку ГЦВП (пособие), вонкомат (по призыву) и по месту требования.\n\n' \
                                    f'Для прохождения данной процедуры вам необходимо:\n' \
                                    f'1) Войти в портал AlmaUnion https://almaunion.almau.edu.kz/login и авторизоваться (ввести свои логин и пароль*)\n' \
                                    f'2) В меню слева выбрать модуль «Обращения»\n\n' \
                                    f'<b>Примечания*</b> Если у вас нет/вы его забыли/потеряли/вообще не было <b>логина и пароля</b>, то вы можете обратиться в Офис регистратора и получить их в индивидуальном порядке.\n\n' \
                                    f'3) Для создания нового обращения нажимаете «OK, я прошел анкетирование»\n' \
                                    f'4) Нажимаете на кнопку «Создать обращение»\n' \
                                    f'5) Выбираете категорию «Заявка на справку»\n' \
                                    f'6) Вид справки «ГЦВП», «Справка для военкомата», «По месту требования»\n' \
                                    f'7) Вводите номер сотового телефона\n' \
                                    f'8) В комментариях заполняете номер справки/место призыва\n' \
                                    f'9) Нажимаете на кнопку «Отправить»\n\n' \
                                    f'<b>В личном кабинете студент так же может получить справку по месту требования с подтверждающим QR кодом в формате PDF.</b>\n' \
                                    f'<b>Такая справка действительна в течении 10 рабочих дней.</b>\n\n' \
                                    f'Студент должен зайти в свой личный кабинет almaunion.almau.edu.kz:\n' \
                                    f'1) В меню слева выбрать модуль «Справка»\n' \
                                    f'2) В появившемся окне «Справка» нажимаете на кнопку «Скачать»\n\n' \
                                    f'Данную справку  можно скачать только при наличии на смартфоне шрифта «Times New Roman», если вы заходите со смартфона. Если данного шрифта нет в телефоне, она выйдет с ошибкой.\n',
                                parse_mode='HTML')


@dp.callback_query_handler(text='application_inst')
async def callback_inline_application_instructions(call: CallbackQuery):
    logging.info(f"User({call.message.chat.id}) вошел в Готовые справки")
    await bot.send_message(chat_id=call.message.chat.id,
                                text=f'Инструкция по заполнению заявлений.\n\n'
                                    f'Для прохождения данной процедуры вам необходимо:\n'
                                    f'1) Войти в портал AlmaUnion https://almaunion.almau.edu.kz/login и авторизоваться (ввести свои логин и пароль*)\n'
                                    f'2) В меню слева выбрать модуль «Обращения»\n\n'
                                    f'<b>Примечания*</b> Если у вас нет/ вы его забыли/ потеряли/ вообще не было <b>Логина и пароля</b>, то вы можете обратиться в Офис регистратора и получить их в индивидуальном порядке.\n\n'
                                    f'3) Для создания нового обращения нажимаете «OK, я прошел анкетирование»\n'
                                    f'4) Нажимаете на кнопку «Создать обращение»\n'
                                    f'5) Выбираете категорию «Заявка на заявление»\n'
                                    f'6) Выбираете вид заявки, т.е. какое заявление вам надо заполнить\n'
                                    f'7) С левой стороны будет прикреплен образец, как заполнить заявление\n'
                                    f'8) В инструкции, как заполнять заявление, вы можете скачать бланк для заполнения заявления\n'
                                    f'9) Вводите номер сотового телефона\n'
                                    f'10) В комментариях заполняете или уточняете интересующие вас вопросы\n'
                                    f'11) Прикрепляете заявление\n'
                                    f'12) Нажимаете на кнопку «Отправить»\n',
                                parse_mode='HTML')


@dp.callback_query_handler(certificate_callback.filter())
async def callback_inline(call: CallbackQuery, callback_data: dict):
    logging.info(f'call = {call.data}')
    certificate_id = callback_data.get('id')
    file_id = await db.find_certificate_id(certificate_id)
    await bot.send_document(call.message.chat.id, file_id)
    await call.answer()


# Запрос на получение справки
@dp.callback_query_handler(text='request_certificate')
async def callback_inline_request(call: CallbackQuery):
    logging.info(f"User({call.message.chat.id}) вошел в Запрос справки")
    await bot.send_message(chat_id=call.message.chat.id,
                           text='Укажите вид справки',
                           reply_markup=keyboard_certificate_type())
    await CertificateRequest.type.set()
    await call.answer()


@dp.message_handler(state=CertificateRequest.type)
async def process_name(message: types.Message, state: FSMContext):
    if message.text == "⬅ В главное меню":
        await message.answer('Возвращение в главное меню', reply_markup=always_stay_menu_keyboard())
        await state.reset_state()
    else:
        async with state.proxy() as data:
            data['type'] = fmt.quote_html(message.text)
        await message.reply("Напишите ваше ФИО", reply_markup=inline_keyboard_cancel_request())
        # await bot.send_message(message.chat.id, 'Напишите ваше ФИО:', reply_markup=inline_keyboard_cancel_request())
        await CertificateRequest.names.set()


@dp.message_handler(content_types=ContentType.TEXT, state=CertificateRequest.names)
async def process_name(message: types.Message, state: FSMContext):
    await delete_inline_buttons_in_dialogue(message)
    async with state.proxy() as data:
        data['names'] = message.text
    await message.reply("Напишите ваш Email", reply_markup=inline_keyboard_cancel_request())
    await CertificateRequest.email.set()


@dp.message_handler(content_types=ContentType.TEXT, state=CertificateRequest.email)
async def process_name(message: types.Message, state: FSMContext):
    await delete_inline_buttons_in_dialogue(message)
    if "@" in message.text:
        email = message.text.strip()
        if is_valid_email(email):
            async with state.proxy() as data:
                data['email'] = fmt.quote_html(message.text)
            await message.reply("Отправьте свой номер телефона", reply_markup=keyboard_request_send_phone())
            await CertificateRequest.phone.set()
        else:
            await message.reply("Неверный формат электронной почты, напишите правильно почту!",
                                reply_markup=inline_keyboard_cancel_request())
    else:
        await message.reply("Неверный формат электронной почты, напишите правильно почту!",
                            reply_markup=inline_keyboard_cancel_request())


@dp.message_handler(content_types=ContentType.CONTACT, state=CertificateRequest.phone)
async def SendRequest(message: types.Message, state: FSMContext):
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
        message_txt = f"<b>Ваши данные:</b>\n" \
                      f"• <b>ФИО:</b> {data['names']}\n" \
                      f"• <b>Ваш email:</b> {data['email']}\n" \
                      f"• <b>Ваш телефон:</b> {data['phone']}\n" \
                      f"• <b>Вид справки:</b> {data['type']}"
        await bot.send_message(message.chat.id, message_txt, reply_markup=inline_keyboard_send_req_data())
        await state.reset_state(with_data=False)
    else:
        logging.info(f"User({message.chat.id}) ввел не правильный номер")
        await message.answer("Вы отправили не свой номер", reply_markup=ReplyKeyboardRemove())
        await message.answer("Повторите отправку номера с помощью кнопки ниже",
                             reply_markup=keyboard_feedback_send_phone())


@dp.callback_query_handler(text='send_req_cancel', state=['*'])
async def callback_inline_request_cancel(call: CallbackQuery, state: FSMContext):
    logging.info(f'User({call.message.chat.id}) отменил заявку - {call.data}')
    await state.reset_state()
    await bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id)
    await bot.answer_callback_query(callback_query_id=call.id, show_alert=False, text="Заявка отменена")
    await bot.send_message(chat_id=call.message.chat.id,
                           text='Отправка отменена\n'
                                'Возвращение в главное меню', reply_markup=always_stay_menu_keyboard())


# Успешное отправление запроса для справки
@dp.callback_query_handler(text='send_req_certificate')
async def callback_inline_send_request(call: CallbackQuery, state: FSMContext):
    logging.info(f"User({call.message.chat.id}) отправил заявку")
    data = await state.get_data()
    await db.add_certificate_request_data(call.message.chat.id, data['names'], data['phone'], data['email'],
                                          data['type'])

    email_message = MIMEMultipart("alternative")
    email_message["From"] = "almaubot@gmail.com"
    email_message["To"] = "killka_m@mail.ru"
    email_message["Subject"] = "Заявка на получение справки с места учебы"
    sending_message = MIMEText(
        f"<html>"
        f"<body>"
        f"<h1>"
        f"Заявка на получение справки с места учебы <br/> <br/>"
        f"Данные студента: <br/>"
        f"ФИО - {data['names']} <br/> "
        f"Email - {data['email']} <br/> "
        f"Телефон - {data['phone']}  <br/> "
        f"Вид справки - {data['type']}"
        f"</h1>"
        f"</body>"
        f"</html>",
        "html", "utf-8"
    )

    email_message.attach(sending_message)
    await bot.send_chat_action(call.message.chat.id, ChatActions.TYPING)
    await aiosmtplib.send(email_message,
                          hostname="smtp.gmail.com",
                          port=587,
                          start_tls=True,
                          # recipients=["killka_m@mail.ru"],
                          username="almaubot@gmail.com",
                          password="mjykwcchpvduwcjy")
    await bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id)
    await bot.answer_callback_query(callback_query_id=call.id, show_alert=False, text="Заявка успешно отправлена")
    await bot.send_message(chat_id=call.message.chat.id,
                           text='Заявка успешно отправлена',
                           reply_markup=always_stay_menu_keyboard())
