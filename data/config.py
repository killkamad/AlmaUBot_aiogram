import os

from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = str(os.getenv("BOT_TOKEN"))
admins = [
    468899120,
]

DB_NAME = str(os.getenv("DB_NAME"))
DB_USER = str(os.getenv("DB_USER"))
DB_PASS = str(os.getenv("DB_PASS"))
DB_HOST = str(os.getenv("DB_HOST"))
DB_PORT = str(os.getenv("DB_PORT"))

# ip = os.getenv("ip")
#
# aiogram_redis = {
#     'host': ip,
# }
#
# redis = {
#     'address': (ip, 6379),
#     'encoding': 'utf8'
# }
