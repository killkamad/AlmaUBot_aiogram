import logging
import aiogram.utils.markdown as fmt
from data.config import admins
from aiogram.types import CallbackQuery, ContentType, ChatActions
from aiogram import types

from keyboards.default import keyboard_feedback_send_phone, always_stay_menu_keyboard
from keyboards.inline import inline_keyboard_send_msg_data, \
    inline_keyboard_cancel_msg_send
from states.feedback_state import FeedbackMessage
from loader import dp, bot

from data.button_names.feedback_buttons import feedback_advisor_button
# Импортирование функций из БД контроллера
from utils import db_api as db
from utils.get_linenumber import get_linenumber
from utils.misc import rate_limit
from aiogram.types import ReplyKeyboardRemove

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import aiosmtplib
from utils.delete_inline_buttons import delete_inline_buttons_in_dialogue
from aiogram.dispatcher import FSMContext
# Библиотека регулярных выражений
import re

# Патерн регулярного выражения для проверки почты
valid_email_pattern = re.compile('(^|\s)[-a-z0-9_.]+@([-a-z0-9]+\.)+[a-z]{2,6}(\s|$)')


# Создается функция для проверки валидности почты
def is_valid_email(s):
    return valid_email_pattern.match(s) is not None


@rate_limit(1)
@dp.message_handler(text=[feedback_advisor_button], state=None)
async def feedback_text_buttons_handler(message: types.Message, state: FSMContext):
    await db.add_bot_log(message.chat.id, message.text, f"{__name__}.py [LINE:{get_linenumber()}]")
    logging.info(f"User({message.chat.id}) нажал на {message.text}")
    if message.text == feedback_advisor_button:
        # await message.answer('...', reply_markup=ReplyKeyboardRemove())
        await message.reply("Что вы хотели бы написать?", reply_markup=inline_keyboard_cancel_msg_send())
        await FeedbackMessage.content.set()


@dp.message_handler(state=FeedbackMessage.content)
async def process_name(message: types.Message, state: FSMContext):
    await delete_inline_buttons_in_dialogue(message)
    async with state.proxy() as data:
        data['content'] = fmt.quote_html(message.text)
    await message.reply("Напишите ваше ФИО", reply_markup=inline_keyboard_cancel_msg_send())
    await FeedbackMessage.names.set()


@dp.message_handler(state=FeedbackMessage.names)
async def process_name(message: types.Message, state: FSMContext):
    await delete_inline_buttons_in_dialogue(message)
    async with state.proxy() as data:
        data['names'] = fmt.quote_html(message.text)
    await message.reply("Напишите ваш Email", reply_markup=inline_keyboard_cancel_msg_send())
    await FeedbackMessage.email.set()


@dp.message_handler(content_types=ContentType.TEXT, state=FeedbackMessage.email)
async def process_name(message: types.Message, state: FSMContext):
    await delete_inline_buttons_in_dialogue(message)
    if "@" in message.text:
        email = message.text.strip()
        if is_valid_email(email):
            async with state.proxy() as data:
                data['email'] = fmt.quote_html(message.text)

            await message.reply("Отправьте свой номер телефона", reply_markup=keyboard_feedback_send_phone())
            await FeedbackMessage.phone.set()
        else:
            await message.reply("Неверный формат электронной почты, напишите правильно почту!",
                                reply_markup=inline_keyboard_cancel_msg_send())
    else:
        await message.reply("Неверный формат электронной почты, напишите правильно почту!",
                            reply_markup=inline_keyboard_cancel_msg_send())


@dp.message_handler(content_types=ContentType.CONTACT, state=FeedbackMessage.phone)
async def SendToEmail(message: types.Message, state: FSMContext):
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
                      f"• <b>Содержание письма:</b> {data['content']}"
        await bot.send_message(message.chat.id, message_txt, reply_markup=inline_keyboard_send_msg_data(),
                               parse_mode='HTML')
        await state.reset_state(with_data=False)
    else:
        logging.info(f"User({message.chat.id}) ввел не правильный номер")
        await message.answer("Вы отправили не свой номер", reply_markup=ReplyKeyboardRemove())
        await message.answer("Повторите отправку номера с помощью кнопки ниже",
                             reply_markup=keyboard_feedback_send_phone())


@dp.callback_query_handler(text='SendMsgCancel', state=['*'])
async def callback_inline_SendDataCancel(call: CallbackQuery, state: FSMContext):
    logging.info(f'User({call.message.chat.id}) отменил отправку письма - {call.data}')
    await bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id)  # Убирает инлайн клавиатуру
    # Добовляет alert вверху экрана
    await bot.answer_callback_query(callback_query_id=call.id, show_alert=False, text="Отправка письма отменена")
    await bot.send_message(chat_id=call.message.chat.id,
                           text='Отправка отменена\n'
                                'Возвращение в главное меню', reply_markup=always_stay_menu_keyboard())
    await state.reset_state()


@dp.callback_query_handler(text='SendMsgToRector')
async def callback_inline_SendMsgToRector(call: CallbackQuery, state: FSMContext):
    logging.info(f"User({call.message.chat.id}) отправил письмо")
    data = await state.get_data()
    await db.add_feedback_msg_data(call.message.chat.id, data['names'], data['phone'], data['email'],
                                   data['content'])
    email_message = MIMEMultipart("alternative")
    email_message["From"] = "almaubot@gmail.com"
    email_message["To"] = "killka_m@mail.ru"
    # email_message["To"] = "ketchupass10@gmail.com"
    email_message["Subject"] = "Письмо эдвайзеру от студента"

    sending_message = MIMEText(
        f"<html>"
        f"<body>"
        f"<h1>"
        f"Письмо от {data['names']}"
        f"</h1>"
        f"<h2>"
        f"Email: {data['email']} <br/> "
        f"Телефон: {data['phone']}  <br/> "
        f"</h2>"
        f"<h2>"
        f"Содержание письма: <br/>"
        f"</h2>"
        f"<p>"
        f"{data['content']}"
        f"</p>"
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
                          username="almaubot@gmail.com",
                          password="mjykwcchpvduwcjy")
    await bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id)
    await bot.answer_callback_query(callback_query_id=call.id, show_alert=False, text="Письмо успешно отправлено")
    await bot.send_message(chat_id=call.message.chat.id,
                           text='Письмо успешно отправлено',
                           reply_markup=always_stay_menu_keyboard())

    try:
        for admin in (await db.find_id_by_role('advisor_admin')):
            await bot.send_message(admin['idt'], f"<b>Вам пришло письмо от студента:</b>\n"
                                          f"• <b>ФИО</b> - {data['names']}\n"
                                          f"• <b>Email</b> - {data['email']}\n"
                                          f"• <b>Телефон</b> - {data['phone']}\n"
                                          f"• <b>Содержание письма:</b>\n"
                                          f"{data['content']}")
    except Exception as err:
        logging.exception(err)
