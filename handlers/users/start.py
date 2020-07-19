from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart
from loader import dp

# Импортирование функций из БД контроллера
from utils import db_api


@dp.message_handler(CommandStart())
async def bot_start(message: types.Message):
    if message.chat.id == 468899120:
        print('Уже есть в базе данных')
    await message.answer(f'Привет, {message.from_user.full_name}!')
    print(await db_api.select_data())
