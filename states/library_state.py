from aiogram.dispatcher.filters.state import StatesGroup, State

class EmailReg(StatesGroup):
    names = State()