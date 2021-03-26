from aiogram.dispatcher.filters.state import StatesGroup, State


class RegisterUserPhone(StatesGroup):
    phone = State()
