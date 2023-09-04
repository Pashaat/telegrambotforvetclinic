from aiogram.dispatcher.filters.state import State,StatesGroup

from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from db import Statistic, Client_info, Doctor_info, Doctor_service, Service_info, Service_type, Sales_info, Coupon
from keyboards.admin_keyboard import editing_doc , add_doctor_keyboard



async def delete (callback:types.callback_query, ):
    doctor_id = callback.data[13:]
    Doctor_info.delete_by_id(doctor_id)
    await callback.message.answer("AХуеНно")


def register_delete_handler(dp:Dispatcher):
    dp.register_callback_query_handler(delete, lambda c: c.data.startswith(f'delete_doctor'), state='*')