from aiogram.dispatcher.filters.state import StatesGroup, State


class CertificateRequest(StatesGroup):
    names = State()
    email = State()
    phone = State()
    type = State()
    upload = State()
