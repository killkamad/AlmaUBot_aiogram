import ast
import logging
import re
import aiogram.utils.markdown as fmt
from aiogram import types
from aiogram.types import CallbackQuery, ContentType, ReplyKeyboardRemove
from aiogram.dispatcher import FSMContext

from loader import dp, bot

# Импорт клавиатур
from keyboards.inline import inline_keyboard_get_certificate, inline_keyboard_send_req_data, certificate_callback, \
    inline_keyboard_cancel_request
from keyboards.default import always_stay_keyboard, keyboard_request_send_phone, keyboard_certificate_type, \
    keyboard_feedback_send_phone, always_stay_menu_keyboard
from utils import db_api as db

# Импорт стейтов
from states.request_state import CertificateRequest

# Патерн регулярного выражения для проверки почты
valid_email_pattern = re.compile('(^|\s)[-a-z0-9_.]+@([-a-z0-9]+\.)+[a-z]{2,6}(\s|$)')


# Создается функция для проверки валидности почты
def is_valid_email(s):
    return valid_email_pattern.match(s) is not None


# Список залитых индивидуальных справок студента
@dp.callback_query_handler(text='complete_certificates')
async def callback_inline_completes(call: CallbackQuery):
    logging.info(f"User({call.message.chat.id}) вошел в Готовые справки")
    await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                text='Готовые справки:',
                                reply_markup=await inline_keyboard_get_certificate(call.message.chat.id))
    await call.answer()


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
    try:
        await bot.edit_message_reply_markup(message.chat.id, message.message_id - 1)
    except:
        pass
    async with state.proxy() as data:
        data['names'] = message.text
    await message.reply("Напишите ваш Email", reply_markup=inline_keyboard_cancel_request())
    await CertificateRequest.email.set()


@dp.message_handler(content_types=ContentType.TEXT, state=CertificateRequest.email)
async def process_name(message: types.Message, state: FSMContext):
    try:
        await bot.edit_message_reply_markup(message.chat.id, message.message_id - 1)
    except:
        pass
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
        message_txt = f"Ваши данные:\n" \
                      f"ФИО: {data['names']}\n" \
                      f"Ваш email: {data['email']}\n" \
                      f"Ваш телефон: {data['phone']}\n" \
                      f"Вид справки: {data['type']}"
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
    await bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id)
    await bot.answer_callback_query(callback_query_id=call.id, show_alert=False, text="Заявка успешно отправлена")
    await bot.send_message(chat_id=call.message.chat.id,
                           text='Заявка успешно отправлена',
                           reply_markup=always_stay_menu_keyboard())
