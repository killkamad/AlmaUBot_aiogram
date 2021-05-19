import os

from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = str(os.getenv("BOT_TOKEN"))
DB_NAME = str(os.getenv("DB_NAME"))
DB_USER = str(os.getenv("DB_USER"))
DB_PASS = str(os.getenv("DB_PASS"))
DB_HOST = str(os.getenv("DB_HOST"))
DB_PORT = str(os.getenv("DB_PORT"))

# Нужно для оповещения о запуске бота
admins = [
    468899120,
    302422833,
    472211929
]

hostname_bot = "smtp.gmail.com"  # smtp сервер
port_bot = 587  # порт
email_bot = "almaubot@gmail.com"  # почта откуда будут отправляться письма
email_bot_password = "mjykwcchpvduwcjy"  # пароль от почты бота

email_library = "lib@almau.edu.kz"  # почта библиотеки
email_certificate = "g.kyzdarbekova@almau.edu.kz"  # почта куда будут отправлять заявки на справку
