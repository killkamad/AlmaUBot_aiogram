from aiogram import types
from aiogram.types import ContentType

from keyboards.default import always_stay_keyboard
from keyboards.inline.library_buttons import inline_keyboard_library_el_res
from keyboards.inline.menu_buttons import inline_keyboard_menu
from loader import dp, bot
import logging

from utils.json_loader import json_data
from utils.misc import rate_limit


@rate_limit(1)
@dp.message_handler(lambda message: message.text in ['🏠 Меню', '❓ Помощь', '💻 О боте', '⬅ В главное меню'])
async def bot_echo(message: types.Message):
    logging.info(f'User({message.chat.id}) нажал на кнопку {message.text}')
    # Кнопки главного меню
    if message.text == '🏠 Меню':
        await message.answer('Главное меню:\n'
                             '- Расписание - здесь можно посмотреть расписание\n'
                             '- FAQ - часто задаваемые вопросы и ответы на них\n'
                             '- Библиотека - поиск книг',
                             reply_markup=inline_keyboard_menu())
    elif message.text == '❓ Помощь':
        await message.answer('Главное меню:\n'
                             '- Расписание - здесь можно посмотреть расписание\n'
                             '- FAQ - часто задаваемые вопросы и ответы на них',
                             reply_markup=inline_keyboard_menu())
    elif message.text == '💻 О боте':
        await message.answer('<b>О боте:</b>\n\n'
                             '- Для загрузки расписания, войти в меню админа - /admin '
                             'и нажать на кнопку <b>"📤 Загрузить расписание"</b>.\n\n'
                             '- Для создания массовой рассылки, войти в меню админа - /admin '
                             'и нажать на кнопку <b>"📣 Рассылка"</b>, сообщение может содержать максимум'
                             ' 1000 символов, к сообщению можно прикрепить фото или файл.\n\n'
                             '- Для получучения файла с расписанием, в главном меню нажать '
                             'на кнопку <b>"📅 Расписание"</b> и выбрать нужный курс.\n\n'
                             '- Для того, посмотреть популярные вопросы и ответы в меню нажать'
                             'на кнопку <b>"⁉ FAQ"</b> и выбрать свой вопрос.', parse_mode='HTML')
    elif message.text == '⬅ В главное меню':
        await message.answer('Возвращение в главное меню', reply_markup=always_stay_keyboard())
        await message.answer('Главное меню:\n'
                             '- Расписание - здесь можно посмотреть расписание\n'
                             '- FAQ - часто задаваемые вопросы и ответы на них\n'
                             '- Библиотека - поиск книг',
                             reply_markup=inline_keyboard_menu())
