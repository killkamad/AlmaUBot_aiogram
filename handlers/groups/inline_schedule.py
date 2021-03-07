import logging
from loader import dp, bot
# Импортирование функций из БД контроллера
from utils import db_api as db

from aiogram.types import InlineQuery, \
    InputTextMessageContent, InlineQueryResultArticle, InlineQueryResultCachedDocument, InlineQueryResultCachedPhoto
import hashlib


@dp.inline_handler(lambda inline_query: True)
async def inline_schedule(inline_query: InlineQuery):
    schedule_list = await db.aws_select_data_schedule()
    # text = inline_query.query or [i['name_sched'] for i in schedule]
    # print(text)
    # input_content = InputTextMessageContent(text)
    # result_id: str = hashlib.md5(text.encode()).hexdigest()
    # print(result_id)
    results = []
    try:
        for i, schedule in enumerate(schedule_list):
            results.append(InlineQueryResultCachedDocument(
                id=i + 1,
                title=f'{schedule["name_sched"]} Расписание',
                document_file_id=schedule["id_sched"],
                # document_file_id="BQACAgIAAxkBAAJwsGBEzD4EXwFiDyQyFft1NB1dddL9AAJTCwACPSMoStz_dcjkQIcgHgQ"
            ))
    except Exception as e:
        print(e)
    # don't forget to set cache_time=1 for testing (default is 300s or 5m)
    await bot.answer_inline_query(inline_query.id, results=results, cache_time=1)
