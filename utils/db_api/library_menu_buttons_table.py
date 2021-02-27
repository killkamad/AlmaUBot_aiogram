import asyncio
from asyncpg import ErrorInAssignmentError, Connection, Record
from loader import db
import logging


async def select_library_menu_button_content(button_name):
    pool: Connection = db
    try:
        async with pool.acquire() as connection:
            sql_select = "SELECT button_content FROM library_menu_buttons WHERE button_name = $1;"
            record: Record = await connection.fetchval(sql_select, str(button_name))
            return record
    except(Exception, ErrorInAssignmentError) as error:
        logging.info(error)


async def edit_library_menu_button(id_telegram, button_name, button_content):
    pool: Connection = db
    try:
        async with pool.acquire() as connection:
            sql_ex = "Update library_menu_buttons set id_telegram = $1, button_content = $3, date_time = now() Where button_name = $2"
            record: Record = await connection.fetch(sql_ex, int(id_telegram), str(button_name), str(button_content))
            logging.info(f"EDIT library button = ({button_name})")
            return record
    except(Exception, ErrorInAssignmentError) as error:
        logging.info(error)


async def main():
    print('Library admin menu buttons')


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    run = loop.run_until_complete(main())
