import asyncio
from asyncpg import ErrorInAssignmentError, Connection, Record
from loader import db
import logging


# Almau Shop получение данных о книгах
async def almaushop_select_books():
    pool: Connection = db
    try:
        async with pool.acquire() as connection:
            sql_select = "SELECT * FROM almau_shop_books"
            record: Record = await connection.fetch(sql_select)
            return record
    except(Exception, ErrorInAssignmentError) as error:
        logging.info(error)


# Добавления книг в таблицу 'almau_shop_books'
async def add_almau_shop_books(id_Telegram, book_name, book_author, price, currency, img, url):
    pool: Connection = db
    try:
        async with pool.acquire() as connection:
            # async with pool.transaction():
            sql_ex = "Insert into almau_shop_books(id_telegram, book_name, book_author, price, currency, img, url) values ($1,$2,$3,$4,$5,$6,$7)"
            record: Record = await connection.fetchrow(sql_ex, int(id_Telegram), str(book_name), str(book_author),
                                                       int(price), str(currency),
                                                       str(img), str(url))
            logging.info(f"ADD data of books from almaushop website to table")
            return record
    except(Exception, ErrorInAssignmentError) as error:
        logging.info(error)


# Полная очистка таблицы almau_shop_books
async def clear_almaushop_books_table():
    pool: Connection = db
    try:
        async with pool.acquire() as connection:
            # async with pool.transaction():
            sql_ex = "DELETE FROM almau_shop_books;"
            record: Record = await connection.fetchrow(sql_ex)
            logging.info(f"All data deleted from almau_shop_books table")
            return record
    except(Exception, ErrorInAssignmentError) as error:
        logging.info(error)


async def main():
    print(await almaushop_select_books())


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    run = loop.run_until_complete(main())
