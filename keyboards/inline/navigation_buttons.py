from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from utils import db_api as db
from data.button_names.navigation_buttons import floor_1, floor_2, floor_3, floor_4, floor_5, floor_6, \
    navigation_university, contact_centers, \
    tutors_university, old_building, new_building, dean_button, teachers_button, rector_button, prorectors_button, \
    management_button, law_button, \
    sem_button, startup_button, business_button, econ_button, rector_place_button, map_menu_button, back_to_old_button, \
    back_to_new_button
from data.button_names.main_menu_buttons import to_back_button
from .callback_datas import cabinet_callback, nav_center_callback


def inline_keyboard_nav_unifi():
    markup = InlineKeyboardMarkup(row_width=1)
    callback_button = InlineKeyboardButton(text=navigation_university, callback_data='map_nav')
    callback_button1 = InlineKeyboardButton(text=contact_centers, callback_data='contacts_center')
    callback_button2 = InlineKeyboardButton(text=tutors_university, callback_data='tutors_university')
    # callback_button3 = InlineKeyboardButton(text="⬅ Назад", callback_data="go_back")
    markup.add(callback_button, callback_button1, callback_button2)
    return markup


# async def inline_keyboard_contacts_center():
#     markup = InlineKeyboardMarkup(row_width=1)
#     schedule = await db.select_data_contact_centers()
#     call_list = []
#     name = []
#     for call_value in schedule:
#         callback_data = "['contacts_center_call', '" + call_value[-1] + "']"
#         name.append(call_value[3])
#         call_list.append(callback_data)
#     markup.add(*[InlineKeyboardButton(text=button, callback_data=call_data) for button, call_data in
#                  zip(name, call_list)])
#     markup.add(InlineKeyboardButton(text="⬅ Назад", callback_data="/nav_unifi"))
#     return markup


async def inline_keyboard_contacts_center():
    markup = InlineKeyboardMarkup(row_width=1)
    centers = await db.select_data_contact_centers()
    markup.add(
        *[InlineKeyboardButton(text=item['name_contact_center'],
                               callback_data=nav_center_callback.new(id=item["id"]))
          for item in centers])
    markup.add(InlineKeyboardButton(text=to_back_button, callback_data="/nav_unifi"))
    return markup


def inline_keyboard_contacts_center_back():
    markup = InlineKeyboardMarkup(row_width=1)
    callback_button = InlineKeyboardButton(text=to_back_button, callback_data='contacts_center')
    markup.add(callback_button)
    return markup


# Кнопки Профессорско-преподавательский состав
def inline_keyboard_pps():
    markup = InlineKeyboardMarkup(row_width=1)
    callback_button = InlineKeyboardButton(text=management_button, callback_data='shcool_management')
    callback_button1 = InlineKeyboardButton(text=law_button, callback_data='shcool_law')
    callback_button2 = InlineKeyboardButton(text=sem_button, callback_data='shcool_engineer')
    callback_button3 = InlineKeyboardButton(text=startup_button,
                                            callback_data='shcool_inovation')
    callback_button4 = InlineKeyboardButton(text=business_button, callback_data='shcool_bussines')
    callback_button5 = InlineKeyboardButton(text=econ_button, callback_data='shcool_economic')
    callback_button6 = InlineKeyboardButton(text=rector_place_button, callback_data='rectorat')
    callback_button7 = InlineKeyboardButton(text=to_back_button, callback_data="/nav_unifi")
    markup.add(callback_button, callback_button1, callback_button2, callback_button3, callback_button4,
               callback_button5, callback_button6, callback_button7)
    return markup


def inline_keyboard_pps_shcool_choise(schoolUni):
    markup = InlineKeyboardMarkup(row_width=1)
    callback_button = InlineKeyboardButton(text=dean_button, callback_data='callback_dekan_shcool_' + schoolUni)
    callback_button1 = InlineKeyboardButton(text=teachers_button, callback_data='callback_tutors_shcool_' + schoolUni)
    callback_button2 = InlineKeyboardButton(text=to_back_button, callback_data='tutors_university')
    markup.add(callback_button, callback_button1, callback_button2)
    return markup


