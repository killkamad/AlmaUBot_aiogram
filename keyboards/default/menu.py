from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

menu = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='Пиво'),
        ],
        [
            KeyboardButton(text='Сиги'),
            KeyboardButton(text='Хавчик')
        ]
    ], resize_keyboard=True)
