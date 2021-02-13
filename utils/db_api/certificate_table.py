import asyncio
from asyncpg import ErrorInAssignmentError, Connection, Record
from loader import db
import logging


# Данные об индивидуальных справках студентов
async def select_data_certificate(user_id):
    pool: Connection = db
    try:
        async with pool.acquire() as connection:
            sql_select = """
                  SELECT
                         crt.id,
                         crt.id_telegram,
                         crt.id_request,
                         crt.id_certif,
                         crt.name_certif
                    FROM certificate crt
                    JOIN request_certificate req
                      ON crt.id_request = req.id
                    JOIN users usr
                      ON req.id_telegram = usr.idt
                   WHERE usr.idt = $1
                   """
            record: Record = await connection.fetch(sql_select, user_id)
            return record
    except(Exception, ErrorInAssignmentError) as error:
        logging.info(error)


async def find_certificate_id(name):
    pool: Connection = db
    try:
        async with pool.acquire() as connection:
            sql_select = "SELECT id_certif FROM certificate WHERE name_certif = $1;"
            record: Record = await connection.fetchrow(sql_select, name)
            record = list(record)[0]
            return record
    except(Exception, ErrorInAssignmentError) as error:
        logging.info(error)


async def find_certificate_name(name):
    pool: Connection = db
    try:
        async with pool.acquire() as connection:
            sql_select = "SELECT name_certif FROM certificate WHERE name_certif = $1;"
            record: Record = await connection.fetchrow(sql_select, name)
            record = list(record)[0]
            return record
    except(Exception, ErrorInAssignmentError) as error:
        logging.info(error)


async def add_certificate_data(id_Telegram, id_request, id_certif, name_certif):
    pool: Connection = db
    try:
        async with pool.acquire() as connection:
            sql_ex = "Insert into certificate(id_Telegram, id_request ,id_certif, name_certif) values ($1,$2,$3,$4)"
            record: Record = await connection.fetchrow(sql_ex, int(id_Telegram), int(id_request), str(id_certif),
                                                       str(name_certif))
            logging.info(f"ADD certificate ({name_certif})")
            return record
    except(Exception, ErrorInAssignmentError) as error:
        logging.info(error)


async def update_certificate_data(id_Telegram, id_request, id_certif, name_certif):
    pool: Connection = db
    try:
        async with pool.acquire() as connection:
            sql_ex = "Update certificate set id_Telegram = $1, id_request = $2, id_certif = $3 Where name_certif = $4"
            record: Record = await connection.fetchrow(sql_ex, int(id_Telegram), int(id_request), str(id_certif),
                                                       str(name_certif))
            logging.info(f"UPDATED certificate ({name_certif})")
            return record
    except(Exception, ErrorInAssignmentError) as error:
        logging.info(error)


async def delete_certificate_button(name_certif):
    pool: Connection = db
    try:
        async with pool.acquire() as connection:
            sql_ex = "Delete from certificate where name_certif = $1"
            record: Record = await connection.fetchrow(sql_ex, str(name_certif))
            logging.info(f"DELETED certificate ({name_certif})")
            return record
    except(Exception, ErrorInAssignmentError) as error:
        logging.info(error)


async def clear_certificate_table(table_name):
    pool: Connection = db
    try:
        async with pool.acquire() as connection:
            # async with pool.transaction():
            sql_ex = "DELETE FROM certificate;"
            record: Record = await connection.fetchrow(sql_ex)
            logging.info(f"All data deleted from ({table_name} table")
            return record
    except(Exception, ErrorInAssignmentError) as error:
        logging.info(error)


async def add_certificate_request_data(id_Telegram, full_name, phone, email, certif_type):
    pool: Connection = db
    try:
        async with pool.acquire() as connection:
            # async with pool.transaction():
            sql_ex = "Insert into request_certificate(id_Telegram, full_name, phone, email, certif_type) values ($1,$2,$3,$4,$5)"
            record: Record = await connection.fetchrow(sql_ex, int(id_Telegram), str(full_name), str(phone), str(email),
                                                       str(certif_type))
            logging.info(f"ADD request for certificate")
            return record
    except(Exception, ErrorInAssignmentError) as error:
        logging.info(error)


async def select_data_request_certificate():
    pool: Connection = db
    try:
        async with pool.acquire() as connection:
            sql_select = "SELECT * FROM request_certificate ORDER BY id;"
            record: Record = await connection.fetch(sql_select)
            return record
    except(Exception, ErrorInAssignmentError) as error:
        logging.info(error)


async def find_request_id(name):
    pool: Connection = db
    try:
        async with pool.acquire() as connection:
            sql_select = "SELECT id FROM request_certificate WHERE full_name = $1;"
            record: Record = await connection.fetchrow(sql_select, name)
            record = list(record)[0]
            return record
    except(Exception, ErrorInAssignmentError) as error:
        logging.info(error)


async def find_request_id_telegram(name):
    pool: Connection = db
    try:
        async with pool.acquire() as connection:
            sql_select = "SELECT id_telegram FROM request_certificate WHERE full_name = $1;"
            record: Record = await connection.fetchrow(sql_select, name)
            record = list(record)[0]
            return record
    except(Exception, ErrorInAssignmentError) as error:
        logging.info(error)


async def find_request_full_name(name):
    pool: Connection = db
    try:
        async with pool.acquire() as connection:
            sql_select = "SELECT full_name FROM request_certificate WHERE full_name = $1;"
            record: Record = await connection.fetchrow(sql_select, name)
            record = list(record)[0]
            return record
    except(Exception, ErrorInAssignmentError) as error:
        logging.info(error)


async def main():
    print(await find_request_full_name('Маштаков Кирилл Юрьевич'))


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    run = loop.run_until_complete(main())
