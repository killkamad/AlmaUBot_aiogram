import asyncio

import asyncpg
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from data.config import DB_USER, DB_PASS, DB_HOST, DB_PORT, DB_NAME
from data import config

bot = Bot(token=config.BOT_TOKEN, parse_mode=types.ParseMode.HTML)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)


############  Удаленный сервер  ############
async def create_pool():
    # asyncpg.connect вместо asyncpg.create_pool, потому что не работает
    return await asyncpg.create_pool(database=DB_NAME,
                                     user=DB_USER,
                                     password=DB_PASS,
                                     host=DB_HOST,
                                     port=DB_PORT)


############  Локальный сервер  ############
# async def create_pool():
#     return await asyncpg.connect(database='killka_m',
#                                  user='postgres',
#                                  password='batman2000',
#                                  host='localhost',
#                                  port=5432)


db = dp.loop.run_until_complete(create_pool())
