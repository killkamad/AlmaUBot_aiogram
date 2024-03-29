from aiogram.utils.callback_data import CallbackData

# ПРИМЕР buy - префикс, item_name - название переменной(похоже на, как сохраняем данные в state), туда можно закладывать, то что нужно сохранить
buy_callback = CallbackData('buy', 'item_name', 'quantity')  # quantity - тоже, название переменной
# в CallbackData, можно добавлять сколько нужно переменных

# AlmaU Shop FAQ
almau_shop_faq_callback = CallbackData('faqsh', 'callback_id')
almau_shop_faq_delete_callback = CallbackData('delete_faqsh', 'callback_id')
almau_shop_faq_edit_callback = CallbackData('edit_faqsh', 'callback_id')

# Main menu FAQ
main_faq_callback = CallbackData('main_faq', 'callback_id')
main_faq_delete_callback = CallbackData('delete_main_faq', 'callback_id')
main_faq_edit_callback = CallbackData('edit_main_faq', 'callback_id')

# Last 10 users
last_ten_users_callback = CallbackData('L10', 'telegram_id')

# Schedule
schedule_callback = CallbackData('sch', 'schedule_id')
schedule_update_callback = CallbackData('schupd', 'schedule_id')
schedule_delete_callback = CallbackData('schdel', 'schedule_id')

# Certificate
instruction_callback = CallbackData('inst', 'id')
instruction_update_callback = CallbackData('instu', 'id')
instruction_add_doc_callback = CallbackData('insta', 'id')
instruction_delete_callback = CallbackData('instd', 'id')

# map-navigation
cabinet_callback = CallbackData('cab', 'id')
cabinet_callback_update = CallbackData('cabu', 'id')
cabinet_callback_delete = CallbackData('cabd', 'id')

# centers univer
nav_center_callback = CallbackData('cntr', 'id')
nav_center_callback_update = CallbackData('cntr_u', 'id')
nav_center_callback_delete = CallbackData('cntr_d', 'id')

# Library resources
lib_res_callback = CallbackData('lib', 'id')
lib_res_delete_callback = CallbackData('libd', 'id')
