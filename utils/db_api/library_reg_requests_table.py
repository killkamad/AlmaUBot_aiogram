import asyncio
from asyncpg import ErrorInAssignmentError, Connection, Record
from loader import db
import logging


async def add_lib_reg_request_data(id_Telegram, full_name, phone, email, data_base):
    pool: Connection = db
    try:
        async with pool.acquire() as connection:
            # async with pool.transaction():
            sql_ex = "Insert into library_reg_requests(id_Telegram, full_name, phone, email, data_base, date_time) values ($1,$2,$3,$4,$5, now())"
            record: Record = await connection.fetchrow(sql_ex, int(id_Telegram), str(full_name), str(phone), str(email),
                                                       str(data_base))
            logging.info(f"ADD registration request for registration in library")
            return record
    except(Exception, ErrorInAssignmentError) as error:
        logging.info(error)


# async def main():
#     print(await select_data_contact_centers())
#
#
# if __name__ == '__main__':
#     loop = asyncio.get_event_loop()
#     run = loop.run_until_complete(main())
