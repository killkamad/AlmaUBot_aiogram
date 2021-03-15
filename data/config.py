import os

from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = str(os.getenv("BOT_TOKEN"))
DB_NAME = str(os.getenv("DB_NAME"))
DB_USER = str(os.getenv("DB_USER"))
DB_PASS = str(os.getenv("DB_PASS"))
DB_HOST = str(os.getenv("DB_HOST"))
DB_PORT = str(os.getenv("DB_PORT"))

admins = [
    468899120,
    302422833,
    472211929
]

library_admins = [
    668049153,
    846857659
]
