from aiogram.dispatcher.filters.state import State, StatesGroup

from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, ParseMode, KeyboardButton


def admin_keyboard():
    admin_kb = ReplyKeyboardMarkup(row_width=3)
    doc_btn = KeyboardButton("Врачи")
    stat_btn = KeyboardButton("Статистика")
    send_btn = KeyboardButton("Рассылка")
    add_btn = KeyboardButton("Добавить врача")
    admin_kb.add(doc_btn, stat_btn, send_btn, add_btn)
    return admin_kb

def add_doctor_keyboard():
    add_kb = ReplyKeyboardMarkup(row_width=1)
    add_btn = KeyboardButton("Добавить врача")
    add_kb.add(add_btn)
    return add_kb

def editing_doc(dlt):
    editing_kb = InlineKeyboardMarkup(row_width=2)
    edit_kb = InlineKeyboardButton("Редактировать", callback_data=f"editing_info;{dlt}")
    delete_kb = InlineKeyboardButton("Удалить врача", callback_data=f"delete_doctor{dlt}")
    editing_kb.add(edit_kb, delete_kb)
    return editing_kb

def send_message():
    send_message_kb = InlineKeyboardMarkup(row_width=1)
    send_btn = InlineKeyboardButton("Отправить", callback_data=f"send;go")
    reject_btn = InlineKeyboardButton("Не отправлять", callback_data=f"send;reject")
    return send_message_kb.add(send_btn, reject_btn)

