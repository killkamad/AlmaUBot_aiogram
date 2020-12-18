import asyncio
from asyncpg import ErrorInAssignmentError, Connection, Record
from loader import db
import logging


async def create_table_users():
    pool: Connection = db
    try:
        async with pool.acquire() as connection:
            # async with pool.transaction():
            sql_ex = """
                CREATE TABLE if not exists users(
                idT INT NOT NULL primary key,
                username VARCHAR (32),
                firstname VARCHAR (256),
                lastname VARCHAR (256),
                role VARCHAR (20))
                """
            record: Record = await connection.execute(sql_ex)
            print('Table users created')
            return record
    except(Exception, ErrorInAssignmentError) as error:
        print(error)


async def create_table_schedule():
    pool: Connection = db
    try:
        async with pool.acquire() as connection:
            # async with pool.transaction():
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
        async with pool.acquire() as connection:
            # async with pool.transaction():
            sql_ex = """
                CREATE TABLE if not exists library_reg_requests(
                id  serial unique primary key,
                id_Telegram INT NOT NULL,
                full_name VARCHAR (200),
                phone VARCHAR (200),
                email VARCHAR (200),
                data_base VARCHAR (200),
                date_time TIMESTAMP)
                """
            record: Record = await pool.fetchval(sql_ex)
            print('Table lib_reg_requests created')
            return record
    except(Exception, ErrorInAssignmentError) as error:
        print(error)


async def create_table_almau_shop_products():
    pool: Connection = db
    try:
        async with pool.acquire() as connection:
            # async with pool.transaction():
            sql_ex = """
                CREATE TABLE if not exists almau_shop_products(
                id  serial unique primary key,
                id_Telegram INT NOT NULL,
                product_name VARCHAR (200),
                price INT,
                currency VARCHAR (100),
                img VARCHAR (300),
                url VARCHAR (300))
                """
            record: Record = await pool.fetchval(sql_ex)
            print('Table almau_shop_products created')
            return record
    except(Exception, ErrorInAssignmentError) as error:
        print(f'error in create_table_almau_shop_products - {error}')


# Создание таблицы академ кадендарь
async def create_table_academic_calendar():
    pool: Connection = db
    try:
        async with pool.acquire() as connection:
            sql_ex = """
                CREATE TABLE if not exists academic_calendar(
                id  serial unique primary key,
                id_Telegram INT NOT NULL,
                id_calendar VARCHAR (500),
                date_time TIMESTAMP)
                """
            record: Record = await pool.fetchval(sql_ex)
            print('Table academic_calendar created')
            return record
    except(Exception, ErrorInAssignmentError) as error:
        print(error)


# Поиск последнего академ календаря в базе
async def find_id_academic_calendar():
    pool: Connection = db
    try:
        sql_select = "SELECT id_calendar FROM academic_calendar ORDER BY id DESC LIMIT 1;"
        record: Record = await pool.fetchval(sql_select)
        return record
    except(Exception, ErrorInAssignmentError) as error:
        logging.info(error)


# Добавление данных академ календаря
async def add_academic_calendar_data(id_Telegram, id_calendar):
    pool: Connection = db
    try:
        async with pool.acquire() as connection:
            # async with pool.transaction():
            sql_ex = "Insert into academic_calendar(id_Telegram, id_calendar, date_time) values ($1,$2, now())"
            record: Record = await connection.fetchrow(sql_ex, int(id_Telegram), str(id_calendar))
            logging.info(f"ADD academic calendar")
            return record
    except(Exception, ErrorInAssignmentError) as error:
        logging.info(error)


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


# Almau Shop получение данных
async def almaushop_select_data():
    pool: Connection = db
    try:
        sql_select = "SELECT * FROM almau_shop_products"
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


# Для тестов
async def insert_data():
    pool: Connection = db
    try:
        async with pool.acquire() as connection:
            # async with pool.transaction():
            sql_select = "Insert into users(username, firstname, lastname, idt, date_time) values ('dedus1337', 'Иван', 'Иванов', 555455, to_timestamp(now(), 'dd-mm-yyyy hh24:mi:ss'));"
            await connection.execute(sql_select)
    except(Exception, ErrorInAssignmentError) as error:
        logging.info(error)


