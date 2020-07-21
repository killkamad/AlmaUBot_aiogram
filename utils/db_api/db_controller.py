import asyncio
import asyncpg
from asyncpg import ErrorInAssignmentError, Connection, Record
from loader import db
import logging


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
        # result = cursor.fetchall()[0][0]
        return record
    except(Exception, ErrorInAssignmentError) as error:
        logging.info(error)


async def insert_data():
    pool: Connection = db
    try:
        async with pool.acquire() as connection:
            async with connection.transaction():
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
        async with pool.acquire() as connection:
            async with connection.transaction():
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
        async with pool.acquire() as connection:
            async with connection.transaction():
                sql_ex = "Insert into schedule(id_Telegram, id_sched, name_sched) values ($1,$2,$3)"
                record: Record = await pool.fetchrow(sql_ex, int(id_Telegram), str(id_sched), str(name_sched))
                logging.info(f"ADD schedule ({name_sched})")
                return record
    except(Exception, ErrorInAssignmentError) as error:
        logging.info(error)


async def clear_schedule_table(table_name):
    pool: Connection = db
    try:
        async with pool.acquire() as connection:
            async with connection.transaction():
                sql_ex = "DELETE FROM schedule;"
                record: Record = await pool.fetchrow(sql_ex)
                logging.info(f"All data deleted from ({table_name} table")
                return record
    except(Exception, ErrorInAssignmentError) as error:
        logging.info(error)


async def main():
    # await insert_data()
    # count_user = await select_users()
    # print(count_user)
    # for i in count_user:
    #     print(i)
    print(await clear_schedule_table('schedule'))
    # print(await check_id('43111'))
    # print(await find_schedule_id('1 курс'))
    # print(await check_role(468899120, 'admin'))
    # await add_data('ggg12g', 'bbbb', 'last31_name', 43111)


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    run = loop.run_until_complete(main())
