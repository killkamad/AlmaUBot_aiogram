import asyncio
import asyncpg
from asyncpg import ErrorInAssignmentError, Connection, Record
from loader import db
import logging


async def create_table_users():
    pool: Connection = db
    try:
        # async with pool.acquire() as connection:
        async with pool.transaction():
            sql_ex = """
                CREATE TABLE if not exists users(
                id  serial unique primary key,
                username VARCHAR (32),
                firstname VARCHAR (256),
                lastname VARCHAR (256),
                idT INT NOT NULL,
                role VARCHAR (20))
                """
            record: Record = await pool.fetchval(sql_ex)
            print('Table users created')
            return record
    except(Exception, ErrorInAssignmentError) as error:
        print(error)


async def create_table_schedule():
    pool: Connection = db
    try:
        # async with pool.acquire() as connection:
        async with pool.transaction():
            sql_ex = """
                CREATE TABLE if not exists schedule(
                id  serial unique primary key,
                id_Telegram INT NOT NULL,
                id_sched VARCHAR (500),
                name_sched VARCHAR (200))
                """
            record: Record = await pool.fetchval(sql_ex)
            print('Table schedule created')
            return record
    except(Exception, ErrorInAssignmentError) as error:
        print(error)


async def create_table_lib_reg_requests():
    pool: Connection = db
    try:
        # async with pool.acquire() as connection:
        async with pool.transaction():
            sql_ex = """
                CREATE TABLE if not exists lib_reg_requests(
                id  serial unique primary key,
                id_Telegram INT NOT NULL,
                tg_message_id INT,
                full_name VARCHAR (200),
                phone VARCHAR (200),
                email VARCHAR (200),
                data_base VARCHAR (200))
                """
            record: Record = await pool.fetchval(sql_ex)
            print('Table lib_reg_requests created')
            return record
    except(Exception, ErrorInAssignmentError) as error:
        print(error)


async def select_users():
    pool: Connection = db
    try:
        sql_select = "SELECT idT FROM users;"
        record: Record = await pool.fetch(sql_select)
        list1 = []
        for i in record:
            list1.append(i[0])
        return list1
    except(Exception, ErrorInAssignmentError) as error:
        print(error)


async def count_users():
    pool: Connection = db
    try:
        sql_select = "SELECT count(*) FROM users;"
        record: Record = await pool.fetchval(sql_select)
        return record
    except(Exception, ErrorInAssignmentError) as error:
        logging.info(error)


async def aws_select_data_schedule():
    pool: Connection = db
    try:
        sql_select = "SELECT * FROM schedule ORDER BY id;"
        record: Record = await pool.fetch(sql_select)
        return record
    except(Exception, ErrorInAssignmentError) as error:
        logging.info(error)


async def find_schedule_id(name):
    pool: Connection = db
    try:
        sql_select = "SELECT id_sched FROM schedule WHERE name_sched = $1;"
        record: Record = await pool.fetchrow(sql_select, name)
        record = list(record)[0]
        return record
    except(Exception, ErrorInAssignmentError) as error:
        logging.info(error)


async def insert_data():
    pool: Connection = db
    try:
        # async with pool.acquire() as connection:
        async with pool.transaction():
            sql_select = "Insert into users(username, firstname, lastname, idt) values ('cock111', 'big', 'bok', 1421423423);"
            record: Record = await pool.fetchval(sql_select)
        return record
    except(Exception, ErrorInAssignmentError) as error:
        logging.info(error)


async def check_id(id):
    pool: Connection = db
    try:
        sql_ex = "SELECT * FROM users WHERE idt=$1;"
        record: Record = await pool.fetch(sql_ex, int(id))
        record = list(record)[0][-2]
        return record
    except(Exception, ErrorInAssignmentError) as error:
        logging.info(error)


async def check_role(id, role):
    pool: Connection = db
    try:
        sql_ex = "SELECT * FROM users WHERE idt = $1 AND role = $2;"
        record: Record = await pool.fetchrow(sql_ex, int(id), role)
        record = list(record)[5]
        return record
    except(Exception, ErrorInAssignmentError) as error:
        logging.info(error)


