from aiogram import types

from keyboards.inline.menu_buttons import inline_keyboard_menu
from loader import dp, bot
import logging

from utils.json_loader import json_data
from utils.misc import rate_limit
from .menu import _main_menu_text
from data.button_names.main_menu_buttons import start_menu_buttons, menu_button, about_button


@rate_limit(1)
@dp.message_handler(lambda message: message.text in start_menu_buttons)
async def bot_echo(message: types.Message):
    logging.info(f'User({message.chat.id}) нажал на кнопку {message.text}')
    # Кнопки главного меню
    if message.text == menu_button:
        await message.answer(_main_menu_text,
                             reply_markup=inline_keyboard_menu())
    elif message.text == about_button:
        await message.answer('<b>О боте:</b>\n\n'
                             '- Для загрузки расписания, войти в меню админа - /admin '
                             'и нажать на кнопку <b>"📤 Загрузить расписание"</b>.\n\n'
                             '- Для обновление расписания, войти в меню админа - /admin '
                             'и нажать на кнопку <b>"♻ Обновить расписание"</b>.\n\n'
                             '- Для удаления расписания, войти в меню админа - /admin '
                             'и нажать на кнопку <b>"❌ Удалить расписание"</b>.\n\n'
                             '- Для обновления данных о товаре для подменю AlmaU Shop, войти в меню админа - /admin '
                             'и нажать на кнопку\n <b>"👔 Обновить мерч AlmaU Shop"</b>.\n\n'
                             '- Для создания массовой рассылки, войти в меню админа - /admin '
                             'и нажать на кнопку <b>"📣 Рассылка"</b>, сообщение может содержать максимум'
                             ' 1000 символов, к сообщению можно прикрепить фото или файл.\n\n'
                             '- Для получения файла с расписанием, в главном меню нажать '
                             'на кнопку <b>"📅 Расписание"</b> и выбрать нужный курс.\n\n'
                             '- Для того, чтобы посмотреть популярные вопросы и ответы в меню нажать'
                             'на кнопку <b>"⁉ FAQ"</b> и выбрать свой вопрос.\n\n'
                             '- Для регистрации на лицензионные базы данных и получении информации'
                             ' по библиотеки в меню нажать на кнопку\n <b>"📚 Библиотека"</b>.\n\n'
                             '- Для просмотра мерча AlmaU и получении информации о AlmaU Shop в меню '
                             'нажать на кнопку <b>"🌀 AlmaU Shop"</b>.',
                             parse_mode='HTML')
