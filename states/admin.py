from aiogram.dispatcher.filters.state import StatesGroup, State


class SendAll(StatesGroup):
    message_text = State()
    message_photo = State()
    message_send_all_users = State()


class SendScheduleToBot(StatesGroup):
    button_name = State()
    send_file = State()


class UpdateSchedule(StatesGroup):
    button_name = State()
    send_file = State()


class DeleteSchedule(StatesGroup):
    button_name = State()
    confirm_delete = State()

class SendAcademCalendar(StatesGroup):
    send_file = State()