async def add_data(username_n, first_name, last_name, id):
    pool: Connection = db
    try:
        # async with pool.acquire() as connection:
        async with pool.transaction():
            # cursor.execute("Insert into users('username', 'firstname', 'lastname', 'idT') values (%s, %s, %s, %s)", data)
            # cursor.execute("Insert into users('username', 'firstname', 'lastname', 'idt') values (%s, %s, %s, %s);", data) #Это для SQlite3
            sql_ex = "Insert into users (username, firstname, lastname, idt) values ($1,$2,$3,$4)"
            record: Record = await pool.fetchrow(sql_ex, username_n, first_name, last_name, id)
            logging.info(f"ADD user({username_n}) to DB")
            return record
    except(Exception, ErrorInAssignmentError) as error:
        logging.info(error)


async def add_schedule_data(id_Telegram, id_sched, name_sched):
    pool: Connection = db
    try:
        # async with pool.acquire() as connection:
        async with pool.transaction():
            sql_ex = "Insert into schedule(id_Telegram, id_sched, name_sched) values ($1,$2,$3)"
            record: Record = await pool.fetchrow(sql_ex, int(id_Telegram), str(id_sched), str(name_sched))
            logging.info(f"ADD schedule ({name_sched})")
            return record
    except(Exception, ErrorInAssignmentError) as error:
        logging.info(error)


async def add_lib_reg_request_data(id_Telegram, tg_message_id, full_name, phone, email, data_base):
    pool: Connection = db
    try:
        # async with pool.acquire() as connection:
        async with pool.transaction():
            sql_ex = "Insert into lib_reg_requests(id_Telegram, tg_message_id, full_name, phone, email, data_base) values ($1,$2,$3,$4,$5,$6)"
            record: Record = await pool.fetchrow(sql_ex, int(id_Telegram), int(tg_message_id), str(full_name), str(phone), str(email), str(data_base))
            logging.info(f"ADD reg_request_data")
            return record
    except(Exception, ErrorInAssignmentError) as error:
        logging.info(error)


async def update_schedule_data(id_Telegram, id_sched, name_sched):
    pool: Connection = db
    try:
        # async with pool.acquire() as connection:
        async with pool.transaction():
            sql_ex = "Update schedule set id_Telegram = $1, id_sched = $2 Where name_sched = $3"
            record: Record = await pool.fetchrow(sql_ex, int(id_Telegram), str(id_sched), str(name_sched))
            logging.info(f"UPDATED schedule ({name_sched})")
            return record
    except(Exception, ErrorInAssignmentError) as error:
        logging.info(error)


# Удлаение кнопки расписания
async def delete_schedule_button(name_sched):
    pool: Connection = db
    try:
        # async with pool.acquire() as connection:
        async with pool.transaction():
            sql_ex = "Delete from schedule where name_sched = $1"
            record: Record = await pool.fetchrow(sql_ex, str(name_sched))
            logging.info(f"DELETED schedule ({name_sched})")
            return record
    except(Exception, ErrorInAssignmentError) as error:
        logging.info(error)


# Полная очистка таблицы с расписанием
async def clear_schedule_table(table_name):
    pool: Connection = db
    try:
        # async with pool.acquire() as connection:
        async with pool.transaction():
            sql_ex = "DELETE FROM schedule;"
            record: Record = await pool.fetchrow(sql_ex)
            logging.info(f"All data deleted from ({table_name} table")
            return record
    except(Exception, ErrorInAssignmentError) as error:
        logging.info(error)


# Создание нужный таблиц в БД
async def set_up_tables():
    await create_table_users()
    await create_table_schedule()
    await create_table_lib_reg_requests()


async def main():
    # await insert_data()
    # count_user = await select_users()
    # print(count_user)
    # for i in count_user:
    #     print(i)
    # print(await clear_schedule_table('schedule'))
    # print(await check_id('43111'))
    # print(await find_schedule_id('после колледжа на 3 года'))
    # print(await check_role(468899120, 'admin'))
    # await add_data('ggg12g', 'bbbb', 'last31_name', 43111)
    await create_table_lib_reg_requests()


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    run = loop.run_until_complete(main())
