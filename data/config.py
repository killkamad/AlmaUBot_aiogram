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

schedule_button_text = "📅 Расписание"
faq_button_text = "❓ FAQ"
library_button_text = "📚 Библиотека"
shop_button_text = "🌀 AlmaU Shop"
calendar_button_text = "🗒 Академический календарь"
certificate_button_text = "🏢 Получить справку"
feedback_button_text = "📝 Связь с эдвайзером"
navigation_button_text = "🗺️ Навигация по университету"

main_menu_def_buttons = [schedule_button_text, faq_button_text, library_button_text, shop_button_text,
                         calendar_button_text, certificate_button_text, feedback_button_text, navigation_button_text]

almaushop_products_button = "🛍  Брендированная продукция"
almaushop_books_button = "📚  Книги"
almaushop_website_button = "🌐  Вебсайт"
almaushop_contacts_button = "☎  Контакты"
almaushop_faq_button = "⁉  ЧаВо"

almaushop_def_buttons = [almaushop_products_button, almaushop_books_button, almaushop_website_button,
                         almaushop_contacts_button, almaushop_faq_button]

feedback_advisor_button = "✏ Написать письмо эдвайзеру"
