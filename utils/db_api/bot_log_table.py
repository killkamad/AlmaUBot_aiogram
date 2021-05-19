import asyncio
from asyncpg import ErrorInAssignmentError, Connection, Record
from loader import db
import logging


# Добавление данных академ календаря
async def add_bot_log(id_telegram, action, log_record):
    pool: Connection = db
    try:
        async with pool.acquire() as connection:
            # async with pool.transaction():
            sql_ex = "Insert into bot_log(id_telegram,action,date_time,log_record) values ($1,$2,now(),$3)"
            record: Record = await connection.fetchrow(sql_ex, int(id_telegram), str(action), str(log_record))
            return record
    except(Exception, ErrorInAssignmentError) as error:
        logging.info(error)
