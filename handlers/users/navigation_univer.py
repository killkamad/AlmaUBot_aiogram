import ast
import logging

from aiogram.types import CallbackQuery
from loader import dp, bot
from keyboards.inline.navigation_buttons import inline_keyboard_nav_unifi, inline_keyboard_contacts_center, \
    inline_keyboard_contacts_center_back
from utils import db_api as db




@dp.callback_query_handler(text='/nav_unifi')
async def callback_inline_nav_unifi(call: CallbackQuery):
    logging.info(f"User({call.message.chat.id}) вошел в Навигацию")
    await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                text='Навигация по университету', reply_markup=inline_keyboard_nav_unifi())

@dp.callback_query_handler(text='contacts_center')
async def callback_inline_contacts_center(call: CallbackQuery):
    logging.info(f"User({call.message.chat.id}) вошел в Контакты ключевых центров")
    await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                text='Контакты ключевых центров', reply_markup=await inline_keyboard_contacts_center())


@dp.callback_query_handler(text_contains="['contacts_center_call'")
async def callback_inline_contacts_center_call(call: CallbackQuery):
    logging.info(f'call = {call.data}')
    valueFromCallBack = ast.literal_eval(call.data)[1]
    description = await db.contact_center_description(valueFromCallBack)
    await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                text=description, reply_markup = inline_keyboard_contacts_center_back())