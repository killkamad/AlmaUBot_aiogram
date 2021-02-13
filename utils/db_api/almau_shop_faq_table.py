import asyncio
from asyncpg import ErrorInAssignmentError, Connection, Record
from loader import db
import logging


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


async def main():
    print(await almaushop_faq_select_data())


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    run = loop.run_until_complete(main())
