import asyncio
from asyncpg import ErrorInAssignmentError, Connection, Record
from loader import db
import logging


# Almau Shop получение данных о мерче
async def almaushop_select_data():
    pool: Connection = db
    try:
        async with pool.acquire() as connection:
            sql_select = "SELECT * FROM almau_shop_products"
            record: Record = await connection.fetch(sql_select)
            return record
    except(Exception, ErrorInAssignmentError) as error:
        logging.info(error)


# Добавления мерча в таблицу 'almau_shop_products'
async def add_almau_shop_data(id_Telegram, product_name, price, currency, img, url):
    pool: Connection = db
    try:
        async with pool.acquire() as connection:
            # async with pool.transaction():
            sql_ex = "Insert into almau_shop_products(id_telegram, product_name, price, currency, img, url) values ($1,$2,$3,$4,$5,$6)"
            record: Record = await connection.fetchrow(sql_ex, int(id_Telegram), str(product_name), int(price),
                                                       str(currency),
                                                       str(img), str(url))
            logging.info(f"ADD data of merch from almaushop website to table")
            return record
    except(Exception, ErrorInAssignmentError) as error:
        logging.info(error)


# Полная очистка таблицы almau_shop_products
async def clear_almaushop_table():
    pool: Connection = db
    try:
        async with pool.acquire() as connection:
            # async with pool.transaction():
            sql_ex = "DELETE FROM almau_shop_products;"
            record: Record = await connection.fetchrow(sql_ex)
            logging.info(f"All data deleted from almau_shop_products table")
            return record
    except(Exception, ErrorInAssignmentError) as error:
        logging.info(error)


async def main():
    print(await almaushop_select_data())


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    run = loop.run_until_complete(main())
