from aiogram.dispatcher.filters.state import StatesGroup, State


class MassMailSending(StatesGroup):
    message_text = State()
    message_attached = State()
    message_send_all_users = State()


class SendScheduleToBot(StatesGroup):
    button_name = State()
    send_file = State()


class UpdateSchedule(StatesGroup):
    button_name = State()
    send_file = State()


class DeleteSchedule(StatesGroup):
    confirm_delete = State()


class SendAcademCalendar(StatesGroup):
    send_file = State()


class CreateFaqAlmauShop(StatesGroup):
    question = State()
    answer = State()


class EditFaqAlmauShop(StatesGroup):
    choice = State()
    selected_item = State()
    question_confirm = State()
    answer_confirm = State()


class DeleteFaqAlmauShop(StatesGroup):
    confirm_delete = State()


class CreateMainFaq(StatesGroup):
    question = State()
    answer = State()


class DeleteMainFaq(StatesGroup):
    question = State()
    confirm_delete = State()


class EditMainFaq(StatesGroup):
    button_name = State()
    choice = State()
    selected_item = State()
    question_confirm = State()
    answer_confirm = State()


class EditButtonContentAlmauShop(StatesGroup):
    button_content = State()
    confirm = State()


class EditButtonContentLibrary(StatesGroup):
    button_content = State()
    confirm = State()


class SendContactCenter(StatesGroup):
    name = State()
    description = State()


class UpdateContactCenter(StatesGroup):
    name = State()
    description = State()


class DeleteContactCenter(StatesGroup):
    name = State()
    confirm_delete = State()


class UpdateUserRole(StatesGroup):
    phone = State()
    role = State()
    confirm = State()


class Pps_admin(StatesGroup):
    shcool = State()
    position = State()
    description = State()


class SendCertificate(StatesGroup):
    request = State()
    button_name = State()
    send_file = State()
    upload = State()
    request_state = State()


class UpdateCertificate(StatesGroup):
    request = State()
    button_name = State()
    send_file = State()


class DeleteCertificate(StatesGroup):
    request = State()
    button_name = State()
    confirm_delete = State()



class Map_navigation(StatesGroup):
    building = State()
    floor = State()
    cabinet = State()
    description = State()


class Map_navigation_update(StatesGroup):
    building = State()
    floor = State()
    cabinet = State()
    description = State()


class Map_navigation_delete(StatesGroup):
    building = State()
    floor = State()
    cabinet = State()