async def check_id(id):
    pool: Connection = db
    try:
        sql_ex = "SELECT idt FROM users WHERE idt=$1;"
        record: Record = await pool.fetchrow(sql_ex, int(id))
        return record[0]
    except(Exception, ErrorInAssignmentError) as error:
        pass


async def check_role(id, role):
    pool: Connection = db
    try:
        sql_ex = "SELECT role FROM users WHERE idt = $1 AND role = $2;"
        record: Record = await pool.fetchrow(sql_ex, int(id), role)
        return record[0]
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
            record: Record = await pool.fetchrow(sql_ex, username_n, first_name, last_name, id)
            logging.info(f"ADD user({id}) to DB")
            return record
    except(Exception, ErrorInAssignmentError) as error:
        logging.info(error)


async def add_schedule_data(id_Telegram, id_sched, name_sched):
    pool: Connection = db
    try:
        async with pool.acquire() as connection:
            # async with pool.transaction():
            sql_ex = "Insert into schedule(id_Telegram, id_sched, name_sched) values ($1,$2,$3)"
            record: Record = await pool.fetchrow(sql_ex, int(id_Telegram), str(id_sched), str(name_sched))
            logging.info(f"ADD schedule ({name_sched})")
            return record
    except(Exception, ErrorInAssignmentError) as error:
        logging.info(error)


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


async def add_almau_shop_data(id_Telegram, product_name, price, currency, img, url):
    pool: Connection = db
    try:
        async with pool.acquire() as connection:
            # async with pool.transaction():
            sql_ex = "Insert into almau_shop_products(id_telegram, product_name, price, currency, img, url) values ($1,$2,$3,$4,$5,$6)"
            record: Record = await connection.fetchrow(sql_ex, int(id_Telegram), str(product_name), int(price),
                                                       str(currency),
                                                       str(img), str(url))
            logging.info(f"ADD registration request for registration in library")
            return record
    except(Exception, ErrorInAssignmentError) as error:
        logging.info(error)


async def update_schedule_data(id_Telegram, id_sched, name_sched):
    pool: Connection = db
    try:
        async with pool.acquire() as connection:
            # async with pool.transaction():
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
        async with pool.acquire() as connection:
            # async with pool.transaction():
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
        async with pool.acquire() as connection:
            # async with pool.transaction():
            sql_ex = "DELETE FROM schedule;"
            record: Record = await connection.fetchrow(sql_ex)
            logging.info(f"All data deleted from ({table_name} table")
            return record
    except(Exception, ErrorInAssignmentError) as error:
        logging.info(error)


# Полная очистка таблицы almau_shop_products
async def clear_almaushop_table():
    pool: Connection = db
    try:
        async with pool.acquire() as connection:
            # async with pool.transaction():
            sql_ex = "DELETE FROM almau_shop_products;"
            record: Record = await connection.fetchrow(sql_ex)
            logging.info(f"All data deleted from almau_shop_products table")
            return record
    except(Exception, ErrorInAssignmentError) as error:
        logging.info(error)


# Создание таблиц в БД
async def set_up_tables():
    await create_table_users()
    await create_table_schedule()
    await create_table_lib_reg_requests()


async def main():
    # print(await add_almau_shop_data(525325, "dadadada", 4000, 'тг', 'https://static.tildacdn.com/tild3865-6336-4639-a332-653936323434/for_AlmaU_0709__.png', 'https://almaushop.kz/#!/tproduct/221510661-1605267838115'))
    # count_user = await select_users()
    # print(count_user)
    # for i in count_user:
    #     print(i)
    # print(await clear_schedule_table('schedule'))
    # print(await check_id('468899120'))
    # print(await find_schedule_id('после колледжа на 3 года'))
    # print(await check_role(468899120, 'admin'))
    # print(await select_users())
    # await add_data('ggg12g', 'bbbb', 'last31_name', 43111)
    # await create_table_lib_reg_requests()
    await create_table_academic_calendar()
    # print(await clear_almaushop_table())


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    run = loop.run_until_complete(main())
