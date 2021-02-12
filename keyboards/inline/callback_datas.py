from aiogram.utils.callback_data import CallbackData

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

# test
buy_callback = CallbackData('buy', 'item_name', 'quantity')
