from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from keyboards.inline.callback_datas import buy_callback
choice = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text='Купить Пиво', callback_data=buy_callback.new(
                item_name='bear', quantity=2
            )),
            InlineKeyboardButton(text='Купить Сиги', callback_data=buy_callback.new(
                item_name='cigar', quantity=4
            )),
        ],
        [
            InlineKeyboardButton(text='Отмена', callback_data='cancel_buy'),
        ]
    ]
)

pivo_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text='Купи тут', url='https://www.youtube.com/results?search_query=aiogram+бот')
        ]
    ]
)

sigi_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text='Купи тут', url='https://stackoverflow.com/questions/55647358/how-do-i-solve-error-dotenv-installation-error-on-pycharm')
        ]
    ]
)