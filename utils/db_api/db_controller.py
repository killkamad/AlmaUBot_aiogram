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
            record: Record = await pool.fetchval(sql_ex)
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
            record: Record = await pool.fetchval(sql_ex)
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


# Поиск последнего академ календаря в базе
async def find_id_academic_calendar():
    pool: Connection = db
    try:
        async with pool.acquire() as connection:
            sql_select = "SELECT id_calendar FROM academic_calendar ORDER BY id DESC LIMIT 1;"
            record: Record = await connection.fetchval(sql_select)
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


async def aws_select_data_schedule():
    pool: Connection = db
    try:
        async with pool.acquire() as connection:
            sql_select = "SELECT * FROM schedule ORDER BY id;"
            record: Record = await connection.fetch(sql_select)
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


async def main_faq_select_question_and_answer(id):
    pool: Connection = db
    try:
        async with pool.acquire() as connection:
            sql_select = "SELECT question, answer FROM main_faq WHERE id = $1;"
            record: Record = await connection.fetchrow(sql_select, int(id))
            return record
    except(Exception, ErrorInAssignmentError) as error:
        logging.info(error)


# Almau Shop получение данных о мерче
async def almaushop_select_data():
    pool: Connection = db
    try:
        async with pool.acquire() as connection:
            sql_select = "SELECT * FROM almau_shop_products"
            record: Record = await connection.fetch(sql_select)
            return record
    except(Exception, ErrorInAssignmentError) as error:
        logging.info(error)


# Almau Shop получение данных о книгах
async def almaushop_select_books():
    pool: Connection = db
    try:
        async with pool.acquire() as connection:
            sql_select = "SELECT * FROM almau_shop_books"
            record: Record = await connection.fetch(sql_select)
            return record
    except(Exception, ErrorInAssignmentError) as error:
        logging.info(error)


# Almau Shop FAQ получение вопроса и ответа
async def almaushop_faq_select_data():
    pool: Connection = db
    try:
        async with pool.acquire() as connection:
            sql_select = "SELECT id, question, answer FROM almau_shop_faq ORDER BY id;"
            record: Record = await connection.fetch(sql_select)
            return record
    except(Exception, ErrorInAssignmentError) as error:
        logging.info(error)


# Главное менб FAQ получение вопроса и ответа
async def main_faq_select_data():
    pool: Connection = db
    try:
        async with pool.acquire() as connection:
            sql_select = "SELECT id, question, answer FROM main_faq ORDER BY id;"
            record: Record = await connection.fetch(sql_select)
            return record
    except(Exception, ErrorInAssignmentError) as error:
        logging.info(error)


async def almaushop_faq_find_answer(id):
    pool: Connection = db
    try:
        async with pool.acquire() as connection:
            sql_select = "SELECT answer FROM almau_shop_faq WHERE id = $1;"
            record: Record = await connection.fetchval(sql_select, int(id))
            return record
    except(Exception, ErrorInAssignmentError) as error:
        logging.info(error)


async def almaushop_faq_find_question(id):
    pool: Connection = db
    try:
        async with pool.acquire() as connection:
            sql_select = "SELECT question FROM almau_shop_faq WHERE id = $1;"
            record: Record = await connection.fetchval(sql_select, int(id))
            return record
    except(Exception, ErrorInAssignmentError) as error:
        logging.info(error)


async def almaushop_faq_find_question_and_answer(id):
    pool: Connection = db
    try:
        async with pool.acquire() as connection:
            sql_select = "SELECT question, answer FROM almau_shop_faq WHERE id = $1;"
            record: Record = await connection.fetchrow(sql_select, int(id))
            return record
    except(Exception, ErrorInAssignmentError) as error:
        logging.info(error)


async def main_faq_select_question_and_answer(id):
    pool: Connection = db
    try:
        async with pool.acquire() as connection:
            sql_select = "SELECT question, answer FROM main_faq WHERE id = $1;"
            record: Record = await connection.fetchrow(sql_select, int(id))
            return record
    except(Exception, ErrorInAssignmentError) as error:
        logging.info(error)


async def select_almau_shop_menu_button_content(button_name):
    pool: Connection = db
    try:
        async with pool.acquire() as connection:
            sql_select = "SELECT button_content FROM almau_shop_menu_buttons WHERE button_name = $1;"
            record: Record = await connection.fetchval(sql_select, str(button_name))
            return record
    except(Exception, ErrorInAssignmentError) as error:
        logging.info(error)


# Удлаение кнопки faq Almau Shop
async def delete_faq_almaushop_button(question):
    pool: Connection = db
    try:
        async with pool.acquire() as connection:
            # async with pool.transaction():
            sql_ex = "Delete from almau_shop_faq where question = $1"
            record: Record = await connection.fetchrow(sql_ex, str(question))
            logging.info(f"DELETED faq - ({question})")
            return record
    except(Exception, ErrorInAssignmentError) as error:
        logging.info(error)


