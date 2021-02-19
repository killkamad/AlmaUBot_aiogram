from aiogram import executor

from loader import dp
from utils.notify_admins import on_startup_notify
import filters, middlewares
filters.setup(dp)
import handlers
middlewares.setup(dp)


async def on_startup(dispatcher):
    # Уведомляет про запуск
    await on_startup_notify(dispatcher)


if __name__ == '__main__':
    executor.start_polling(dp, on_startup=on_startup)
