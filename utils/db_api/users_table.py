import asyncio
from asyncpg import ErrorInAssignmentError, Connection, Record
from loader import db
import logging


async def select_users():
    pool: Connection = db
    try:
        async with pool.acquire() as connection:
            sql_select = "SELECT idT FROM users;"
            record: Record = await connection.fetch(sql_select)
            list1 = []
            for i in record:
                list1.append(i[0])
            return list1
    except(Exception, ErrorInAssignmentError) as error:
        print(error)


async def count_users():
    pool: Connection = db
    try:
        async with pool.acquire() as connection:
            sql_select = "SELECT count(*) FROM users;"
            record: Record = await connection.fetchval(sql_select)
            return record
    except(Exception, ErrorInAssignmentError) as error:
        logging.info(error)


# Проверка, есть ли такой номер в БД
async def check_phone_in_users(phone):
    pool: Connection = db
    try:
        async with pool.acquire() as connection:
            sql_select = "SELECT * FROM users WHERE phone = $1;"
            record: Record = await connection.fetchrow(sql_select, str(phone))
            return record
    except(Exception, ErrorInAssignmentError) as error:
        logging.info(error)


# Поиск роли по номеру телефона
async def check_role_for_admin(phone):
    pool: Connection = db
    try:
        async with pool.acquire() as connection:
            sql_ex = "SELECT role FROM users WHERE phone = $1;"
            record: Record = await connection.fetchrow(sql_ex, str(phone))
            return record[0]
    except(Exception, ErrorInAssignmentError) as error:
        logging.info(error)


# Поиск роли по номеру телефона
async def select_last_ten_users():
    pool: Connection = db
    try:
        async with pool.acquire() as connection:
            sql_ex = "SELECT idt FROM users WHERE date_time IS NOT NULL ORDER BY date_time DESC;"
            record = await connection.fetch(sql_ex)
            return record
    except(Exception, ErrorInAssignmentError) as error:
        logging.info(error)


# Поиск роли по номеру телефона
async def find_user_by_telegram_id(idt):
    pool: Connection = db
    try:
        async with pool.acquire() as connection:
            sql_ex = "SELECT idt, username, firstname, lastname, role, phone, date_time FROM users WHERE idt=$1;"
            record = await connection.fetchrow(sql_ex, int(idt))
            return record
    except(Exception, ErrorInAssignmentError) as error:
        logging.info(error)


async def check_id(id):
    pool: Connection = db
    try:
        async with pool.acquire() as connection:
            sql_ex = "SELECT idt FROM users WHERE idt=$1;"
            record: Record = await connection.fetchrow(sql_ex, int(id))
            return record[0]
    except(Exception, ErrorInAssignmentError) as error:
        pass


# async def check_role(id, role):
#     pool: Connection = db
#     try:
#         async with pool.acquire() as connection:
#             sql_ex = "SELECT role FROM users WHERE idt = $1 AND role = $2;"
#             record: Record = await connection.fetchrow(sql_ex, int(id), role)
#             return record[0]
#     except(Exception, ErrorInAssignmentError) as error:
#         logging.info(error)


async def check_role_by_id(id):
    pool: Connection = db
    try:
        async with pool.acquire() as connection:
            sql_ex = "SELECT role FROM users WHERE idt = $1;"
            record: Record = await connection.fetchval(sql_ex, int(id))
            return record
    except(Exception, ErrorInAssignmentError) as error:
        logging.info(error)


async def add_data(username_n, first_name, last_name, id):
    pool: Connection = db
    try:
        async with pool.acquire() as connection:
            # async with pool.transaction():
            # cursor.execute("Insert into users('username', 'firstname', 'lastname', 'idT') values (%s, %s, %s, %s)", data)
            # cursor.execute("Insert into users('username', 'firstname', 'lastname', 'idt') values (%s, %s, %s, %s);", data) #Это для SQlite3
            sql_ex = "Insert into users (username, firstname, lastname, idt, date_time) values ($1,$2,$3,$4,now())"
            record: Record = await connection.fetchrow(sql_ex, username_n, first_name, last_name, id)
            logging.info(f"ADD user({id}) to DB")
            return record
    except(Exception, ErrorInAssignmentError) as error:
        logging.info(error)


async def register_user_phone(id_telegram, phone):
    pool: Connection = db
    try:
        async with pool.acquire() as connection:
            # async with pool.transaction():
            sql_ex = "UPDATE users set phone = $1 WHERE idt = $2"
            record: Record = await connection.fetchrow(sql_ex, str(phone), int(id_telegram))
            logging.info(f"Registered phone for {id_telegram}")
            return record
    except(Exception, ErrorInAssignmentError) as error:
        logging.info(error)


# Изменение роль пользователя
async def edit_user_role(role, phone):
    pool: Connection = db
    try:
        async with pool.acquire() as connection:
            # async with pool.transaction():
            sql_ex = "UPDATE users set role = $1 WHERE phone = $2"
            record: Record = await connection.fetchrow(sql_ex, str(role), str(phone))
            logging.info(f"EDITED role for phone {phone}")
            return record
    except(Exception, ErrorInAssignmentError) as error:
        logging.info(error)


async def main():
    print(await select_users())
    print(await check_role_by_id(468899120))


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    run = loop.run_until_complete(main())