# Удлаение кнопки FAQ в главном меню
async def delete_main_faq_button(question):
    pool: Connection = db
    try:
        async with pool.acquire() as connection:
            # async with pool.transaction():
            sql_ex = "Delete from main_faq where question = $1"
            record: Record = await connection.fetchrow(sql_ex, str(question))
            logging.info(f"DELETED main_faq question - ({question})")
            return record
    except(Exception, ErrorInAssignmentError) as error:
        logging.info(error)


async def find_schedule_id(name):
    pool: Connection = db
    try:
        async with pool.acquire() as connection:
            sql_select = "SELECT id_sched FROM schedule WHERE name_sched = $1;"
            record: Record = await connection.fetchrow(sql_select, name)
            record = list(record)[0]
            return record
    except(Exception, ErrorInAssignmentError) as error:
        logging.info(error)


############## Для тестов ####################
# async def insert_data():
#     pool: Connection = db
#     try:
#         async with pool.acquire() as connection:
#             # async with pool.transaction():
#             sql_select = "Insert into users(username, firstname, lastname, idt, date_time) values ('dedus1337', 'Иван', 'Иванов', 555455, to_timestamp(now(), 'dd-mm-yyyy hh24:mi:ss'));"
#             await connection.execute(sql_select)
#     except(Exception, ErrorInAssignmentError) as error:
#         logging.info(error)
###############################################

async def check_id(id):
    pool: Connection = db
    try:
        async with pool.acquire() as connection:
            sql_ex = "SELECT idt FROM users WHERE idt=$1;"
            record: Record = await connection.fetchrow(sql_ex, int(id))
            return record[0]
    except(Exception, ErrorInAssignmentError) as error:
        pass


async def check_role(id, role):
    pool: Connection = db
    try:
        async with pool.acquire() as connection:
            sql_ex = "SELECT role FROM users WHERE idt = $1 AND role = $2;"
            record: Record = await connection.fetchrow(sql_ex, int(id), role)
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
            record: Record = await connection.fetchrow(sql_ex, username_n, first_name, last_name, id)
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
            record: Record = await connection.fetchrow(sql_ex, int(id_Telegram), str(id_sched), str(name_sched))
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


async def add_feedback_msg_data(id_Telegram, full_name, phone, email, message_content):
    pool: Connection = db
    try:
        async with pool.acquire() as connection:
            # async with pool.transaction():
            sql_ex = "Insert into message_to_rector(id_Telegram, full_name, phone, email, message_content, date_time) values ($1,$2,$3,$4,$5, now())"
            record: Record = await connection.fetchrow(sql_ex, int(id_Telegram), str(full_name), str(phone), str(email),
                                                       str(message_content))
            logging.info(f"ADD messages for feedback to rector")
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


# Добавления мерча в таблицу 'almau_shop_products'
async def add_almau_shop_data(id_Telegram, product_name, price, currency, img, url):
    pool: Connection = db
    try:
        async with pool.acquire() as connection:
            # async with pool.transaction():
            sql_ex = "Insert into almau_shop_products(id_telegram, product_name, price, currency, img, url) values ($1,$2,$3,$4,$5,$6)"
            record: Record = await connection.fetchrow(sql_ex, int(id_Telegram), str(product_name), int(price),
                                                       str(currency),
                                                       str(img), str(url))
            logging.info(f"ADD data of merch from almaushop website to table")
            return record
    except(Exception, ErrorInAssignmentError) as error:
        logging.info(error)


# Добавления книг в таблицу 'almau_shop_books'
async def add_almau_shop_books(id_Telegram, book_name, book_author, price, currency, img, url):
    pool: Connection = db
    try:
        async with pool.acquire() as connection:
            # async with pool.transaction():
            sql_ex = "Insert into almau_shop_books(id_telegram, book_name, book_author, price, currency, img, url) values ($1,$2,$3,$4,$5,$6,$7)"
            record: Record = await connection.fetchrow(sql_ex, int(id_Telegram), str(book_name), str(book_author),
                                                       int(price), str(currency),
                                                       str(img), str(url))
            logging.info(f"ADD data of books from almaushop website to table")
            return record
    except(Exception, ErrorInAssignmentError) as error:
        logging.info(error)


async def add_almau_shop_faq(id_telegram, question, answer):
    pool: Connection = db
    try:
        async with pool.acquire() as connection:
            sql_ex = "Insert into almau_shop_faq(id_Telegram, question, answer, date_time) values ($1,$2,$3,now())"
            record: Record = await connection.fetchrow(sql_ex, int(id_telegram), str(question), str(answer))
            logging.info(f"ADD almaushop faq({question}) to DB")
            return record
    except(Exception, ErrorInAssignmentError) as error:
        logging.info(error)


