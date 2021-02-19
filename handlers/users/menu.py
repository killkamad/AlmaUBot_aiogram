import ast
import logging
from loader import dp, bot

from aiogram.types import CallbackQuery, ContentType, ReplyKeyboardRemove, Message
from aiogram import types
from keyboards.default import always_stay_keyboard, keyboard_library, keyboard_almaushop, keyboard_feedback, \
    keyboard_send_phone_to_register_in_db, always_stay_menu_keyboard
from keyboards.inline import main_faq_callback, inline_keyboard_menu, inline_keyboard_schedule, \
    inline_keyboard_main_faq, inline_keyboard_main_faq_back, inline_keyboard_certificate, schedule_callback, \
    inline_keyboard_nav_unifi

from data.config import admins
# Импортирование функций из БД контроллера
from utils import db_api as db

from utils.misc import rate_limit
from states.register_user_phone import RegisterUserPhone

from aiogram.dispatcher import FSMContext
from states.feedback_state import FeedbackMessage

_main_menu_text = 'Главное меню:\n' \
                  '- Расписание - просмотр актуального расписания\n' \
                  '- FAQ - часто задаваемые вопросы студентов и ответы на них\n' \
                  '- Библиотека - поиск книг\n' \
                  '- AlmaU Shop - просмотр мерча AlmaU и книг\n' \
                  '- Академический календарь - получение календаря на учебный год\n' \
                  '- Обратная связь с ректором - возможность написать свою жалобу или пожелания ректору\n'


# Настройка команд для бота
@dp.message_handler(commands="set_commands", state="*")
async def cmd_set_commands(message: types.Message):
    logging.info(f"User({message.chat.id}) использовал команду 'set_commands'")
    for admin in admins:
        try:
            if message.from_user.id == admin:
                commands = [types.BotCommand(command="/menu", description="главное меню"),
                            types.BotCommand(command="/help", description="помощь"),
                            types.BotCommand(command="/admin", description="админ меню"),
                            types.BotCommand(command="/set_commands", description="установка команд бота")
                            ]
                await bot.set_my_commands(commands)
                await message.answer("Команды настроены.")
        except Exception as err:
            logging.exception(err)


@rate_limit(6, 'menu_old')
@dp.message_handler(commands=['menu_old'])
async def menu_handler(message):
    logging.info(f"User({message.chat.id}) вошел в меню")
    await bot.send_message(message.chat.id, _main_menu_text,
                           reply_markup=inline_keyboard_menu())


@rate_limit(5, 'menu')
@dp.message_handler(commands=['menu'])
async def menu_handler(message):
    logging.info(f"User({message.chat.id}) вошел в меню")
    await bot.send_message(message.chat.id, 'Главное меню ↘',
                           reply_markup=always_stay_menu_keyboard())


################# Регистрация номера в таблицу Users ###########################
@rate_limit(6, 'phone_reg')
@dp.message_handler(commands=['phone_reg'])
async def register_user_phone(message):
    logging.info(f"User({message.chat.id}) начал регистрацию номера телефона")
    await message.answer("Отправьте свой номер телефона", reply_markup=keyboard_send_phone_to_register_in_db())
    await RegisterUserPhone.phone.set()


@dp.message_handler(content_types=ContentType.CONTACT, state=RegisterUserPhone.phone)
async def register_user_phone_next(message: types.Message, state: FSMContext):
    if message.chat.id == message.contact.user_id:
        logging.info(f"User({message.chat.id}) ввел правильный номер {message.contact.phone_number}")
        await message.reply("✅ Номер телефона получен, и успешно зарегистрирован",
                            reply_markup=always_stay_menu_keyboard())
        phone = message.contact.phone_number
        if phone.startswith("+"):
            phone = phone
        else:
            phone = f"+{phone}"
        await db.register_user_phone(message.chat.id, phone)
        await state.reset_state()
    else:
        logging.info(f"User({message.chat.id}) ввел не правильный номер")
        await message.answer("Вы отправили не свой номер", reply_markup=ReplyKeyboardRemove())
        await message.answer("Повторите отправку номера с помощью кнопки ниже",
                             reply_markup=keyboard_send_phone_to_register_in_db())


################# КОНЕЦ Регистрация номера в таблицу Users КОНЕЦ ###########################


@rate_limit(1, 'Меню')
@dp.message_handler(lambda message: message.text in ["📅 Расписание", "⁉ FAQ", "📚 Библиотека", "🌀 AlmaU Shop",
                                                     "🗒 Академический календарь", "🏢 Получить справку",
                                                     "📝 Связь с ректором", "🗺️ Навигация по университету"])
