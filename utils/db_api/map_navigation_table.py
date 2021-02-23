import asyncio
from asyncpg import ErrorInAssignmentError, Connection, Record
from loader import db
import logging


async def add_map_navigation_data(id_Telegram, building, floor, cabinet, cabinet_description):
    pool: Connection = db
    try:
        async with pool.acquire() as connection:
            # async with pool.transaction():
            sql_ex = "Insert into map_navigation(id_Telegram, building, floor, cabinet, cabinet_description,date_time) values ($1,$2,$3,$4,$5,now())"
            record: Record = await connection.fetchrow(sql_ex, int(id_Telegram), str(building),
                                                       str(floor), str(cabinet), str(cabinet_description))
            logging.info(f"ADD map_navigation ({cabinet})")
            return record
    except(Exception, ErrorInAssignmentError) as error:
        logging.info(error)

# building, floor
async def map_nav_description(building, floor):
    pool: Connection = db
    try:
        async with pool.acquire() as connection:
            sql_select = "SELECT cabinet, cabinet_description FROM map_navigation WHERE building = $1 and floor=$2 ORDER BY cabinet;"
            record: Record = await connection.fetch(sql_select, str(building), str(floor))
            return record
    except(Exception, ErrorInAssignmentError) as error:
        logging.info(error)


async def find_cabinet_description(cabinet):
    pool: Connection = db
    try:
        async with pool.acquire() as connection:
            sql_select = "SELECT cabinet_description FROM map_navigation WHERE cabinet = $1;"
            record: Record = await connection.fetchval(sql_select, str(cabinet))
            return record
    except(Exception, ErrorInAssignmentError) as error:
        logging.info(error)


async def select_cabinet_admin(id):
    pool: Connection = db
    try:
        async with pool.acquire() as connection:
            sql_select = "SELECT cabinet FROM map_navigation WHERE id = $1;"
            record: Record = await connection.fetchrow(sql_select, int(id))
            return record
    except(Exception, ErrorInAssignmentError) as error:
        logging.info(error)


async def select_cabinet_admin_check():
    pool: Connection = db
    try:
        async with pool.acquire() as connection:
            sql_select = "SELECT cabinet FROM map_navigation ORDER BY id;"
            record: Record = await connection.fetch(sql_select)
            return record
    except(Exception, ErrorInAssignmentError) as error:
        logging.info(error)


async def update_map_nav_description_data(id_Telegram, building, floor, cabinet, cabinet_description):
    pool: Connection = db
    try:
        async with pool.acquire() as connection:
            # async with pool.transaction():
            sql_ex = "Update map_navigation set id_Telegram = $1, cabinet_description = $5 Where building = $2 and floor = $3 and cabinet = $4"
            record: Record = await connection.fetchrow(sql_ex, int(id_Telegram), str(building),
                                                       str(floor), str(cabinet), str(cabinet_description))
            logging.info(f"UPDATED cabinet ({cabinet})")
            return record
    except(Exception, ErrorInAssignmentError) as error:
        logging.info(error)


async def delete_map_nav_description_data(building, floor, cabinet):
    pool: Connection = db
    try:
        async with pool.acquire() as connection:
            # async with pool.transaction():
            sql_ex = "Delete from map_navigation where building = $1 and floor = $2 and cabinet = $3"
            record: Record = await connection.fetchrow(sql_ex, str(building),
                                                       str(floor), str(cabinet))
            logging.info(f"DELETED cabinet ({cabinet})")
            return record
    except(Exception, ErrorInAssignmentError) as error:
        logging.info(error)


async def main():
    print("gg wp")


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    run = loop.run_until_complete(main())