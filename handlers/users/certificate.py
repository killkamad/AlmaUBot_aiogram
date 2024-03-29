import logging
import re
import aiosmtplib
import aiogram.utils.markdown as fmt
from aiogram import types
from aiogram.types import CallbackQuery, ContentType, ReplyKeyboardRemove, ChatActions
from aiogram.dispatcher import FSMContext

from data.config import email_certificate, email_bot, email_bot_password, hostname_bot, port_bot
from loader import dp, bot

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# Импорт клавиатур
from keyboards.inline import inline_keyboard_send_req_data, instruction_callback, \
    inline_keyboard_cancel_request, inline_keyboard_certificate_back
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


@dp.callback_query_handler(instruction_callback.filter())
async def callback_inline(call: CallbackQuery, callback_data: dict):
    logging.info(f'call = {call.data}')
    id = callback_data.get('id')
    button_content = await db.select_instruction(id)
    if button_content['button_file']:
        await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                    text=button_content['button_content'])
        await bot.send_document(call.message.chat.id, button_content['button_file'],
                                reply_markup=inline_keyboard_certificate_back())
    else:
        await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                    text=button_content['button_content'],
                                    reply_markup=inline_keyboard_certificate_back())
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
        await message.reply("Напишите комментарий к заявке (название военкомата, место требования и т.д.)", reply_markup=inline_keyboard_cancel_request())
        # await bot.send_message(message.chat.id, 'Напишите ваше ФИО:', reply_markup=inline_keyboard_cancel_request())
        await CertificateRequest.comment.set()


@dp.message_handler(content_types=ContentType.TEXT, state=CertificateRequest.comment)
async def process_name(message: types.Message, state: FSMContext):
    await delete_inline_buttons_in_dialogue(message)
    async with state.proxy() as data:
        data['comment'] = message.text
    await message.reply("Напишите ваше ФИО", reply_markup=inline_keyboard_cancel_request())
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
                      f"• <b>Вид справки:</b> {data['type']}\n" \
                      f"• <b>Комментарий:</b> {data['comment']}\n"
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
                                          data['type'], data['comment'])

    email_message = MIMEMultipart("alternative")
    email_message["From"] = email_bot
    email_message["To"] = email_certificate
    email_message["Subject"] = "Заявка на получение справки"
    sending_message = MIMEText(
        f"<html>"
        f"<body>"
        f"<h1>"
        f"Заявка на получение справки<br/> <br/>"
        f"Данные студента: <br/>"
        f"ФИО - {data['names']} <br/> "
        f"Email - {data['email']} <br/> "
        f"Телефон - {data['phone']}  <br/> "
        f"Вид справки - {data['type']} <br/> "
        f"Комментарий - {data['comment']}"
        f"</h1>"
        f"</body>"
        f"</html>",
        "html", "utf-8"
    )

    email_message.attach(sending_message)
    await bot.send_chat_action(call.message.chat.id, ChatActions.TYPING)
    await aiosmtplib.send(email_message,
                          hostname=hostname_bot,
                          port=port_bot,
                          start_tls=True,
                          username=email_bot,
                          password=email_bot_password)
    await bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id)
    await bot.answer_callback_query(callback_query_id=call.id, show_alert=False, text="Заявка успешно отправлена")
    await bot.send_message(chat_id=call.message.chat.id,
                           text='Заявка успешно отправлена',
                           reply_markup=always_stay_menu_keyboard())
    try:
        for admin in (await db.find_id_by_role('certificate_admin')):
            await bot.send_message(admin['idt'], f"Пришла заявка на получение справки:\n"
                                                 f"• ФИО - {data['names']}\n"
                                                 f"• Email - {data['email']}\n"
                                                 f"• Телефон - {data['phone']}\n"
                                                 f"• Вид справки - {data['type']}\n"
                                                 f"• Комментарий - {data['comment']}")
    except Exception as err:
        logging.exception(err)
