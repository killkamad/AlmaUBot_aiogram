import asyncio
import logging

from aiogram import types
from aiogram.types import CallbackQuery

from keyboards.inline import almau_shop_faq_callback
from keyboards.inline.almaushop_buttons import inline_keyboard_faq_almaushop, inline_keyboard_faq_almaushop_back
from loader import dp, bot
# Импортирование функций из БД контроллера
from utils import db_api as db
from utils.misc import rate_limit


# Библиотека регулярных выражений


@rate_limit(1)
@dp.message_handler(lambda message: message.text in ['🛍  Мерч', '📚  Книги', '🌐  Вебсайт', '☎  Контакты', '⁉  ЧаВо'])
async def almaushop_text_buttons_handler(message: types.Message):
    logging.info(f"User({message.chat.id}) нажал на {message.text}")
    request = 0
    # Кнопки AlmaU Shop
    if message.text == '🛍  Мерч':
        data = await db.almaushop_select_data()
        for item in data:
            text = f'<u><a href="{item["url"]}">{item["product_name"]}</a></u> \n' \
                   f'{item["price"]} {item["currency"]}\n'
            await bot.send_photo(chat_id=message.chat.id, photo=item["img"], caption=text)
            request += 1
            if request % 30 == 0:
                await asyncio.sleep(2)
                request = 0
    elif message.text == '📚  Книги':
        data = await db.almaushop_select_books()
        for item in data:
            text = f'<u><a href="{item["url"]}">{item["book_name"]}</a></u> \n' \
                   f'{item["book_author"]} \n' \
                   f'{item["price"]} {item["currency"]}\n'
            await bot.send_photo(chat_id=message.chat.id, photo=item["img"], caption=text)
            request += 1
            if request % 30 == 0:
                await asyncio.sleep(2)
                request = 0
    elif message.text == '🌐  Вебсайт':
        await bot.send_message(chat_id=message.chat.id,
                               text='Вебсайт – https://almaushop.kz')
    elif message.text == '☎  Контакты':
        text = 'Контакты: \n' \
               '• Телефон +7 777 227 30 62\n' \
               '• Почта t.possivnаya@almau.edu.kz'
        await bot.send_message(message.chat.id, text=text)
    elif message.text == '⁉  ЧаВо':
        text = "F.A.Q ↘"
        await bot.send_message(message.chat.id, text=text, reply_markup=await inline_keyboard_faq_almaushop())


@dp.callback_query_handler(almau_shop_faq_callback.filter())
async def callback_inline_add_faq_almaushop(call: CallbackQuery, callback_data: dict):
    id = callback_data.get('callback_id')
    answer = await db.almaushop_faq_find_answer(id)
    await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                text=answer, reply_markup=inline_keyboard_faq_almaushop_back())
    logging.info(f'User({call.message.chat.id}) нажал на кнопку {id}')
    logging.info(f'User({call.message.chat.id}) нажал на кнопку {callback_data}')


@dp.callback_query_handler(text='back_to_almau_shop_faq')
async def callback_inline_update_almaushop_merch(call: CallbackQuery):
    logging.info(f'User({call.message.chat.id}) вернулся в админ меню')
    await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                text="F.A.Q ↘",
                                reply_markup=await inline_keyboard_faq_almaushop())
