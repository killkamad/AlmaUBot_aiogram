import ast
import logging

from aiogram.types import CallbackQuery, ContentType
from aiogram import types
from keyboards.default import always_stay_keyboard, keyboard_library
from loader import dp, bot
from keyboards.inline.menu_buttons import inline_keyboard_menu
from keyboards.inline.schedule_buttons import inline_keyboard_schedule
from keyboards.inline.faq_buttons import inline_keyboard_faq
from data.config import admins

# Импортирование функций из БД контроллера
from utils import db_api as db

from utils.misc import rate_limit
from utils.json_loader import json_data


# Настройка команд для бота
@dp.message_handler(commands="set_commands", state="*")
async def cmd_set_commands(message: types.Message):
    logging.info(f"User({message.chat.id}) использовал команду 'set_commands'")
    for admin in admins:
        try:
            if message.from_user.id == admin:
                commands = [types.BotCommand(command="/menu", description="главное меню"),
                            types.BotCommand(command="/admin", description="админ меню")]
                await bot.set_my_commands(commands)
                await message.answer("Команды настроены.")
        except Exception as err:
            logging.exception(err)


@rate_limit(5, 'menu')
@dp.message_handler(commands=['menu'])
async def menu_handler(message):
    logging.info(f"User({message.chat.id}) вошел в меню")
    await bot.send_message(message.chat.id, f'Вы находитесь в главном меню.',
                           reply_markup=always_stay_keyboard())
    await bot.send_message(message.chat.id, 'Главное меню:\n'
                                            '- Расписание - здесь можно посмотреть расписание\n'
                                            '- FAQ - часто задаваемые вопросы и ответы на них\n'
                                            '- Библиотека - поиск книг',
                           reply_markup=inline_keyboard_menu())


@dp.callback_query_handler(text='/schedule')
async def callback_inline_schedule(call: CallbackQuery):
    logging.info(f"User({call.message.chat.id}) вошел в Расписание")
    await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                text='Выберите ваш курс ↘', reply_markup=await inline_keyboard_schedule())


@dp.callback_query_handler(text='/faq')
async def callback_inline_schedule(call: CallbackQuery):
    logging.info(f"User({call.message.chat.id}) вошел в F.A.Q")
    await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                text='F.A.Q ↘', reply_markup=inline_keyboard_faq())


@dp.callback_query_handler(text='/library')
async def callback_inline_schedule(call: CallbackQuery):
    logging.info(f"User({call.message.chat.id}) вошел в Библиотеку")
    await bot.send_message(chat_id=call.message.chat.id,
                           text='Библиотека ↘', reply_markup=keyboard_library())


#  Получение айди расписания из бд и отправка пользователю
@dp.callback_query_handler(text_contains="['schedule_call'")
async def callback_inline(call: CallbackQuery):
    logging.info(f'call = {call.data}')
    valueFromCallBack = ast.literal_eval(call.data)[1]
    file_id = await db.find_schedule_id(valueFromCallBack)
    await bot.send_document(call.message.chat.id, file_id)


@dp.callback_query_handler(text='go_back')
async def callback_inline(call: CallbackQuery):
    logging.info(f"User({call.message.chat.id}) нажал кнопку Назад и вернулся в Главное меню")
    await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                text='Главное меню:\n'
                                     '- Расписание - здесь можно посмотреть расписание\n'
                                     '- FAQ - часто задаваемые вопросы и ответы на них',
                                reply_markup=inline_keyboard_menu())


# Меню F.A.Q
@dp.callback_query_handler(text=['moodle', 'retake', 'reactor_info', 'atestat', 'u_wifi'])
async def callback_inline_faq(call: CallbackQuery):
    logging.info(f"User({call.message.chat.id}) нажал на кнопку {call.data}")
    if call.data == "moodle":
        text = (await json_data())['faq_answers']['moodle']
        await bot.send_message(call.message.chat.id, text=text)
    elif call.data == "retake":
        text = (await json_data())['faq_answers']['retake']
        await bot.send_message(call.message.chat.id, text=text)
    elif call.data == "reactor_info":
        text = (await json_data())['faq_answers']['rektor']
        await bot.send_message(call.message.chat.id, text=text)
    elif call.data == "atestat":
        text = (await json_data())['faq_answers']['examination']
        await bot.send_message(call.message.chat.id, text=text)
    elif call.data == "u_wifi":
        text = (await json_data())['faq_answers']['wifi1']
        await bot.send_message(call.message.chat.id, text=text)