async def add_data_main_faq(id_telegram, question, answer):
    pool: Connection = db
    try:
        async with pool.acquire() as connection:
            sql_ex = "Insert into main_faq(id_Telegram, question, answer, date_time) values ($1,$2,$3,now())"
            record: Record = await connection.fetchrow(sql_ex, int(id_telegram), str(question), str(answer))
            logging.info(f"ADD main_faq({question}) to DB")
            return record
    except(Exception, ErrorInAssignmentError) as error:
        logging.info(error)


async def edit_almau_shop_menu_button(id_telegram, button_content, button_name):
    pool: Connection = db
    try:
        async with pool.acquire() as connection:
            sql_ex = "Update almau_shop_menu_buttons set id_Telegram = $1, button_content = $2, date_time = now() Where button_name = $3"
            record: Record = await connection.fetch(sql_ex, int(id_telegram), str(button_content), str(button_name))
            logging.info(f"EDIT almaushop button = ({button_name})")
            return record
    except(Exception, ErrorInAssignmentError) as error:
        logging.info(error)


async def edit_almau_shop_faq_question(id_telegram, question, id):
    pool: Connection = db
    try:
        async with pool.acquire() as connection:
            sql_ex = "Update almau_shop_faq set id_Telegram = $1, question = $2, date_time = now() Where id = $3"
            record: Record = await connection.fetch(sql_ex, int(id_telegram), str(question), int(id))
            logging.info(f"EDIT almaushop faq id = ({id}) to DB")
            return record
    except(Exception, ErrorInAssignmentError) as error:
        logging.info(error)


async def edit_almau_shop_faq_answer(id_telegram, answer, id):
    pool: Connection = db
    try:
        async with pool.acquire() as connection:
            sql_ex = "Update almau_shop_faq set id_Telegram = $1, answer = $2, date_time = now() Where id = $3"
            record: Record = await connection.fetchrow(sql_ex, int(id_telegram), str(answer), int(id))
            logging.info(f"EDIT almaushop faq id = ({id}) to DB")
            return record
    except(Exception, ErrorInAssignmentError) as error:
        logging.info(error)


async def edit_main_faq_question(id_telegram, question, id):
    pool: Connection = db
    try:
        async with pool.acquire() as connection:
            sql_ex = "Update main_faq set id_Telegram = $1, question = $2, date_time = now() Where id = $3"
            record: Record = await connection.fetch(sql_ex, int(id_telegram), str(question), int(id))
            logging.info(f"EDIT  main_faq question id = ({id}) to DB")
            return record
    except(Exception, ErrorInAssignmentError) as error:
        logging.info(error)


async def edit_main_faq_answer(id_telegram, answer, id):
    pool: Connection = db
    try:
        async with pool.acquire() as connection:
            sql_ex = "Update main_faq set id_Telegram = $1, answer = $2, date_time = now() Where id = $3"
            record: Record = await connection.fetchrow(sql_ex, int(id_telegram), str(answer), int(id))
            logging.info(f"EDIT  main_faq answer id = ({id}) to DB")
            return record
    except(Exception, ErrorInAssignmentError) as error:
        logging.info(error)


async def update_schedule_data(id_Telegram, id_sched, name_sched):
    pool: Connection = db
    try:
        async with pool.acquire() as connection:
            # async with pool.transaction():
            sql_ex = "Update schedule set id_Telegram = $1, id_sched = $2 Where name_sched = $3"
            record: Record = await connection.fetchrow(sql_ex, int(id_Telegram), str(id_sched), str(name_sched))
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
            record: Record = await connection.fetchrow(sql_ex, str(name_sched))
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


# Полная очистка таблицы almau_shop_books
async def clear_almaushop_books_table():
    pool: Connection = db
    try:
        async with pool.acquire() as connection:
            # async with pool.transaction():
            sql_ex = "DELETE FROM almau_shop_books;"
            record: Record = await connection.fetchrow(sql_ex)
            logging.info(f"All data deleted from almau_shop_books table")
            return record
    except(Exception, ErrorInAssignmentError) as error:
        logging.info(error)


async def add_contact_center_data(id_Telegram, description_contact_center, name_contact_center):
    pool: Connection = db
    try:
        async with pool.acquire() as connection:
            # async with pool.transaction():
            sql_ex = "Insert into contact_centers(id_Telegram, description_contact_center, name_contact_center) values ($1,$2,$3)"
            record: Record = await connection.fetchrow(sql_ex, int(id_Telegram), str(description_contact_center),
                                                       str(name_contact_center))
            logging.info(f"ADD contact_centers ({name_contact_center})")
            return record
    except(Exception, ErrorInAssignmentError) as error:
        logging.info(error)


