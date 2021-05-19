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
                  SELECT crt.*
                    FROM certificate crt
                    JOIN users usr
                      ON crt.id_telegram = usr.idt
                   WHERE usr.idt = $1 AND crt.is_loaded
                   """
            record: Record = await connection.fetch(sql_select, user_id)
            return record
    except(Exception, ErrorInAssignmentError) as error:
        logging.info(error)


async def find_certificate_id(id_request):
    pool: Connection = db
    try:
        async with pool.acquire() as connection:
            sql_select = "SELECT id_certif FROM certificate WHERE id = $1;"
            record: Record = await connection.fetchrow(sql_select, int(id_request))
            record = list(record)[0]
            return record
    except(Exception, ErrorInAssignmentError) as error:
        logging.info(error)


async def find_certificate_name(id_request):
    pool: Connection = db
    try:
        async with pool.acquire() as connection:
            sql_select = "SELECT certif_type FROM certificate WHERE id = $1;"
            record: Record = await connection.fetchrow(sql_select, int(id_request))
            record = list(record)[0]
            return record
    except(Exception, ErrorInAssignmentError) as error:
        logging.info(error)


async def add_certificate_data(id_request, id_certif, is_loaded):
    pool: Connection = db
    try:
        async with pool.acquire() as connection:
            sql_ex = "Update certificate set id_certif = $2, is_loaded = $3, date_time = now() Where id = $1"
            record: Record = await connection.fetchrow(sql_ex, int(id_request), str(id_certif), bool(is_loaded))
            logging.info(f"ADD certificate for request #({id_request})")
            return record
    except(Exception, ErrorInAssignmentError) as error:
        logging.info(error)


async def update_certificate_data(id_request, id_certif):
    pool: Connection = db
    try:
        async with pool.acquire() as connection:
            sql_ex = "Update certificate set id_certif = $2, date_time = now() Where id = $1"
            record: Record = await connection.fetchrow(sql_ex, int(id_request), str(id_certif))
            logging.info(f"UPDATED certificate ({id_request})")
            return record
    except(Exception, ErrorInAssignmentError) as error:
        logging.info(error)


async def delete_certificate_button(id_request):
    pool: Connection = db
    try:
        async with pool.acquire() as connection:
            sql_ex = "Delete from certificate where id = $1"
            record: Record = await connection.fetchrow(sql_ex, int(id_request))
            logging.info(f"DELETED certificate ({id_request})")
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
            sql_ex = "Insert into certificate(id_Telegram, full_name, phone, email, certif_type, date_time) values ($1,$2,$3,$4,$5, now())"
            record: Record = await connection.fetchrow(sql_ex, int(id_Telegram), str(full_name), str(phone), str(email),
                                                       str(certif_type))
            logging.info(f"ADD request for certificate")
            return record
    except(Exception, ErrorInAssignmentError) as error:
        logging.info(error)


async def select_data_on_send_request_certificate():
    pool: Connection = db
    try:
        async with pool.acquire() as connection:
            sql_select = "SELECT DISTINCT ON (phone) * FROM certificate WHERE id_certif IS NULL AND is_loaded IS NOT TRUE;"
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
                	     req.*
                    FROM certificate req
                   WHERE req.is_loaded IS TRUE
                   ORDER BY req.phone, req.date_time DESC;
                   """
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
                		 req.*
                	FROM certificate req
                	JOIN users usr
                	  ON req.id_telegram = usr.idt
                   WHERE usr.idt = $1 AND req.is_loaded IS NOT TRUE;
                   """
            record: Record = await connection.fetch(sql_select, user_id)
            return record
    except(Exception, ErrorInAssignmentError) as error:
        logging.info(error)


async def find_request_id_telegram(id):
    pool: Connection = db
    try:
        async with pool.acquire() as connection:
            sql_select = "SELECT id_telegram FROM certificate WHERE id = $1;"
            record: Record = await connection.fetchrow(sql_select, int(id))
            record = list(record)[0]
            return record
    except(Exception, ErrorInAssignmentError) as error:
        logging.info(error)


async def add_instruction(id_Telegram, button_name, button_content):
    pool: Connection = db
    try:
        async with pool.acquire() as connection:
            sql_ex = "Insert into certificate_menu_buttons(id_Telegram, button_name, button_content, date_time) values ($1,$2,$3, now())"
            record: Record = await connection.fetchrow(sql_ex, int(id_Telegram), str(button_name), str(button_content))
            logging.info(f"ADD instuction of ({button_name})")
            return record
    except(Exception, ErrorInAssignmentError) as error:
        logging.info(error)


async def select_data_instruction():
    pool: Connection = db
    try:
        async with pool.acquire() as connection:
            sql_select = "SELECT * FROM certificate_menu_buttons"
            record: Record = await connection.fetch(sql_select)
            return record
    except(Exception, ErrorInAssignmentError) as error:
        logging.info(error)


async def select_instruction(id):
    pool: Connection = db
    try:
        async with pool.acquire() as connection:
            sql_select = "SELECT button_content FROM certificate_menu_buttons WHERE id = $1"
            record: Record = await connection.fetchrow(sql_select, int(id))
            record = list(record)[0]
            return record
    except(Exception, ErrorInAssignmentError) as error:
        logging.info(error)


async def select_data_on_edit_instruction():
    pool: Connection = db
    try:
        async with pool.acquire() as connection:
            sql_select = "SELECT * FROM certificate_menu_buttons"
            record: Record = await connection.fetch(sql_select)
            return record
    except(Exception, ErrorInAssignmentError) as error:
        logging.info(error)


async def update_instruction_data(button_name, button_content):
    pool: Connection = db
    try:
        async with pool.acquire() as connection:
            sql_ex = "Update certificate_menu_buttons set button_content = $2, date_time = now() Where id = $1"
            record: Record = await connection.fetchrow(sql_ex, int(button_name), str(button_content))
            logging.info(f"UPDATED button ({id_request})")
            return record
    except(Exception, ErrorInAssignmentError) as error:
        logging.info(error)


async def delete_instruction_button(button_name):
    pool: Connection = db
    try:
        async with pool.acquire() as connection:
            sql_ex = "Delete from certificate_menu_buttons where id = $1"
            record: Record = await connection.fetchrow(sql_ex, int(button_name))
            logging.info(f"DELETED instruction ({button_name})")
            return record
    except(Exception, ErrorInAssignmentError) as error:
        logging.info(error)

async def main():
    await alter_table_certificate()


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    run = loop.run_until_complete(main())
