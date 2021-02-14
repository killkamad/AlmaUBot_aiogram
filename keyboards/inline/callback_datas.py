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
schedule_callback = CallbackData('schedule_call', 'schedule_name')
schedule_update_callback = CallbackData('schedule_upd_call', 'schedule_name')
schedule_delete_callback = CallbackData('schedule_del_call', 'schedule_name')
