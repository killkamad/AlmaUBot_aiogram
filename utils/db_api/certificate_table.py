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
                         crt.name_certif,
                         crt.is_loaded,
                         crt.date_time
                    FROM certificate crt
                    JOIN request_certificate req
                      ON crt.id_request = req.id
                    JOIN users usr
                      ON req.id_telegram = usr.idt
                   WHERE usr.idt = $1 AND crt.is_loaded
                   """
            record: Record = await connection.fetch(sql_select, user_id)
            return record
    except(Exception, ErrorInAssignmentError) as error:
        logging.info(error)


async def find_certificate_id(id_req):
    pool: Connection = db
    try:
        async with pool.acquire() as connection:
            sql_select = "SELECT id_certif FROM certificate WHERE id_request = $1;"
            record: Record = await connection.fetchrow(sql_select, int(id_req))
            record = list(record)[0]
            return record
    except(Exception, ErrorInAssignmentError) as error:
        logging.info(error)


async def find_certificate_name(id_req):
    pool: Connection = db
    try:
        async with pool.acquire() as connection:
            sql_select = "SELECT name_certif FROM certificate WHERE id_request = $1;"
            record: Record = await connection.fetchrow(sql_select, int(id_req))
            record = list(record)[0]
            return record
    except(Exception, ErrorInAssignmentError) as error:
        logging.info(error)


async def add_certificate_data(id_Telegram, id_request, id_certif, name_certif, is_loaded):
    pool: Connection = db
    try:
        async with pool.acquire() as connection:
            sql_ex = "Insert into certificate(id_Telegram, id_request ,id_certif, name_certif, date_time, is_loaded) values ($1,$2,$3,$4, now(),$5)"
            record: Record = await connection.fetchrow(sql_ex, int(id_Telegram), int(id_request), str(id_certif),
                                                       str(name_certif), bool(is_loaded))
            logging.info(f"ADD certificate ({name_certif})")
            return record
    except(Exception, ErrorInAssignmentError) as error:
        logging.info(error)


async def update_certificate_data(id_Telegram, id_request, id_certif, id_req):
    pool: Connection = db
    try:
        async with pool.acquire() as connection:
            sql_ex = "Update certificate set id_Telegram = $1, id_request = $2, id_certif = $3 Where id_request = $4"
            record: Record = await connection.fetchrow(sql_ex, int(id_Telegram), int(id_request), str(id_certif),
                                                       int(id_req))
            logging.info(f"UPDATED certificate ({id_req})")
            return record
    except(Exception, ErrorInAssignmentError) as error:
        logging.info(error)


async def delete_certificate_button(id_req):
    pool: Connection = db
    try:
        async with pool.acquire() as connection:
            sql_ex = "Delete from certificate where id_request = $1"
            record: Record = await connection.fetchrow(sql_ex, int(id_req))
            logging.info(f"DELETED certificate ({id_req})")
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
            sql_ex = "Insert into request_certificate(id_Telegram, full_name, phone, email, certif_type, date_time) values ($1,$2,$3,$4,$5, now())"
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
            sql_select = "SELECT DISTINCT ON (phone) * FROM request_certificate ORDER BY phone, date_time DESC;"
            record: Record = await connection.fetch(sql_select)
            return record
    except(Exception, ErrorInAssignmentError) as error:
        logging.info(error)


async def select_data_on_send_request_certificate():
    pool: Connection = db
    try:
        async with pool.acquire() as connection:
            sql_select = "SELECT DISTINCT ON (phone) * FROM request_certificate WHERE is_loaded IS FALSE;"
            record: Record = await connection.fetch(sql_select)
            return record
    except(Exception, ErrorInAssignmentError) as error:
        logging.info(error)


async def select_data_on_edit_request_certificate():
    pool: Connection = db
    try:
        async with pool.acquire() as connection:
            sql_select = """
                          SELECT DISTINCT ON (req.phone)
                        	     req.id,
                        	     req.id_telegram,
                        	     req.full_name,
                        	     req.phone,
                        	     req.email,
                        	     req.certif_type,
                        	     req.is_loaded,
                        	     req.date_time
                            FROM request_certificate req
                            JOIN certificate crt
                              ON req.id = crt.id_request
                            WHERE req.is_loaded IS TRUE
                            ORDER BY req.phone, req.date_time DESC;"""
            record: Record = await connection.fetch(sql_select)
            return record
    except(Exception, ErrorInAssignmentError) as error:
        logging.info(error)


async def select_data_certificate_type(user_id):
    pool: Connection = db
    try:
        async with pool.acquire() as connection:
            sql_select = """
                  SELECT DISTINCT ON (req.certif_type)
                		 req.id,
                		 req.id_telegram,
                		 req.full_name,
                		 req.phone,
                		 req.email,
                		 req.certif_type,
                		 req.date_time,
                         req.is_loaded
                	FROM request_certificate req
                	JOIN users usr
                	  ON req.id_telegram = usr.idt
                   WHERE usr.idt = $1 AND req.is_loaded IS NOT TRUE;
                   """
            record: Record = await connection.fetch(sql_select, user_id)
            return record
    except(Exception, ErrorInAssignmentError) as error:
        logging.info(error)


async def mark_as_loaded_request(id, is_loaded):
    pool: Connection = db
    try:
        async with pool.acquire() as connection:
            # async with pool.transaction():
            sql_ex = """
                UPDATE request_certificate SET is_loaded = $2 WHERE id = $1;
                """
            # record: Record = await pool.fetchval(sql_ex)
            record: Record = await connection.fetchrow(sql_ex, int(id), bool(is_loaded))
            logging.info('UPDATED request_certificate, function - mark_as_loaded_request')
            return record
    except(Exception, ErrorInAssignmentError) as error:
        print(error)


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


async def alter_table_certificate():
    pool: Connection = db
    try:
        async with pool.acquire() as connection:
            # async with pool.transaction():
            sql_ex = """
                ALTER TABLE certificate ALTER COLUMN is_loaded BOOLEAN SET DEFAULT FALSE
                """
            # record: Record = await pool.fetchval(sql_ex)
            record: Record = await connection.fetchval(sql_ex)
            print('Table certificate successfully created')
            return record
    except(Exception, ErrorInAssignmentError) as error:
        print(error)


async def main():
    await alter_table_certificate()


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    run = loop.run_until_complete(main())
