from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from utils import db_api as db


async def inline_keyboard_schedule():
    markup = InlineKeyboardMarkup(row_width=3)
    schedule = await db.aws_select_data_schedule()
    call_list = []
    schedule_name = []
    for call_value in schedule:
        callback_data = "['schedule_call', '" + call_value[-1] + "']"
        schedule_name.append(call_value[3])
        # print(callback_data)
        call_list.append(callback_data)
    # print('schedule_name', schedule_name)
    # print(call_list)
    # markup.add(*[types.InlineKeyboardButton(text=schedule[button][3], callback_data=schedule[button][3]) for button in
    #              range(0, len(schedule))])
    markup.add(*[InlineKeyboardButton(text=button, callback_data=call_data) for button, call_data in
                 zip(schedule_name, call_list)])
    # for i in schedule:
    #     print(i)
    markup.add(InlineKeyboardButton(text="🔙 Назад", callback_data="go_back"))
    return markup
