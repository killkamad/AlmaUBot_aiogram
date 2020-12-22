from aiogram.dispatcher.filters.state import StatesGroup, State


class FeedbackMessage(StatesGroup):
    names = State()
    email = State()
    phone = State()
    content = State()
