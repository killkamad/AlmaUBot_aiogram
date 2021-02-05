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


class CreateFaqAlmauShop(StatesGroup):
    question = State()
    answer = State()


class DeleteFaqAlmauShop(StatesGroup):
    question = State()
    confirm_delete = State()


class EditFaqAlmauShop(StatesGroup):
    button_name = State()
    choice = State()
    selected_item = State()
    question_confirm = State()
    answer_confirm = State()


class SendContactCenter(StatesGroup):
    name = State()
    description = State()


class UpdateContactCenter(StatesGroup):
    name = State()
    description = State()


class DeleteContactCenter(StatesGroup):
    name = State()
    confirm_delete = State()
