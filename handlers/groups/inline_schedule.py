import logging
from loader import dp, bot
# Импортирование функций из БД контроллера
from utils import db_api as db
from aiogram.types import InlineQuery, \
    InputTextMessageContent, InlineQueryResultArticle, InlineQueryResultCachedDocument, InlineQueryResultCachedPhoto


@dp.inline_handler(lambda inline_query: True)
async def inline_schedule(inline_query: InlineQuery):
    query = inline_query.query.strip().lower()
    schedule_list = await db.aws_select_data_schedule()
    search_result = []
    results = []
    for item in schedule_list:
        if query in item['name_sched']:
            search_result.append([item['name_sched'], item['id_sched']])
    # result_id: str = hashlib.md5(text.encode()).hexdigest()
    try:
        for i, schedule in enumerate(search_result):
            results.append(InlineQueryResultCachedDocument(
                id=f'{i + 1}',
                title=f'{schedule[0]}',
                document_file_id=schedule[1],
            ))
    except Exception as e:
        logging.info(f'{e}')

    if query and not results:
        results.append(
            InlineQueryResultArticle(
                id='999999',
                title='Расписания с таким названием не найдено',
                input_message_content=InputTextMessageContent(
                    message_text=f'Ничего не нашлось по запросу "{query}"',
                ),
            )
        )
    # don't forget to set cache_time=1 for testing (default is 300s or 5m)
    await bot.answer_inline_query(inline_query.id, results=results, cache_time=1)
