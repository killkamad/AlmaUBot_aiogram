from aiogram.dispatcher.filters.state import StatesGroup, State


class EmailReg(StatesGroup):
    bookbase = State()
    names = State()
    email = State()
    phone = State()
