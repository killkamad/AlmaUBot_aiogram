# Админ кнопки для AlmaU Shop
from .admin_almaushop_buttons import inline_keyboard_almau_shop_admin, inline_keyboard_add_almaushop_faq_or_cancel, \
    inline_keyboard_edit_button_content_almaushop_or_cancel, inline_keyboard_delete_faq_almaushop, \
    inline_keyboard_edit_faq_almaushop, cancel_or_delete_faq_almau_shop, inline_keyboard_edit_faq_almaushop_choice, \
    inline_keyboard_edit_almaushop_faq_or_cancel

# Админ кнопки для Расписания
from .admin_schedule_buttons import inline_keyboard_schedule_admin, cancel_or_send_schedule, cancel_or_update_schedule, \
    cancel_or_delete_schedule, inline_keyboard_update_schedule, inline_keyboard_delete_schedule, inline_keyboard_cancel_schedule

# Админ кнопки для F.A.Q главного меню
from .admin_faq_buttons import inline_keyboard_faq_admin, inline_keyboard_add_main_faq_or_cancel, \
    inline_keyboard_delete_main_faq, inline_keyboard_edit_main_faq, cancel_or_delete_main_faq, \
    inline_keyboard_edit_main_faq_choice, inline_keyboard_edit_main_faq_or_cancel

# Админ кнопки для Пользователей
from .admin_users_buttons import inline_keyboard_users_admin, inline_keyboard_users_admin_roles, \
    inline_keyboard_users_admin_roles_accept_decline, inline_keyboard_select_last_ten_users, back_to_last_ten_users

# Админ кнопки для Массовой рассылки
from .admin_mass_mailing_buttons import inline_keyboard_mass_mailing_send_or_attach, inline_keyboard_cancel_or_send, \
    inline_keyboard_cancel

# Админ кнопки для Академического календаря
from .admin_academic_calendar_buttons import cancel_academic_calendar, cancel_or_send_academic_calendar

# Админ кнопки для меню Навагации
from .admin_navigation_buttons import inline_keyboard_nav_university_admin_menu, inline_keyboard_contact_center_admin, \
    cancel_or_send_contact_center_admin, inline_keyboard_contacts_center_update, cancel_or_update_contact_center_admin, \
    inline_keyboard_contacts_center_delete, cancel_or_delete_contact_center_admin, \
    inline_keyboard_cancel_contact_center_admin, cancel_or_send_tutors_management

# Админ кнопки для Справок
from .admin_certificate_buttons import inline_keyboard_certificate_admin, cancel_or_send_certificate, \
    cancel_or_update_certificate, cancel_or_delete_certificate, inline_keyboard_upd_req_certificate, \
    inline_keyboard_update_certificate, inline_keyboard_del_req_certificate, inline_keyboard_delete_certificate, \
    inline_keyboard_get_request_certificate

# Кнопки для главного админ меню
from .admin_main_buttons import inline_keyboard_admin

# CALLBACK DATAS фильтр
from .callback_datas import almau_shop_faq_callback, almau_shop_faq_edit_callback, almau_shop_faq_delete_callback, \
    main_faq_edit_callback, main_faq_delete_callback, main_faq_callback, schedule_callback, schedule_update_callback, \
    schedule_delete_callback

from .feedback_buttons import inline_keyboard_feedback, inline_keyboard_send_msg_data
from .almaushop_buttons import inline_keyboard_faq_almaushop, inline_keyboard_faq_almaushop_back
from .navigation_buttons import inline_keyboard_nav_unifi, inline_keyboard_contacts_center, \
    inline_keyboard_contacts_center_back
from .certificate_buttons import inline_keyboard_certificate, inline_keyboard_get_certificate, \
    inline_keyboard_send_req_data
from .schedule_buttons import inline_keyboard_schedule
from .menu_buttons import inline_keyboard_menu
from .faq_buttons import inline_keyboard_main_faq, inline_keyboard_main_faq_back