async def main_menu_handler(message: Message):
    logging.info(f"User({message.chat.id}) enter {message.text}")
    if message.text == "📅 Расписание":
        await message.answer(text='Выберите ваш курс ↘', reply_markup=await inline_keyboard_schedule())
    elif message.text == "⁉ FAQ":
        await message.answer(text='F.A.Q ↘', reply_markup=await inline_keyboard_main_faq())
    elif message.text == "📚 Библиотека":
        await message.answer(text='Библиотека ↘', reply_markup=keyboard_library())
    elif message.text == "🌀 AlmaU Shop":
        await message.answer(text='AlmaU Shop ↘', reply_markup=keyboard_almaushop())
    elif message.text == "🗒 Академический календарь":
        file_id = await db.find_id_academic_calendar()
        await bot.send_document(message.chat.id, file_id)
    elif message.text == "🏢 Получить справку":
        await message.answer(text='Получение справки с места учебы\n' \
                                  'Вы можете получить справку или оставить заявку на получение справки с места учебы по месту требования (военкомат и тд.) ↘',
                             reply_markup=await inline_keyboard_certificate())
    elif message.text == "📝 Связь с ректором":
        await message.answer(
            text='Вы можете написать письмо с жалобами и предложениями адресованное ректору нашего университета. \n'
                 'Для этого вам нужно указать свои контактные данные и непосредственно текст самого письма.',
            reply_markup=keyboard_feedback())
    elif message.text == "🗺️ Навигация по университету":
        await message.answer(text='Навигация по университету', reply_markup=inline_keyboard_nav_unifi())


@dp.message_handler(lambda message: message.text in ["⬅ В главное меню"])
async def main_menu_handler(message: Message):
    logging.info(f"User({message.chat.id}) enter {message.text}")
    if message.text == "⬅ В главное меню":
        await message.answer('Возвращение в главное меню', reply_markup=always_stay_menu_keyboard())


@dp.callback_query_handler(text='/schedule')
async def callback_inline_schedule(call: CallbackQuery):
    logging.info(f"User({call.message.chat.id}) вошел в Расписание")
    await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                text='Выберите ваш курс ↘', reply_markup=await inline_keyboard_schedule())


@dp.callback_query_handler(text='/faq')
async def callback_inline_faq(call: CallbackQuery):
    logging.info(f"User({call.message.chat.id}) вошел в F.A.Q")
    await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                text='F.A.Q ↘', reply_markup=await inline_keyboard_main_faq())


@dp.callback_query_handler(text='/library')
async def callback_inline_library(call: CallbackQuery):
    logging.info(f"User({call.message.chat.id}) вошел в Библиотеку")
    await bot.send_message(chat_id=call.message.chat.id,
                           text='Библиотека ↘', reply_markup=keyboard_library())


@dp.callback_query_handler(text='/feedback')
async def callback_inline_feedback(call: CallbackQuery):
    logging.info(f"User({call.message.chat.id}) вошел в Обратную связь с ректором")
    await bot.send_message(chat_id=call.message.chat.id,
                           text='Обратная связь с ректором ↘')
    await bot.send_message(chat_id=call.message.chat.id,
                           text='Вы можете написать письмо с жалобами и предложениями адресованное ректору нашего университета. \n'
                                'Для этого вам нужно указать свои контактные данные и непосредственно текст самого письма.',
                           reply_markup=keyboard_feedback())


@dp.callback_query_handler(text='/almaushop')
async def callback_inline_almaushop(call: CallbackQuery):
    logging.info(f"User({call.message.chat.id}) вошел в AlmaU Shop")
    await bot.send_message(chat_id=call.message.chat.id,
                           text='AlmaU Shop ↘', reply_markup=keyboard_almaushop())


@dp.callback_query_handler(text='/certificate')
async def callback_inline_certificate(call: CallbackQuery):
    logging.info(f"User({call.message.chat.id}) вошел в Получение справки")
    await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                text='Получение справки с места учебы ↘ \n' \
                                     'Вы можете получить справку или оставить заявку на получение справки с места учебы по месту требования (военкомат и тд.)',
                                reply_markup=await inline_keyboard_certificate())


@dp.callback_query_handler(text='/academ_calendar')
async def callback_academ_calendar(call: CallbackQuery):
    file_id = await db.find_id_academic_calendar()
    await bot.send_document(call.message.chat.id, file_id)


@dp.callback_query_handler(text='go_back')
async def callback_inline(call: CallbackQuery):
    logging.info(f"User({call.message.chat.id}) нажал кнопку Назад и вернулся в Главное меню")
    await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                text=_main_menu_text,
                                reply_markup=inline_keyboard_menu())


######################  Динамические кнопки Расписания ##################################################


@dp.callback_query_handler(schedule_callback.filter())
async def callback_inline(call: CallbackQuery, callback_data: dict):
    logging.info(f'call = {call.data}')
    schedule_name = callback_data.get('schedule_name')  # Получение названия кнопки из callback_data
    file_id = await db.find_schedule_id(schedule_name)  # Получение file_id кнопки из БД
    await bot.send_document(call.message.chat.id, file_id)  # Отправка расписания пользователю


###################### КОНЕЦ Динамические кнопки Расписания КОНЕЦ #################################################
############################ Меню F.A.Q #########################################################
@dp.callback_query_handler(main_faq_callback.filter())
async def callback_inline_faq_menu(call: CallbackQuery, callback_data: dict):
    id = callback_data.get('callback_id')
    answer = (await db.main_faq_select_question_and_answer(id))['answer']
    await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                text=answer, reply_markup=inline_keyboard_main_faq_back())


@dp.callback_query_handler(text='back_to_main_faq')
async def callback_inline_faq_menu_back(call: CallbackQuery):
    logging.info(f'User({call.message.chat.id}) вернулся в админ меню')
    await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                text="F.A.Q ↘",
                                reply_markup=await inline_keyboard_main_faq())

############################ КОНЕЦ Меню F.A.Q КОНЕЦ #########################################################
