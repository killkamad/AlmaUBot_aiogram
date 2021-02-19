from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from utils import db_api as db
from .callback_datas import schedule_callback


async def inline_keyboard_schedule():
    markup = InlineKeyboardMarkup(row_width=2)
    schedule = await db.aws_select_data_schedule()
    markup.add(*[InlineKeyboardButton(text=item['name_sched'], callback_data=schedule_callback.new(schedule_name=item["name_sched"])) for item in schedule])
    # markup.add(InlineKeyboardButton(text="⬅ Назад", callback_data="go_back"))
    return markup
