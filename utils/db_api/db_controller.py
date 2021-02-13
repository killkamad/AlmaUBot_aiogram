import asyncio
from asyncpg import ErrorInAssignmentError, Connection, Record
from loader import db
import logging


############## Для тестов ####################
# async def insert_data():
#     pool: Connection = db
#     try:
#         async with pool.acquire() as connection:
#             # async with pool.transaction():
#             sql_select = "Insert into users(username, firstname, lastname, idt, date_time) values ('dedus1337', 'Иван', 'Иванов', 555455, to_timestamp(now(), 'dd-mm-yyyy hh24:mi:ss'));"
#             await connection.execute(sql_select)
#     except(Exception, ErrorInAssignmentError) as error:
#         logging.info(error)
###############################################


# Тестировочка времени
# async def test_test():
#     pool: Connection = db
#     try:
#         async with pool.acquire() as connection:
#             # async with pool.transaction():
#             sql_ex = "SELECT date_time From users WHERE date_time IS NOT NULL"
#             record: Record = await pool.fetch(sql_ex)
#             return record
#     except(Exception, ErrorInAssignmentError) as error:
#         logging.info(error)

# async def main():
#     print((await find_user_by_telegram_id(468899120))['phone'])
#
#
# if __name__ == '__main__':
#     loop = asyncio.get_event_loop()
#     run = loop.run_until_complete(main())
