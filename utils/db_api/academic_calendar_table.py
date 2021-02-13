import asyncio
from asyncpg import ErrorInAssignmentError, Connection, Record
from loader import db
import logging


# Поиск последнего академ календаря в базе
async def find_id_academic_calendar():
    pool: Connection = db
    try:
        async with pool.acquire() as connection:
            sql_select = "SELECT id_calendar FROM academic_calendar ORDER BY id DESC LIMIT 1;"
            record: Record = await connection.fetchval(sql_select)
            return record
    except(Exception, ErrorInAssignmentError) as error:
        logging.info(error)


# Добавление данных академ календаря
async def add_academic_calendar_data(id_Telegram, id_calendar):
    pool: Connection = db
    try:
        async with pool.acquire() as connection:
            # async with pool.transaction():
            sql_ex = "Insert into academic_calendar(id_Telegram, id_calendar, date_time) values ($1,$2, now())"
            record: Record = await connection.fetchrow(sql_ex, int(id_Telegram), str(id_calendar))
            logging.info(f"ADD academic calendar")
            return record
    except(Exception, ErrorInAssignmentError) as error:
        logging.info(error)


async def main():
    print(await find_id_academic_calendar())


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    run = loop.run_until_complete(main())
