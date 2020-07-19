import asyncio
import asyncpg
from asyncpg import ErrorInAssignmentError, Connection, Record
from loader import db


async def select_data():
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


async def insert_data():
    pool: Connection = db
    try:
        async with pool.acquire() as connection:
            async with connection.transaction():
                sql_select = "Insert into users(username, firstname, lastname, idt) values ('cock111', 'big', 'bok', 1421423423);"
                record: Record = await pool.fetchval(sql_select)
        return record
    except(Exception, ErrorInAssignmentError) as error:
        print(error)


async def main():
    # await insert_data()
    count_users = await select_data()
    print(count_users)


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    run = loop.run_until_complete(main())
