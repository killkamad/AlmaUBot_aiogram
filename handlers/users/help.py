import logging
from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandHelp
from loader import dp
from utils.misc import rate_limit
from utils import db_api as db

message_for_admin = '<b>О боте:</b>\n\n' \
                    '- Для загрузки расписания, войти в меню админа - /admin ' \
                    'и нажать на кнопку <b>"📤 Загрузить расписание"</b>.\n\n' \
                    '- Для обновление расписания, войти в меню админа - /admin ' \
                    'и нажать на кнопку <b>"♻ Обновить расписание"</b>.\n\n' \
                    '- Для удаления расписания, войти в меню админа - /admin ' \
                    'и нажать на кнопку <b>"❌ Удалить расписание"</b>.\n\n' \
                    '- Для обновления данных о товаре для подменю AlmaU Shop, войти в меню админа - /admin ' \
                    'и нажать на кнопку\n <b>"👔 Обновить мерч AlmaU Shop"</b>.\n\n' \
                    '- Для создания массовой рассылки, войти в меню админа - /admin ' \
                    'и нажать на кнопку <b>"📣 Рассылка"</b>, сообщение может содержать максимум' \
                    ' 1000 символов, к сообщению можно прикрепить фото или файл.\n\n'

message_for_user = '<b>О боте:</b>\n\n' \
                   '- Для получения файла с расписанием, в главном меню нажать ' \
                   'на кнопку <b>"📅 Расписание"</b> и выбрать нужный курс.\n\n' \
                   '- Для того, чтобы посмотреть популярные вопросы и ответы в меню нажать' \
                   'на кнопку <b>"⁉ FAQ"</b> и выбрать свой вопрос.\n\n' \
                   '- Для регистрации на лицензионные базы данных в меню нажать на кнопку\n <b>"📚 Библиотека"</b> ➡' \
                   ' <b>"⚡ Электронные ресурсы"</b> ➡ <b>"📕 Лицензионные Базы Данных"</b> ➡' \
                   ' <b>"Зарегистрироваться"</b>\n\n' \
                   '- Для просмотра брендированной продукции и книг AlmaU в меню ' \
                   'нажать на кнопку <b>"🌀 AlmaU Shop"</b>.\n\n' \
                   '- Для получения академического календаря, в главном меню нажать на кнопку' \
                   ' <b>"🗒 Академический календарь"</b>\n\n' \
                   '- Для получения справок в главном меню нажать на кнопку <b>"🏢 Получить справку"</b>\n\n' \
                   '- Для того, чтобы написать письмо эдвайзеру, в главном меню нажать на кнопку <b>"📝 Связь с эдвайзером"</b> ' \
                   'и заполнить нужную информацию\n\n' \
                   '- Для получения информации об аудиториях, в главном меню нажать на кнопку <b>"🗺️ Навигация по университету"</b> ' \
                   'и потом нажать на кнопку <b>"🗺 Навигация по университету"</b>\n\n' \
                   '- Для получения информации о офисах и центах университета, в главном меню нажать ' \
                   'на кнопку <b>"🗺️ Навигация по университету"</b> и потом нажать на <b>"💬 Контакты ключевых центров"</b>\n\n' \
                   '- Для получения информации о преподавателях, деканах, ректору и т.д, в главном меню нажать на кнопку ' \
                   '<b>"🗺️ Навигация по университету"</b> и потом нажать на <b>"👨‍🏫 Профессорско-преподавательский состав"</b>'


@rate_limit(5, 'help')
@dp.message_handler(CommandHelp())
async def bot_help(message: types.Message):
    logging.info(f"User({message.chat.id}) enter {message.text}")
    role = await db.check_role_by_id(message.chat.id)
    try:
        if role == 'admin':
            await message.answer(message_for_admin, parse_mode='HTML')
        else:
            await message.answer(message_for_user, parse_mode='HTML')
    except Exception as e:
        logging.info(f'Ошибка - {e}')
