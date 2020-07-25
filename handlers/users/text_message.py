from aiogram import types
from aiogram.types import ContentType
from keyboards.inline.menu_buttons import inline_keyboard_menu
from loader import dp
import logging
from utils.misc import rate_limit


@rate_limit(1)
@dp.message_handler(content_types=ContentType.TEXT)
async def bot_echo(message: types.Message):
    if message.text == '🏠 Меню':
        logging.info(f'Пользователь {message.from_user.username} вошел в меню')
        await message.answer('Главное меню:\n'
                             '- Расписание - здесь можно посмотреть расписание\n'
                             '- FAQ - часто задаваемые вопросы и ответы на них',
                             reply_markup=inline_keyboard_menu())
    if message.text == '❓ Помощь':
        logging.info(f'Пользователь {message.from_user.username} вошел в помощь')
        await message.answer('Главное меню:\n'
                             '- Расписание - здесь можно посмотреть расписание\n'
                             '- FAQ - часто задаваемые вопросы и ответы на них',
                             reply_markup=inline_keyboard_menu())
    if message.text == '💻 О боте':
        logging.info(f'Пользователь {message.from_user.username} вошел в О боте ')
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

