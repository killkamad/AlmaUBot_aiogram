# Админ кнопки для AlmaU Shop
from .admin_almaushop_buttons import inline_keyboard_almau_shop_admin, inline_keyboard_add_almaushop_faq_or_cancel, \
    inline_keyboard_edit_button_content_almaushop_or_cancel, inline_keyboard_delete_faq_almaushop, \
    inline_keyboard_edit_faq_almaushop, cancel_or_delete_faq_almau_shop, inline_keyboard_edit_faq_almaushop_choice, \
    inline_keyboard_edit_almaushop_faq_or_cancel, inline_keyboard_cancel_almaushop_faq_create, \
    inline_keyboard_cancel_almaushop_faq_update, inline_keyboard_cancel_almaushop_website_contacts

# Админ кнопки для Расписания
from .admin_schedule_buttons import inline_keyboard_schedule_admin, cancel_or_send_schedule, cancel_or_update_schedule, \
    cancel_or_delete_schedule, inline_keyboard_update_schedule, inline_keyboard_delete_schedule, \
    inline_keyboard_cancel_schedule

# Админ кнопки для F.A.Q главного меню
from .admin_faq_buttons import inline_keyboard_faq_admin, inline_keyboard_add_main_faq_or_cancel, \
    inline_keyboard_delete_main_faq, inline_keyboard_edit_main_faq, cancel_or_delete_main_faq, \
    inline_keyboard_edit_main_faq_choice, inline_keyboard_edit_main_faq_or_cancel, inline_keyboard_cancel_faq, \
    inline_keyboard_cancel_faq_edit

# Админ кнопки для Пользователей
from .admin_users_buttons import inline_keyboard_users_admin, inline_keyboard_users_admin_roles, \
    inline_keyboard_users_admin_roles_accept_decline, inline_keyboard_select_last_ten_users, back_to_last_ten_users, \
    inline_keyboard_cancel_users_role_change

# Админ кнопки для Массовой рассылки
from .admin_mass_mailing_buttons import inline_keyboard_mass_mailing_send_or_attach, inline_keyboard_cancel_or_send, \
    inline_keyboard_cancel_mass_mailing

# Админ кнопки для Академического календаря
from .admin_academic_calendar_buttons import cancel_academic_calendar, cancel_or_send_academic_calendar

# Админ кнопки для меню Навагации
from .admin_navigation_buttons import inline_keyboard_nav_university_admin_menu, inline_keyboard_contact_center_admin, \
    cancel_or_send_contact_center_admin, inline_keyboard_contacts_center_update, cancel_or_update_contact_center_admin, \
    inline_keyboard_contacts_center_delete, cancel_or_delete_contact_center_admin, \
    inline_keyboard_cancel_contact_center_admin, cancel_or_send_tutors_management, inline_keyboard_map_nav_admin_menu, \
    cancel_or_send_map_nav_admin, inline_keyboard_cabinets_admin, cancel_or_update_map_nav_admin, \
    cancel_or_delete_map_nav_admin, inline_keyboard_cancel_map_nav_admin, map_nav_admin_choice_floor_new_delete, \
    map_nav_admin_choice_floor_old_delete, keyboard_map_nav_choice_building_delete, \
    keyboard_map_nav_choice_building_update, \
    map_nav_admin_choice_floor_new_update, map_nav_admin_choice_floor_old_update, map_nav_admin_choice_floor_new, \
    map_nav_admin_choice_floor_old, keyboard_map_nav_choice_building, keyboard_pps_choice_position, \
    keyboard_pps_choice_position_rector, keyboard_pps_choice_shcool, inline_keyboard_cancel_tutors_admin, \
    cancel_or_send_or_image_map_nav_admin, cancel_or_update_or_image_map_nav_admin

# Админ кнопки для Справок
from .admin_certificate_buttons import inline_keyboard_certificate_admin, cancel_or_send_certificate, \
    cancel_or_update_certificate, cancel_or_delete_certificate, inline_keyboard_upd_req_certificate, \
    inline_keyboard_update_certificate, inline_keyboard_del_req_certificate, inline_keyboard_delete_certificate, \
    inline_keyboard_get_request_certificate, inline_keyboard_cancel_certificate, inline_keyboard_get_certificate_type, \
    inline_keyboard_on_send_request_certificate

from .admin_library_buttons import inline_keyboard_library_first_page_admin, inline_keyboard_library_second_page_admin, \
    inline_keyboard_edit_button_content_library_or_cancel, inline_keyboard_cancel_edit_library_button, \
    inline_keyboard_library_res_admin, inline_keyboard_library_res_edit_admin, cancel_or_add_lib_resource, \
    inline_keyboard_del_lib_res, cancel_or_delete_lib_resource, cancel_edit_lib_res

# Кнопки для главного админ меню и админ меню для ролей
from .admin_main_buttons import inline_keyboard_admin, inline_keyboard_library_admin, inline_keyboard_marketing_admin

# CALLBACK DATAS фильтр
from .callback_datas import almau_shop_faq_callback, almau_shop_faq_edit_callback, almau_shop_faq_delete_callback, \
    main_faq_edit_callback, main_faq_delete_callback, main_faq_callback, schedule_callback, schedule_update_callback, \
    schedule_delete_callback, certificate_callback, certificate_update_callback, certificate_delete_callback, \
    request_callback, request_type_callback, request_update_callback, request_delete_callback, \
    cabinet_callback, cabinet_callback_update, nav_center_callback_update, nav_center_callback_delete, \
    nav_center_callback, lib_res_callback, lib_res_delete_callback

from .library_buttons import inline_keyboard_library_registration, inline_keyboard_send_reg_data, \
    inline_keyboard_back_to_library, inline_keyboard_library_el_res, inline_keyboard_library_base_kaz, \
    inline_keyboard_library_base_zarub, inline_keyboard_library_online_bib, inline_keyboard_cancel_lic_db_reg, \
    inline_keyboard_library_choice_db
from .feedback_buttons import inline_keyboard_feedback, inline_keyboard_send_msg_data, inline_keyboard_cancel_msg_send
from .almaushop_buttons import inline_keyboard_faq_almaushop, inline_keyboard_faq_almaushop_back
from .navigation_buttons import inline_keyboard_nav_unifi, inline_keyboard_contacts_center, \
    inline_keyboard_contacts_center_back
from .certificate_buttons import inline_keyboard_certificate, inline_keyboard_get_certificate, \
    inline_keyboard_send_req_data, inline_keyboard_cancel_request
from .schedule_buttons import inline_keyboard_schedule
from .menu_buttons import inline_keyboard_menu
from .faq_buttons import inline_keyboard_main_faq, inline_keyboard_main_faq_back
