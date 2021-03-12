import asyncio
from asyncpg import ErrorInAssignmentError, Connection, Record
from loader import db
import logging


async def aws_select_data_schedule():
    pool: Connection = db
    try:
        async with pool.acquire() as connection:
            sql_select = "SELECT * FROM schedule ORDER BY id;"
            record: Record = await connection.fetch(sql_select)
            return record
    except(Exception, ErrorInAssignmentError) as error:
        logging.info(error)


async def find_schedule_id(schedule_id):
    pool: Connection = db
    try:
        async with pool.acquire() as connection:
            sql_select = "SELECT id_sched FROM schedule WHERE id = $1;"
            record: Record = await connection.fetchrow(sql_select, int(schedule_id))
            record = list(record)[0]
            return record
    except(Exception, ErrorInAssignmentError) as error:
        logging.info(error)


async def find_schedule_name_by_id(schedule_id):
    pool: Connection = db
    try:
        async with pool.acquire() as connection:
            sql_select = "SELECT name_sched FROM schedule WHERE id = $1;"
            record: Record = await connection.fetchval(sql_select, int(schedule_id))
            return record
    except(Exception, ErrorInAssignmentError) as error:
        logging.info(error)


async def add_schedule_data(id_Telegram, id_sched, name_sched):
    pool: Connection = db
    try:
        async with pool.acquire() as connection:
            # async with pool.transaction():
            sql_ex = "Insert into schedule(id_Telegram, id_sched, name_sched) values ($1,$2,$3)"
            record: Record = await connection.fetchrow(sql_ex, int(id_Telegram), str(id_sched), str(name_sched))
            logging.info(f"ADD schedule ({name_sched})")
            return record
    except(Exception, ErrorInAssignmentError) as error:
        logging.info(error)


async def update_schedule_data(id_Telegram, id_sched, name_sched):
    pool: Connection = db
    try:
        async with pool.acquire() as connection:
            # async with pool.transaction():
            sql_ex = "Update schedule set id_Telegram = $1, id_sched = $2 Where name_sched = $3"
            record: Record = await connection.fetchrow(sql_ex, int(id_Telegram), str(id_sched), str(name_sched))
            logging.info(f"UPDATED schedule ({name_sched})")
            return record
    except(Exception, ErrorInAssignmentError) as error:
        logging.info(error)


# Удлаение кнопки расписания
async def delete_schedule_button(name_sched):
    pool: Connection = db
    try:
        async with pool.acquire() as connection:
            # async with pool.transaction():
            sql_ex = "Delete from schedule where name_sched = $1"
            record: Record = await connection.fetchrow(sql_ex, str(name_sched))
            logging.info(f"DELETED schedule ({name_sched})")
            return record
    except(Exception, ErrorInAssignmentError) as error:
        logging.info(error)


# Полная очистка таблицы с расписанием
async def clear_schedule_table(table_name):
    pool: Connection = db
    try:
        async with pool.acquire() as connection:
            # async with pool.transaction():
            sql_ex = "DELETE FROM schedule;"
            record: Record = await connection.fetchrow(sql_ex)
            logging.info(f"All data deleted from ({table_name} table")
            return record
    except(Exception, ErrorInAssignmentError) as error:
        logging.info(error)


async def main():
    print(await find_schedule_name_by_id(17))


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    run = loop.run_until_complete(main())
