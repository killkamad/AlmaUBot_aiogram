import asyncio
import logging

from aiogram import types
from aiogram.types import CallbackQuery, InputMediaPhoto, ChatActions
from math import ceil
from keyboards.inline import almau_shop_faq_callback
from keyboards.inline.almaushop_buttons import inline_keyboard_faq_almaushop, inline_keyboard_faq_almaushop_back
from loader import dp, bot
# Импортирование функций из БД контроллера
from utils import db_api as db
from utils.get_linenumber import get_linenumber
from utils.misc import rate_limit

from data.button_names.almaushop_buttons import almaushop_products_button, almaushop_books_button, \
    almaushop_website_button, \
    almaushop_contacts_button, almaushop_faq_button, almaushop_def_buttons


# Библиотека регулярных выражений
@rate_limit(3)
@dp.message_handler(lambda message: message.text in [almaushop_products_button, almaushop_books_button])
async def almaushop_text_buttons_parser_handler(message: types.Message):
    logging.info(f"User({message.chat.id}) нажал на {message.text}")
    await db.add_bot_log(message.chat.id, message.text, f"{__name__}.py [LINE:{get_linenumber()}]")
    albums_list = []
    start = 0
    messages_sent = 0
    if message.text == almaushop_products_button:
        data = await db.almaushop_select_data()
        for item in data:
            text = f'<u><a href="{item["url"]}">{item["product_name"]}</a></u> \n' \
                   f'{item["price"]} {item["currency"]}\n'
            albums_list.append(InputMediaPhoto(item["img"], caption=text))
    elif message.text == almaushop_books_button:
        data = await db.almaushop_select_books()
        for item in data:
            text = f'<u><a href="{item["url"]}">{item["book_name"]}</a></u> \n' \
                   f'{item["book_author"]} \n' \
                   f'{item["price"]} {item["currency"]}\n'
            albums_list.append(InputMediaPhoto(item["img"], caption=text))
    for i in range(1, ceil(len(albums_list) / 10) + 1):
        await bot.send_chat_action(message.chat.id, ChatActions.UPLOAD_PHOTO)
        await bot.send_media_group(message.chat.id, albums_list[start:10 * i])
        start += 10
        messages_sent += 1
        if messages_sent % 30 == 0:
            await asyncio.sleep(1)
            messages_sent = 0


@rate_limit(1)
@dp.message_handler(lambda message: message.text in almaushop_def_buttons)
async def almaushop_text_buttons_handler(message: types.Message):
    logging.info(f"User({message.chat.id}) нажал на {message.text}")
    await db.add_bot_log(message.chat.id, message.text, f"{__name__}.py [LINE:{get_linenumber()}]")
    if message.text == almaushop_website_button:
        button_content = await db.select_almau_shop_menu_button_content(message.text)
        await bot.send_message(chat_id=message.chat.id,
                               text=button_content)
    elif message.text == almaushop_contacts_button:
        button_content = await db.select_almau_shop_menu_button_content(message.text)
        await bot.send_message(message.chat.id,
                               text=button_content)
    elif message.text == almaushop_faq_button:
        text = "AlmaU Shop F.A.Q ↘"
        await bot.send_message(message.chat.id, text=text, reply_markup=await inline_keyboard_faq_almaushop())


@dp.callback_query_handler(almau_shop_faq_callback.filter())
async def almaushop_faq_menu(call: CallbackQuery, callback_data: dict):
    id = callback_data.get('callback_id')
    answer = await db.almaushop_faq_find_answer(id)
    await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                text=answer, reply_markup=inline_keyboard_faq_almaushop_back())
    await call.answer()


@dp.callback_query_handler(text='back_to_almau_shop_faq')
async def almaushop_faq_menu_back(call: CallbackQuery):
    logging.info(f'User({call.message.chat.id}) вернулся в админ меню')
    await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                text="F.A.Q ↘",
                                reply_markup=await inline_keyboard_faq_almaushop())
    await call.answer()
