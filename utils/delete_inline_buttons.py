from loader import bot
import logging


# Убирает инлайн клавиатуру


async def delete_inline_buttons_in_dialogue(message, n=1):
    try:
        await bot.edit_message_reply_markup(message.chat.id, message.message_id - n)
    except Exception as error:
        # logging.info(error)
        n = n + 1
        if n >= 6:
            return
        await delete_inline_buttons_in_dialogue(message, n)
