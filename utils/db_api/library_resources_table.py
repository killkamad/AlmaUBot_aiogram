import asyncio
from asyncpg import ErrorInAssignmentError, Connection, Record
from loader import db
import logging


async def add_lib_resource(id_Telegram, button_name, lib_url, lib_type):
    pool: Connection = db
    try:
        async with pool.acquire() as connection:
            sql_ex = "Insert into library_resources(id_Telegram, button_name , lib_url, lib_type, date_time) values ($1,$2,$3,$4, now())"
            record: Record = await connection.fetchrow(sql_ex, int(id_Telegram), str(button_name), str(lib_url), str(lib_type))
            logging.info(f"ADD resource ({button_name})")
            return record
    except(Exception, ErrorInAssignmentError) as error:
        logging.info(error)


async def select_data_lib_resource(lib_type):
    pool: Connection = db
    try:
        async with pool.acquire() as connection:
            sql_select = "SELECT * FROM library_resources WHERE lib_type = $1"
            record: Record = await connection.fetch(sql_select, lib_type)
            return record
    except(Exception, ErrorInAssignmentError) as error:
        logging.info(error)


async def select_data_lib_resource_reg():
    pool: Connection = db
    try:
        async with pool.acquire() as connection:
            sql_select = "SELECT * FROM library_resources WHERE lib_type = 'reg'"
            record: Record = await connection.fetch(sql_select)
            return record
    except(Exception, ErrorInAssignmentError) as error:
        logging.info(error)


async def select_data_lib_resource_kz():
    pool: Connection = db
    try:
        async with pool.acquire() as connection:
            sql_select = "SELECT * FROM library_resources WHERE lib_type = 'kz'"
            record: Record = await connection.fetch(sql_select)
            return record
    except(Exception, ErrorInAssignmentError) as error:
        logging.info(error)


async def select_data_lib_resource_frgn():
    pool: Connection = db
    try:
        async with pool.acquire() as connection:
            sql_select = "SELECT * FROM library_resources WHERE lib_type = 'foreign'"
            record: Record = await connection.fetch(sql_select)
            return record
    except(Exception, ErrorInAssignmentError) as error:
        logging.info(error)


async def select_data_lib_resource_online():
    pool: Connection = db
    try:
        async with pool.acquire() as connection:
            sql_select = "SELECT * FROM library_resources WHERE lib_type = 'online'"
            record: Record = await connection.fetch(sql_select)
            return record
    except(Exception, ErrorInAssignmentError) as error:
        logging.info(error)


async def delete_library_resource(id):
    pool: Connection = db
    try:
        async with pool.acquire() as connection:
            sql_ex = "Delete from library_resources where id = $1"
            record: Record = await connection.fetchrow(sql_ex, int(id))
            logging.info(f"DELETED resource ({id})")
            return record
    except(Exception, ErrorInAssignmentError) as error:
        logging.info(error)


async def find_library_resource(id):
    pool: Connection = db
    try:
        async with pool.acquire() as connection:
            sql_ex = "SELECT * from library_resources where id = $1"
            record: Record = await connection.fetchrow(sql_ex, int(id))
            return record
    except(Exception, ErrorInAssignmentError) as error:
        logging.info(error)


async def main():
    print('Library resources admin')


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    run = loop.run_until_complete(main())
