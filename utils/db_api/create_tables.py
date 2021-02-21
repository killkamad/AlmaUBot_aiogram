import asyncio
from asyncpg import ErrorInAssignmentError, Connection, Record
from loader import db
import logging


# Создание таблицы пользователей
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
                phone VARCHAR (200),
                role VARCHAR (20))
                """
            record: Record = await connection.execute(sql_ex)
            print('Table users successfully created')
            return record
    except(Exception, ErrorInAssignmentError) as error:
        print(error)


# Создание таблицы для расписанием
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
            # record: Record = await pool.fetchval(sql_ex)
            record: Record = await connection.fetchval(sql_ex)
            print('Table schedule successfully created')
            return record
    except(Exception, ErrorInAssignmentError) as error:
        print(error)


# Создание таблицы для регистрации на лицензионные базы данных (БИБЛИОТЕКА)
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
            # record: Record = await pool.fetchval(sql_ex)
            record: Record = await connection.fetchval(sql_ex)
            print('Table lib_reg_requests successfully created')
            return record
    except(Exception, ErrorInAssignmentError) as error:
        print(error)


# Создание таблицы для обращения к ректору
async def create_table_message_to_rector():
    pool: Connection = db
    try:
        async with pool.acquire() as connection:
            # async with pool.transaction():
            sql_ex = """
                CREATE TABLE if not exists message_to_rector(
                id  serial unique primary key,
                id_Telegram INT NOT NULL,
                full_name VARCHAR (200),
                phone VARCHAR (200),
                email VARCHAR (200),
                message_content VARCHAR (990),
                date_time TIMESTAMP)
                """
            record: Record = await connection.fetchval(sql_ex)
            print('Table message_to_rector successfully created')
            return record
    except(Exception, ErrorInAssignmentError) as error:
        print(error)


# Создание таблицы с мерчом для almaushop
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
            record: Record = await connection.fetchval(sql_ex)
            print('Table almau_shop_products successfully created')
            return record
    except(Exception, ErrorInAssignmentError) as error:
        print(f'error in create_table_almau_shop_products - {error}')


# Создание таблицы с книгами для almaushop
async def create_table_almau_shop_books():
    pool: Connection = db
    try:
        async with pool.acquire() as connection:
            # async with pool.transaction():
            sql_ex = """
                CREATE TABLE if not exists almau_shop_books(
                id  serial unique primary key,
                id_Telegram INT NOT NULL,
                book_name VARCHAR (200),
                book_author VARCHAR (200),
                price INT,
                currency VARCHAR (100),
                img VARCHAR (300),
                url VARCHAR (300))
                """
            record: Record = await connection.fetchval(sql_ex)
            print('Table almau_shop_books successfully created')
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
            record: Record = await connection.fetchval(sql_ex)
            print('Table academic_calendar successfully created')
            return record
    except(Exception, ErrorInAssignmentError) as error:
        print(error)


# Создание таблицы FAQ для AlmaU Shop
async def create_table_almau_shop_faq():
    pool: Connection = db
    try:
        async with pool.acquire() as connection:
            sql_ex = """
                CREATE TABLE if not exists almau_shop_faq(
                id  serial unique primary key,
                id_Telegram INT NOT NULL,
                question VARCHAR (300),
                answer VARCHAR (4000),
                date_time TIMESTAMP)
                """
            record: Record = await connection.fetchval(sql_ex)
            print('Table almau_shop_faq successfully created')
            return record
    except(Exception, ErrorInAssignmentError) as error:
        print(error)


# Создание таблицы для ключевых центров (Навигация)
async def create_table_contact_centers():
    pool: Connection = db
    try:
        async with pool.acquire() as connection:
            sql_ex = """
                CREATE TABLE if not exists contact_centers(
                id  serial unique primary key,
                id_Telegram INT NOT NULL,
                description_contact_center VARCHAR (990),
                name_contact_center VARCHAR (200))
                """
            record: Record = await connection.fetchval(sql_ex)
            print('Table contact_centers successfully created')
            return record
    except(Exception, ErrorInAssignmentError) as error:
        print(error)


# Создание таблицы для кнопок меню AlmaU Shop
async def create_table_almau_shop_menu_buttons():
    pool: Connection = db
    try:
        async with pool.acquire() as connection:
            sql_ex = """
                CREATE TABLE if not exists almau_shop_menu_buttons(
                id  serial unique primary key,
                id_Telegram INT NOT NULL,
                button_name VARCHAR (300),
                button_content VARCHAR (4000),
                date_time TIMESTAMP)
                """
            record: Record = await connection.fetchval(sql_ex)
            print('Table almau_shop_menu_buttons successfully created')
            return record
    except(Exception, ErrorInAssignmentError) as error:
        print(error)


# Создание таблицы для FAQ в главном меню
async def create_table_main_faq():
    pool: Connection = db
    try:
        async with pool.acquire() as connection:
            sql_ex = """
                    CREATE TABLE if not exists main_faq(
                    id  serial unique primary key,
                    id_Telegram INT NOT NULL,
                    question VARCHAR (300),
                    answer VARCHAR (4000),
                    date_time TIMESTAMP)
                    """
            record: Record = await connection.fetchval(sql_ex)
            print('Table main_faq successfully created')
            return record
    except(Exception, ErrorInAssignmentError) as error:
        print(error)


# Создание таблицы для профессорско-преподавательского состава
async def create_table_pps():
    pool: Connection = db
    try:
        async with pool.acquire() as connection:
            # async with pool.transaction():
            sql_ex = """
                CREATE TABLE if not exists tutors_and_employees(
                id  serial unique primary key,
                id_Telegram INT NOT NULL,
                shcool VARCHAR (200),
                position VARCHAR (200),
                description VARCHAR (990),
                date_time TIMESTAMP)
                """
            # record: Record = await pool.fetchval(sql_ex)
            record: Record = await connection.fetchval(sql_ex)
            print('Table tutors_and_employees successfully created')
            return record
    except(Exception, ErrorInAssignmentError) as error:
        print(error)


# Создание таблицы для справок
async def create_table_certificate():
    pool: Connection = db
    try:
        async with pool.acquire() as connection:
            # async with pool.transaction():
            sql_ex = """
                CREATE TABLE if not exists certificate(
                id  serial unique primary key,
                id_Telegram INT NOT NULL,
                id_request INT NOT NULL,
                id_certif VARCHAR (500),
                name_certif VARCHAR (200),
                FOREIGN KEY (id_request) REFERENCES request_certificate (id))
                """
            # record: Record = await pool.fetchval(sql_ex)
            record: Record = await connection.fetchval(sql_ex)
            print('Table certificate successfully created')
            return record
    except(Exception, ErrorInAssignmentError) as error:
        print(error)


async def create_table_request_certificate():
    pool: Connection = db
    try:
        async with pool.acquire() as connection:
            # async with pool.transaction():
            sql_ex = """
                CREATE TABLE if not exists request_certificate(
                id  serial unique primary key,
                id_Telegram INT NOT NULL,
                full_name VARCHAR (200),
                phone VARCHAR (200),
                email VARCHAR (200),
                certif_type VARCHAR (200),
                date_time TIMESTAMP)
                """
            record: Record = await pool.fetchval(sql_ex)
            print('Table request_certificate successfully created')
            return record
    except(Exception, ErrorInAssignmentError) as error:
        print(error)


# Создание таблицы для карты навигации
async def create_table_map_navigation():
    pool: Connection = db
    try:
        async with pool.acquire() as connection:
            # async with pool.transaction():
            sql_ex = """
                CREATE TABLE if not exists map_navigation(
                id  serial unique primary key,
                id_Telegram INT NOT NULL,
                building VARCHAR (200),
                floor VARCHAR (200),
                cabinet VARCHAR (200),
                cabinet_description VARCHAR (990),
                date_time TIMESTAMP)
                """
            # record: Record = await pool.fetchval(sql_ex)
            record: Record = await connection.fetchval(sql_ex)
            print('Table map_navigation successfully created')
            return record
    except(Exception, ErrorInAssignmentError) as error:
        print(error)


# async def create_table_test():
#     pool: Connection = db
#     try:
#         async with pool.acquire() as connection:
#             # async with pool.transaction():
#             sql_ex = """
#                 AlTER TABLE certificate ADD date_time TIMESTAMP
#                 """
#             record: Record = await pool.fetchval(sql_ex)
#             print('Table request_certificate successfully created')
#             return record
#     except(Exception, ErrorInAssignmentError) as error:
#         print(error)


# Создание таблиц в БД
async def set_up_tables():
    try:
        await create_table_users()
        await create_table_schedule()
        await create_table_lib_reg_requests()
        await create_table_message_to_rector()
        await create_table_academic_calendar()
        await create_table_almau_shop_products()
        await create_table_almau_shop_books()
        await create_table_almau_shop_faq()
        await create_table_almau_shop_menu_buttons()
        await create_table_main_faq()
        await create_table_pps()
        await create_table_certificate()
        await create_table_request_certificate()
        await create_table_map_navigation()
    except Exception as error:
        print(f'Error - {error}')


async def main():
    # count_user = await select_users()
    # print(count_user)
    # for i in count_user:
    #     print(i)
    await set_up_tables()
    # await create_table_test()


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    run = loop.run_until_complete(main())
