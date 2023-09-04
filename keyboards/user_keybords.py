from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, ParseMode, KeyboardButton
from peewee import *
from db import Statistic, Client_info, Doctor_info, Doctor_service, Service_info, Service_type, Sales_info, Coupon



db = SqliteDatabase('vetbot.db')


def main_menu():
    menu_kb = ReplyKeyboardMarkup(row_width=4, one_time_keyboard=True)
    serv_btn = KeyboardButton("Услуги")
    docs_btn = KeyboardButton("Врачи")
    cont_btn = KeyboardButton("Контакты")
    wrt_btn = KeyboardButton("Запись на прием")
    menu_kb.add(serv_btn, docs_btn, cont_btn, wrt_btn)
    return menu_kb


def coupon_menu():
    menu_kb = ReplyKeyboardMarkup(row_width=2, one_time_keyboard=True)
    yes_btn = KeyboardButton('Да')
    no_btn = KeyboardButton('Нет')
    menu_kb.add(no_btn, yes_btn)
    return menu_kb



def services_type_menu():
    stm = Service_type.select()
    services_type_kb = ReplyKeyboardMarkup(row_width=2)
    for service in stm:
        services_type_kb.add(service.ServiceType)
    return services_type_kb


def services_name_menu(st):
    # snm = Service_info.select()
    # snms = [snm.ServiceName for snm in snm]
    # services_name_kb = ReplyKeyboardMarkup(row_width=2)
    # for service in snms:
    #     services_name_kb.add(service)

    qq = Service_info.select().join(Service_type).where(Service_type.ServiceType == f'{st}')
    services_name_kb = ReplyKeyboardMarkup(row_width=2, one_time_keyboard=True)
    for service in qq:
        services_name_kb.add(KeyboardButton(service.ServiceName))

    return services_name_kb


def docs_menu():
    DFN = Doctor_info.select()
    docs_kb = ReplyKeyboardMarkup(row_width=2, one_time_keyboard=True)
    doc1_btn = KeyboardButton("Все врачи")
    docs_kb.add(doc1_btn)
    for dock in DFN:
        docs_kb.add(dock.DoctorFullName)
    # doc2_btn = KeyboardButton("Врач 1 ")
    # doc3_btn = KeyboardButton("Врач 2")
    #docs_kb.add(doc1_btn, doc2_btn, doc3_btn)
    return docs_kb


def stock_menu():
    stock_kb = ReplyKeyboardMarkup(row_width=2, one_time_keyboard=True)
    slv_btn = KeyboardButton("SLIVKI")
    stk_btn = KeyboardButton("Акции")
    stock_kb.add(slv_btn, stk_btn)
    return stock_kb

def back_button():
    back_kb = InlineKeyboardMarkup(row_width=2)
    back_btn = InlineKeyboardButton('Предыдущий шаг', callback_data='back')
    mainmenu_btn = InlineKeyboardButton('Главное меню', callback_data='mainmenu')
    back_kb.add(back_btn, mainmenu_btn)
    return back_kb

def mainmenu_button():
    mainmenu_kb = InlineKeyboardMarkup()
    mainmenu_btn = InlineKeyboardButton('Главное меню', callback_data='mainmenu')
    mainmenu_kb.add(mainmenu_btn)
    return mainmenu_kb