import asyncio
from asyncpg import ErrorInAssignmentError, Connection, Record
from loader import db
import logging


async def add_certificate_request_data(id_Telegram, full_name, phone, email, certif_type, comment):
    pool: Connection = db
    try:
        async with pool.acquire() as connection:
            # async with pool.transaction():
            sql_ex = "Insert into certificate(id_Telegram, full_name, phone, email, certif_type, comment, date_time) values ($1,$2,$3,$4,$5,$6, now())"
            record: Record = await connection.fetchrow(sql_ex, int(id_Telegram), str(full_name), str(phone), str(email),
                                                       str(certif_type), str(comment))
            logging.info(f"ADD request for certificate")
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


async def add_instruction_document(button_id, button_file):
    pool: Connection = db
    try:
        async with pool.acquire() as connection:
            sql_ex = "Update certificate_menu_buttons set button_file = $2, date_time = now() Where id = $1"
            record: Record = await connection.fetchrow(sql_ex, int(button_id), str(button_file))
            return record
    except(Exception, ErrorInAssignmentError) as error:
        logging.info(error)


async def add_instruction_with_document(id_Telegram, button_name, button_content, button_file):
    pool: Connection = db
    try:
        async with pool.acquire() as connection:
            sql_ex = "Insert into certificate_menu_buttons(id_Telegram, button_name, button_content, button_file, date_time) values ($1,$2,$3,$4, now())"
            record: Record = await connection.fetchrow(sql_ex, int(id_Telegram), str(button_name), str(button_content),
                                                       str(button_file))
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
            sql_select = "SELECT button_content, button_file FROM certificate_menu_buttons WHERE id = $1"
            record: Record = await connection.fetchrow(sql_select, int(id))
            return record
    except(Exception, ErrorInAssignmentError) as error:
        logging.info(error)


async def select_instruction_all(id):
    pool: Connection = db
    try:
        async with pool.acquire() as connection:
            sql_select = "SELECT * FROM certificate_menu_buttons WHERE id = $1"
            record: Record = await connection.fetchrow(sql_select, int(id))
            return record
    except(Exception, ErrorInAssignmentError) as error:
        logging.info(error)


async def select_instruction_without_file():
    pool: Connection = db
    try:
        async with pool.acquire() as connection:
            sql_select = "SELECT id, button_name, button_content FROM certificate_menu_buttons WHERE button_file is null"
            record: Record = await connection.fetch(sql_select)
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
            # logging.info(f"UPDATED button ({id_request})")
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
    print(await select_instruction_without_file())


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    run = loop.run_until_complete(main())