def inline_keyboard_pps_rectorat():
    markup = InlineKeyboardMarkup(row_width=1)
    callback_button = InlineKeyboardButton(text=rector_button, callback_data='rectorat_rector')
    callback_button1 = InlineKeyboardButton(text=prorectors_button, callback_data='rectorat_humans')
    callback_button2 = InlineKeyboardButton(text=to_back_button, callback_data='tutors_university')
    markup.add(callback_button, callback_button1, callback_button2)
    return markup


def inline_keyboard_pps_shcool_back(school):
    markup = InlineKeyboardMarkup(row_width=1)
    callback_button = InlineKeyboardButton(text=to_back_button, callback_data='shcool_' + school)
    markup.add(callback_button)
    return markup


def inline_keyboard_pps_rectorat_back():
    markup = InlineKeyboardMarkup(row_width=1)
    callback_button = InlineKeyboardButton(text=to_back_button, callback_data='rectorat')
    markup.add(callback_button)
    return markup


# кнопки карт навигации
def inline_keyboard_map_nav():
    markup = InlineKeyboardMarkup(row_width=1)
    callback_button = InlineKeyboardButton(text=old_building, callback_data='old_building')
    callback_button1 = InlineKeyboardButton(text=new_building, callback_data='new_building')
    callback_button2 = InlineKeyboardButton(text=to_back_button, callback_data="/nav_unifi")
    markup.add(callback_button, callback_button1, callback_button2)
    return markup


def inline_keyboard_new_building():
    markup = InlineKeyboardMarkup(row_width=1)
    callback_button = InlineKeyboardButton(text=floor_1, callback_data='new_building_first')
    callback_button1 = InlineKeyboardButton(text=floor_2, callback_data='new_building_second')
    callback_button2 = InlineKeyboardButton(text=floor_3, callback_data='new_building_third')
    callback_button3 = InlineKeyboardButton(text=floor_4, callback_data='new_building_fourth')
    callback_button4 = InlineKeyboardButton(text=floor_5, callback_data='new_building_fifth')
    callback_button5 = InlineKeyboardButton(text=floor_6, callback_data='new_building_sixth')
    callback_button6 = InlineKeyboardButton(text=to_back_button, callback_data="map_nav")
    markup.add(callback_button, callback_button1, callback_button2, callback_button3, callback_button4,
               callback_button5, callback_button6)
    return markup


def inline_keyboard_old_building():
    markup = InlineKeyboardMarkup(row_width=1)
    callback_button = InlineKeyboardButton(text=floor_1, callback_data='old_building_first')
    callback_button1 = InlineKeyboardButton(text=floor_2, callback_data='old_building_second')
    callback_button2 = InlineKeyboardButton(text=floor_3, callback_data='old_building_third')
    callback_button3 = InlineKeyboardButton(text=floor_4, callback_data='old_building_fourth')
    callback_button4 = InlineKeyboardButton(text=to_back_button, callback_data="map_nav")
    markup.add(callback_button, callback_button1, callback_button2, callback_button3, callback_button4)
    return markup


# кнопки перехода
def inline_keyboard_new_building_back():
    markup = InlineKeyboardMarkup(row_width=1)
    callback_button = InlineKeyboardButton(text=map_menu_button, callback_data="map_nav")
    markup.add(callback_button)
    return markup


def inline_keyboard_old_building_back(building_callback, floor_callback):
    markup = InlineKeyboardMarkup(row_width=1)
    callback_button = InlineKeyboardButton(text=to_back_button,
                                           callback_data=building_callback + "building" + floor_callback)
    callback_button1 = InlineKeyboardButton(text=back_to_old_button, callback_data="old_building")
    callback_button2 = InlineKeyboardButton(text=back_to_new_button, callback_data="new_building")
    markup.add(callback_button, callback_button1, callback_button2)
    return markup


# кнопки кабинетов нового здания
async def inline_keyboard_cabinets_dinamyc(building, floor):
    markup = InlineKeyboardMarkup(row_width=3)
    if building == 'Новое здание':
        build_call = 'new'
    else:
        build_call = 'old'
    map_navigation = await db.map_nav_description(building, floor)
    markup.add(
        *[InlineKeyboardButton(text=item['cabinet'], callback_data=cabinet_callback.new(id=item["id"])) for
          item in map_navigation])
    markup.add(InlineKeyboardButton(text=to_back_button, callback_data=build_call + "_building"))
    return markup
