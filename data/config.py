import os

from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = str(os.getenv("BOT_TOKEN"))
admins = [
    468899120,
    302422833,
    472211929
]

library_admins = [
    668049153,
    846857659
]

# Для Теста
# library_admins = [
#     468899120,
# ]

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

floor_1 = "1️⃣ этаж"
floor_2 = "2️⃣ этаж"
floor_3 = "3️⃣ этаж"
floor_4 = "4️⃣ этаж"
floor_5 = "5️⃣ этаж"
floor_6 = "6️⃣ этаж"

navigation_university = "🗺 Навигация по университету"
contact_centers = "💬 Контакты ключевых центров"
tutors_university = "👨‍🏫 Профессорско-преподавательский состав"

old_building = "🏛 Старое здание"
new_building = "🏢 Новое здание"
