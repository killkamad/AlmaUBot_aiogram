import asyncio
from asyncpg import ErrorInAssignmentError, Connection, Record
from loader import db
import logging


async def main_faq_select_question_and_answer_and_type(id):
    pool: Connection = db
    try:
        async with pool.acquire() as connection:
            sql_select = "SELECT question, answer, type_answer FROM main_faq WHERE id = $1;"
            record: Record = await connection.fetchrow(sql_select, int(id))
            return record
    except(Exception, ErrorInAssignmentError) as error:
        logging.info(error)


# Главное меню FAQ получение айди, вопроса и ответа
async def main_faq_select_data(page):
    pool: Connection = db
    try:
        async with pool.acquire() as connection:
            sql_select = "SELECT id, question, answer FROM main_faq ORDER BY id LIMIT 10 OFFSET $1*10;"
            record: Record = await connection.fetch(sql_select, int(page))
            return record
    except(Exception, ErrorInAssignmentError) as error:
        logging.info(error)


# Главное меню FAQ получение айди, вопроса и ответа ЕЩЕ 10 штук
async def main_faq_select_data_next_ten_rows():
    pool: Connection = db
    try:
        async with pool.acquire() as connection:
            sql_select = "SELECT id, question, answer FROM main_faq ORDER BY id LIMIT 10 OFFSET 0;"
            record: Record = await connection.fetch(sql_select)
            return record
    except(Exception, ErrorInAssignmentError) as error:
        logging.info(error)


# Подсчет строк
async def main_faq_count():
    pool: Connection = db
    try:
        async with pool.acquire() as connection:
            sql_select = "SELECT count(*) FROM main_faq;"
            record: Record = await connection.fetchval(sql_select)
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


async def add_data_main_faq(id_telegram, question, answer, type_answer):
    pool: Connection = db
    try:
        async with pool.acquire() as connection:
            sql_ex = "Insert into main_faq(id_Telegram, question, answer, type_answer, date_time) values ($1,$2,$3,$4,now())"
            record: Record = await connection.fetchrow(sql_ex, int(id_telegram), str(question), str(answer),
                                                       str(type_answer))
            logging.info(f"ADD main_faq({question}) to DB")
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


async def edit_main_faq_answer(id_telegram, answer, id, type_answer):
    pool: Connection = db
    try:
        async with pool.acquire() as connection:
            sql_ex = "Update main_faq set id_Telegram = $1, answer = $2, type_answer = $3, date_time = now() Where id = $4"
            record: Record = await connection.fetchrow(sql_ex, int(id_telegram), str(answer), str(type_answer), int(id))
            logging.info(f"EDIT  main_faq answer id = ({id}) to DB")
            return record
    except(Exception, ErrorInAssignmentError) as error:
        logging.info(error)


async def main():
    # print(await main_faq_count())
    # for i, j in enumerate(await main_faq_select_data_next_ten_rows(), 1):
    #     print(i, j)
    # print(await main_faq_select_data_next_ten_rows())
    for i in range(15):
        await add_data_main_faq(124342141, f"question{i}?", f'answer{i}')


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    run = loop.run_until_complete(main())
