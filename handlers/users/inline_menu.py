import logging

from keyboards.inline.callback_datas import buy_callback
from loader import dp, bot
from aiogram.types import Message, CallbackQuery
from keyboards.inline.choice_buttons import choice, pivo_keyboard, sigi_keyboard
from aiogram.dispatcher.filters import Command


@dp.message_handler(Command('items'))
async def show_items(message: Message):
    await message.answer(text='На продажу у нас есть 2 товара: 2 Сиги и 1 Пиво. \n'
                              'Если ничо не надо жми отмену',
                         reply_markup=choice)


@dp.callback_query_handler(text_contains='bear')
async def callback_inline(call: CallbackQuery):
    call_data = call.data
    logging.info(f'call = {call_data}')

    await call.message.answer('Вы выбрали Пиво, спасибо', reply_markup=pivo_keyboard)


@dp.callback_query_handler(buy_callback.filter(item_name='cigar'))
async def buy_some(call: CallbackQuery, callback_data: dict):
    logging.info(f'call = {callback_data}')
    quantity = callback_data.get('quantity')
    await call.message.answer(f'Вы выбрали Сиги, сиг всего {quantity}, спасибо', reply_markup=sigi_keyboard)


@dp.callback_query_handler(text='cancel_buy')
async def buy_some(call: CallbackQuery):
    await call.message.answer('Вы отменили эту покупку!')
    await call.message.edit_reply_markup()