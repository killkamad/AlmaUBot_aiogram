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
schedule_callback = CallbackData('sch', 'schedule_name')
schedule_update_callback = CallbackData('schupd', 'schedule_name')
schedule_delete_callback = CallbackData('schdel', 'schedule_name')

# Certificate
certificate_callback = CallbackData('crt', 'id')
certificate_update_callback = CallbackData('crtu', 'id')
certificate_delete_callback = CallbackData('crtd', 'id')

# Request
request_callback = CallbackData('req', 'request_name')
request_type_callback = CallbackData('reqt', 'request_name')
request_update_callback = CallbackData('requ', 'request_name')
request_delete_callback = CallbackData('reqd', 'request_name')

# map-navigation
cabinet_callback = CallbackData('cab', 'cabinet')
cabinet_callback_update = CallbackData('cabu', 'cabinet')
cabinet_callback_delete = CallbackData('cabd', 'cabinet')

# centers univer
nav_center_callback = CallbackData('cntr', 'id')
nav_center_callback_update = CallbackData('cntr_u', 'id')
nav_center_callback_delete = CallbackData('cntr_d', 'id')

#Library resources
lib_res_callback = CallbackData('lib', 'id')
lib_res_delete_callback = CallbackData('libd', 'id')
