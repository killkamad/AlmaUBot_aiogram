import asyncio
from asyncpg import ErrorInAssignmentError, Connection, Record
from loader import db
import logging


async def add_feedback_msg_data(id_Telegram, full_name, phone, email, message_content):
    pool: Connection = db
    try:
        async with pool.acquire() as connection:
            # async with pool.transaction():
            sql_ex = "Insert into message_to_rector(id_Telegram, full_name, phone, email, message_content, date_time) values ($1,$2,$3,$4,$5, now())"
            record: Record = await connection.fetchrow(sql_ex, int(id_Telegram), str(full_name), str(phone), str(email),
                                                       str(message_content))
            logging.info(f"ADD messages for feedback to rector")
            return record
    except(Exception, ErrorInAssignmentError) as error:
        logging.info(error)

# async def main():
#     print(await main_faq_select_question_and_answer(1))
#
#
# if __name__ == '__main__':
#     loop = asyncio.get_event_loop()
#     run = loop.run_until_complete(main())