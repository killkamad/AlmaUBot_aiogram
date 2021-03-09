import asyncio
from asyncpg import ErrorInAssignmentError, Connection, Record
from loader import db
import logging


async def add_pps_data(id_Telegram, shcool, position, description, photo_id):
    pool: Connection = db
    try:
        async with pool.acquire() as connection:
            # async with pool.transaction():
            sql_ex ='''
                    UPDATE tutors_and_employees
                    SET id_Telegram = $1, description = $4, photo_id = $5, date_time = now()
                    WHERE shcool = $2 and position = $3
                    '''
            record: Record = await connection.fetchrow(sql_ex, int(id_Telegram), str(shcool),
                                                       str(position), str(description), str(photo_id))
            logging.info(f"ADD info to ({shcool}) shcool")
            return record
    except(Exception, ErrorInAssignmentError) as error:
        logging.info(error)


async def add_pps_data_photo(id_Telegram, shcool, position, photo_id):
    pool: Connection = db
    try:
        async with pool.acquire() as connection:
            # async with pool.transaction():
            sql_ex ='''
                    UPDATE tutors_and_employees
                    SET id_Telegram = $1, photo_id = $4, date_time = now()
                    WHERE shcool = $2 and position = $3
                    '''
            record: Record = await connection.fetchrow(sql_ex, int(id_Telegram), str(shcool),
                                                       str(position), str(photo_id))
            logging.info(f"ADD info to ({shcool}) shcool")
            return record
    except(Exception, ErrorInAssignmentError) as error:
        logging.info(error)


async def add_pps_data_description(id_Telegram, shcool, position, description):
    pool: Connection = db
    try:
        async with pool.acquire() as connection:
            # async with pool.transaction():
            sql_ex ='''
                    UPDATE tutors_and_employees
                    SET id_Telegram = $1, description = $4, date_time = now()
                    WHERE shcool = $2 and position = $3
                    '''
            record: Record = await connection.fetchrow(sql_ex, int(id_Telegram), str(shcool),
                                                       str(position), str(description))
            logging.info(f"ADD info to ({shcool}) shcool")
            return record
    except(Exception, ErrorInAssignmentError) as error:
        logging.info(error)

async def find_photoid_pps(shcool, position):
    pool: Connection = db
    try:
        async with pool.acquire() as connection:
            sql_select = "SELECT photo_id FROM tutors_and_employees WHERE shcool = $1 and position = $2;"
            record: Record = await connection.fetchval(sql_select, str(shcool), str(position))
            return record
    except(Exception, ErrorInAssignmentError) as error:
        logging.info(error)


async def pps_center_description(shcool, position):
    pool: Connection = db
    try:
        async with pool.acquire() as connection:
            sql_select = "SELECT description FROM tutors_and_employees WHERE shcool = $1 and position=$2 ORDER BY id DESC LIMIT 1;"
            record: Record = await connection.fetchrow(sql_select, str(shcool), str(position))
            record = list(record)[0]
            return record
    except(Exception, ErrorInAssignmentError) as error:
        logging.info(error)


# async def main():
#     print(await pps_center_description())
#
#
# if __name__ == '__main__':
#     loop = asyncio.get_event_loop()
#     run = loop.run_until_complete(main())
