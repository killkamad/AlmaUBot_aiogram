from aiogram.dispatcher.filters.state import StatesGroup, State


class AdminSendAll(StatesGroup):
    message_text = State()
    message_photo = State()
    message_send_all_users = State()


class AdminSendScheduleToBot(StatesGroup):
    button_name = State()
    send_file = State()