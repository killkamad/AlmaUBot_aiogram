from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from data.button_names.lib_buttons import lib_website_button, lib_resources_button, lib_contacts_button, \
                                          lib_work_hours_button, lib_courses_button, lib_idcard_button, \
                                          lib_rules_button, lib_rights_button, lib_unallowed_button, \
                                          lib_responsibility_button, lib_booking_button
from data.button_names.main_menu_buttons import to_main_menu_button, send_phone_button


def keyboard_library():
    markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    callback_button1 = KeyboardButton(text=lib_website_button)
    callback_button2 = KeyboardButton(text=lib_resources_button)
    callback_button3 = KeyboardButton(text=lib_contacts_button)
    callback_button4 = KeyboardButton(text=lib_work_hours_button)
    callback_button7 = KeyboardButton(text=lib_courses_button)
    callback_button8 = KeyboardButton(text=lib_idcard_button)
    callback_button9 = KeyboardButton(text=lib_rules_button)
    callback_button10 = KeyboardButton(text=lib_rights_button)
    callback_button11 = KeyboardButton(text=lib_unallowed_button)
    callback_button12 = KeyboardButton(text=lib_responsibility_button)
    callback_button13 = KeyboardButton(text=lib_booking_button)
    callback_button14 = KeyboardButton(text=to_main_menu_button)
    markup.add(callback_button1, callback_button2, callback_button3, callback_button4,
               callback_button13, callback_button7, callback_button8, callback_button9,
               callback_button10, callback_button11, callback_button12)
    markup.row(callback_button14)
    return markup


def keyboard_library_send_phone():
    markup = ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    button_phone = KeyboardButton(text=send_phone_button, request_contact=True)
    markup.add(button_phone)
    return markup
