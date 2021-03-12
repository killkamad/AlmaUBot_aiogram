import logging

from aiogram import types
from aiogram.types import CallbackQuery

from loader import dp, bot
from keyboards.default import always_stay_menu_keyboard
# Импортирование функций из БД контроллера
from utils import db_api as db


@dp.message_handler(commands=["start"])
async def bot_start(message: types.Message):
    check_id = await db.check_id(message.chat.id)
    if message.chat.id == check_id:
        logging.info(f'Данный пользователь ({message.chat.id}) уже находится в базе данных')
    else:
        await db.add_data(message.chat.username, message.chat.first_name, message.chat.last_name, message.chat.id)
    if message.from_user.first_name:
        await bot.send_message(message.chat.id, f'Привет, {message.from_user.first_name} 😃',
                               reply_markup=always_stay_menu_keyboard())
    elif message.from_user.last_name:
        await bot.send_message(message.chat.id, f'Привет, {message.from_user.last_name} 😃',
                               reply_markup=always_stay_menu_keyboard())
    elif message.from_user.username:
        await bot.send_message(message.chat.id, f'Привет, {message.from_user.username} 😃',
                               reply_markup=always_stay_menu_keyboard())
    # await bot.send_message(message.chat.id, _main_menu_text, reply_markup=inline_keyboard_menu())