# Удаления ключевого центра
async def delete_contact_center_button(name_contact_center):
    pool: Connection = db
    try:
        async with pool.acquire() as connection:
            # async with pool.transaction():
            sql_ex = "Delete from contact_centers where name_contact_center = $1"
            record: Record = await connection.fetchrow(sql_ex, str(name_contact_center))
            logging.info(f"DELETED contact_center ({name_contact_center})")
            return record
    except(Exception, ErrorInAssignmentError) as error:
        logging.info(error)


# обновление описания центра
async def update_contact_center_data(id_Telegram, description_contact_center, name_contact_center):
    pool: Connection = db
    try:
        async with pool.acquire() as connection:
            # async with pool.transaction():
            sql_ex = "Update contact_centers set id_Telegram = $1, description_contact_center = $2 Where name_contact_center = $3"
            record: Record = await connection.fetchrow(sql_ex, int(id_Telegram), str(description_contact_center),
                                                       str(name_contact_center))
            logging.info(f"UPDATED contact_center ({name_contact_center})")
            return record
    except(Exception, ErrorInAssignmentError) as error:
        logging.info(error)


# Описание определенного  центра
async def contact_center_description(name):
    pool: Connection = db
    try:
        async with pool.acquire() as connection:
            sql_select = "SELECT description_contact_center FROM contact_centers WHERE name_contact_center = $1;"
            record: Record = await connection.fetchrow(sql_select, name)
            record = list(record)[0]
            return record
    except(Exception, ErrorInAssignmentError) as error:
        logging.info(error)


# Все данные о контактах ключевых центров
async def select_data_contact_centers():
    pool: Connection = db
    try:
        async with pool.acquire() as connection:
            sql_select = "SELECT * FROM contact_centers ORDER BY id;"
            record: Record = await connection.fetch(sql_select)
            return record
    except(Exception, ErrorInAssignmentError) as error:
        logging.info(error)


async def add_pps_data(id_Telegram, shcool, position, description):
    pool: Connection = db
    try:
        async with pool.acquire() as connection:
            # async with pool.transaction():
            sql_ex = "Insert into tutors_and_employees(id_Telegram, shcool, position, description, date_time) values ($1,$2,$3,$4,now())"
            record: Record = await pool.fetchrow(sql_ex, int(id_Telegram), str(shcool),
                                                 str(position), str(description))
            logging.info(f"ADD info to ({shcool}) shcool")
            return record
    except(Exception, ErrorInAssignmentError) as error:
        logging.info(error)


async def pps_center_description(shcool, position):
    pool: Connection = db
    try:
        sql_select = "SELECT description FROM tutors_and_employees WHERE shcool = $1 and position=$2 ORDER BY id DESC LIMIT 1;"
        record: Record = await pool.fetchrow(sql_select, str(shcool), str(position))
        record = list(record)[0]
        return record
    except(Exception, ErrorInAssignmentError) as error:
        logging.info(error)


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
    except Exception as error:
        print(f'Error - {error}')


# Тестировочка времени
# async def test_test():
#     pool: Connection = db
#     try:
#         async with pool.acquire() as connection:
#             # async with pool.transaction():
#             sql_ex = "SELECT date_time From users WHERE date_time IS NOT NULL"
#             record: Record = await pool.fetch(sql_ex)
#             return record
#     except(Exception, ErrorInAssignmentError) as error:
#         logging.info(error)

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
    # await create_table_academic_calendar()
    # await set_up_tables()
    # print(await clear_almaushop_table())
    # await add_almau_shop_books(5135215, 'book_name', 'book_author', 54545, 'currency', 'img', 'url')
    # await add_almau_shop_faq(1488, "Poel?", "Yes dada")
    # print(await almaushop_faq_find_answer(14))
    # print(await almaushop_faq_find_question_and_answer(12))
    # for i in (await almaushop_faq_select_data()):
    #     print(i['id'], i['question'], i['answer'])
    # await edit_almau_shop_faq_question(468899120, 'Как можно?', 12)
    # for i in (await test_test()):
    #     print(i['date_time'].day)
    # print(i['date_time'], type(i['date_time']))
    # await register_user_phone(468899120, '+767565345353')
    # print(type(await check_phone_in_users('+7707101062065')))
    # if not (await check_phone_in_users('+77071010620')):
    #     print('Netu')
    # else:
    #     print('EST')
    # for i in (await select_last_ten_users()):
    #     print(i)
    print((await find_user_by_telegram_id(468899120))['phone'])

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    run = loop.run_until_complete(main())
