import asyncio
import logging

from aiogram import types
from aiogram.types import CallbackQuery, InputMediaPhoto, ChatActions

from keyboards.inline import almau_shop_faq_callback
from keyboards.inline.almaushop_buttons import inline_keyboard_faq_almaushop, inline_keyboard_faq_almaushop_back
from loader import dp, bot
# Импортирование функций из БД контроллера
from utils import db_api as db
from utils.misc import rate_limit

from data.config import almaushop_products_button, almaushop_books_button, almaushop_website_button, \
    almaushop_contacts_button, almaushop_faq_button, almaushop_def_buttons


# Библиотека регулярных выражений
@rate_limit(3)
@dp.message_handler(lambda message: message.text in almaushop_def_buttons)
async def almaushop_text_buttons_parser_handler(message: types.Message):
    logging.info(f"User({message.chat.id}) нажал на {message.text}")
    # Кнопки AlmaU Shop
    albums_list = []
    albums = 0
    await bot.send_chat_action(message.chat.id, ChatActions.UPLOAD_PHOTO)
    if message.text == almaushop_products_button:
        data = await db.almaushop_select_data()
        for item in data:
            text = f'<u><a href="{item["url"]}">{item["product_name"]}</a></u> \n' \
                   f'{item["price"]} {item["currency"]}\n'
            albums_list.append(InputMediaPhoto(item["img"], caption=text))
            albums += 1
            if albums % 10 == 0:
                await bot.send_media_group(message.chat.id, albums_list)
                await asyncio.sleep(1)
                albums_list.clear()
    elif message.text == almaushop_books_button:
        data = await db.almaushop_select_books()
        for item in data:
            text = f'<u><a href="{item["url"]}">{item["book_name"]}</a></u> \n' \
                   f'{item["book_author"]} \n' \
                   f'{item["price"]} {item["currency"]}\n'
            albums_list.append(InputMediaPhoto(item["img"], caption=text))
            albums += 1
            if albums % 10 == 0:
                await bot.send_media_group(message.chat.id, albums_list)
                await asyncio.sleep(1)
                albums_list.clear()
            # await bot.send_photo(chat_id=message.chat.id, photo=item["img"], caption=text)
            # request += 1
            # if request % 30 == 0:
            #     await asyncio.sleep(2)
            #     request = 0


@rate_limit(1)
@dp.message_handler(lambda message: message.text in almaushop_def_buttons)
async def almaushop_text_buttons_handler(message: types.Message):
    logging.info(f"User({message.chat.id}) нажал на {message.text}")
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
