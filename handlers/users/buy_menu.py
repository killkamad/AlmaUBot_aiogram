from loader import dp
from aiogram.types import Message, ContentType, ReplyKeyboardRemove
from keyboards.default import menu
from aiogram.dispatcher.filters import Command, Text


# @dp.message_handler(Command('menu'))
# async def show_menu(message: Message):
#     await message.answer('Выберите товар из меню ниже', reply_markup=menu)
#
#
# @dp.message_handler(Text(equals=['Пиво', 'Сиги', 'Хавчик']))
# async def menu_handler(message: Message):
#     text = message.text
#     await message.answer(f'Вы выбрали {text}. Спасибо', reply_markup=ReplyKeyboardRemove())
