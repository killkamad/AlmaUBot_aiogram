import asyncio
from loader import bot


async def bot_delete_messages(message, n):
    s = 1
    for i in range(n):
        await bot.delete_message(message.chat.id, message.message_id - s)
        s += 1
