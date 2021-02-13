import asyncio
from asyncpg import ErrorInAssignmentError, Connection, Record
from loader import db
import logging


async def select_almau_shop_menu_button_content(button_name):
    pool: Connection = db
    try:
        async with pool.acquire() as connection:
            sql_select = "SELECT button_content FROM almau_shop_menu_buttons WHERE button_name = $1;"
            record: Record = await connection.fetchval(sql_select, str(button_name))
            return record
    except(Exception, ErrorInAssignmentError) as error:
        logging.info(error)


async def edit_almau_shop_menu_button(id_telegram, button_content, button_name):
    pool: Connection = db
    try:
        async with pool.acquire() as connection:
            sql_ex = "Update almau_shop_menu_buttons set id_Telegram = $1, button_content = $2, date_time = now() Where button_name = $3"
            record: Record = await connection.fetch(sql_ex, int(id_telegram), str(button_content), str(button_name))
            logging.info(f"EDIT almaushop button = ({button_name})")
            return record
    except(Exception, ErrorInAssignmentError) as error:
        logging.info(error)


async def main():
    print(await select_almau_shop_menu_button_content('dadwa'))


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    run = loop.run_until_complete(main())
