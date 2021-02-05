from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandHelp
from keyboards.inline.menu_buttons import inline_keyboard_menu
from loader import dp
from utils.misc import rate_limit


# @rate_limit(5, 'help')
# @dp.message_handler(CommandHelp())
# async def bot_help(message: types.Message):
#     text = [
#         'Возможности бота:\n'
#         '- Расписание - здесь можно посмотреть расписание\n'
#         '- FAQ - часто задаваемые вопросы и ответы на них'
#     ]
#     await message.answer('\n'.join(text), reply_markup=inline_keyboard_menu())
