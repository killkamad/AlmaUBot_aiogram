import logging

from aiogram import types
from aiogram.types import CallbackQuery

from loader import dp, bot
from keyboards.inline.menu_buttons import inline_keyboard_menu
from keyboards.default.menu_def_buttons import always_stay_keyboard
# Импортирование функций из БД контроллера
from utils import db_api as db


@dp.message_handler(commands=["start"])
async def bot_start(message: types.Message):
    check_id = await db.check_id(message.chat.id)
    if message.chat.id == check_id:
        logging.info('Уже есть в базе данных')
    else:
        await db.add_data(message.chat.username, message.chat.first_name, message.chat.last_name, message.chat.id)
        logging.info('Успешное добавление в базу данных')
    await bot.send_message(message.chat.id, f'Привет, {message.from_user.first_name} 😃',
                           reply_markup=always_stay_keyboard())
    await bot.send_message(message.chat.id, 'Главное меню:\n'
                                            '- Расписание - здесь можно посмотреть расписание\n'
                                            '- FAQ - часто задаваемые вопросы и ответы на них',
                           reply_markup=inline_keyboard_menu())
