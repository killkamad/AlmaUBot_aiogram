import asyncio
from asyncpg import ErrorInAssignmentError, Connection, Record
from loader import db
import logging


async def main_faq_select_question_and_answer(id):
    pool: Connection = db
    try:
        async with pool.acquire() as connection:
            sql_select = "SELECT question, answer FROM main_faq WHERE id = $1;"
            record: Record = await connection.fetchrow(sql_select, int(id))
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


async def main_faq_select_question_and_answer(id):
    pool: Connection = db
    try:
        async with pool.acquire() as connection:
            sql_select = "SELECT question, answer FROM main_faq WHERE id = $1;"
            record: Record = await connection.fetchrow(sql_select, int(id))
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


async def main():
    print(await main_faq_select_question_and_answer(1))


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    run = loop.run_until_complete(main())
