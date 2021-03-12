import asyncio
from asyncpg import ErrorInAssignmentError, Connection, Record
from loader import db
import logging


async def add_contact_center_data(id_Telegram, description_contact_center, name_contact_center):
    pool: Connection = db
    try:
        async with pool.acquire() as connection:
            # async with pool.transaction():
            sql_ex = "Insert into contact_centers(id_Telegram, description_contact_center, name_contact_center) values ($1,$2,$3)"
            record: Record = await connection.fetchrow(sql_ex, int(id_Telegram), str(description_contact_center),
                                                       str(name_contact_center))
            logging.info(f"ADD contact_centers ({name_contact_center})")
            return record
    except(Exception, ErrorInAssignmentError) as error:
        logging.info(error)


# Удаления ключевого центра
async def delete_contact_center_button(name_contact_center):
    pool: Connection = db
    try:
        async with pool.acquire() as connection:
            # async with pool.transaction():
            sql_ex = "Delete from contact_centers where name_contact_center = $1"
            record: Record = await connection.fetchrow(sql_ex, str(name_contact_center))
            logging.info(f"DELETED contact_center ({name_contact_center})")
            return record
    except(Exception, ErrorInAssignmentError) as error:
        logging.info(error)


# обновление описания центра
async def update_contact_center_data(id_Telegram, description_contact_center, name_contact_center):
    pool: Connection = db
    try:
        async with pool.acquire() as connection:
            # async with pool.transaction():
            sql_ex = "Update contact_centers set id_Telegram = $1, description_contact_center = $2 Where name_contact_center = $3"
            record: Record = await connection.fetchrow(sql_ex, int(id_Telegram), str(description_contact_center),
                                                       str(name_contact_center))
            logging.info(f"UPDATED contact_center ({name_contact_center})")
            return record
    except(Exception, ErrorInAssignmentError) as error:
        logging.info(error)


# Описание определенного  центра
async def contact_center_description(id):
    pool: Connection = db
    try:
        async with pool.acquire() as connection:
            sql_select = "SELECT description_contact_center FROM contact_centers WHERE id = $1;"
            record: Record = await connection.fetchrow(sql_select, int(id))
            record = list(record)[0]
            return record
    except(Exception, ErrorInAssignmentError) as error:
        logging.info(error)


# Поиск название контакт центра по айди
async def search_contact_center_name(id):
    pool: Connection = db
    try:
        async with pool.acquire() as connection:
            sql_select = "SELECT name_contact_center FROM contact_centers WHERE id = $1;"
            record: Record = await connection.fetchval(sql_select, int(id))
            return record
    except(Exception, ErrorInAssignmentError) as error:
        logging.info(error)


async def description_contact_center_name(id):
    pool: Connection = db
    try:
        async with pool.acquire() as connection:
            sql_select = "SELECT description_contact_center FROM contact_centers WHERE id = $1;"
            record: Record = await connection.fetchval(sql_select, int(id))
            return record
    except(Exception, ErrorInAssignmentError) as error:
        logging.info(error)


# Все данные о контактах ключевых центров
async def select_data_contact_centers():
    pool: Connection = db
    try:
        async with pool.acquire() as connection:
            sql_select = "SELECT * FROM contact_centers ORDER BY id;"
            record: Record = await connection.fetch(sql_select)
            return record
    except(Exception, ErrorInAssignmentError) as error:
        logging.info(error)


async def main():
    # a = await select_data_contact_centers()
    # for i in a:
    #     print(i['id'])
    print(await search_contact_center_name(26))

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    run = loop.run_until_complete(main())
