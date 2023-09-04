from aiogram.dispatcher.filters.state import State,StatesGroup

from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from db import Statistic, Client_info, Doctor_info, Doctor_service, Service_info, Service_type, Sales_info, Coupon
from handlers.states import Editing_info_state, AdminStates
from keyboards.admin_keyboard import editing_doc , add_doctor_keyboard



async def editing(callback:types.callback_query, state:FSMContext):
    await state.set_data({'doctor_id': callback.data.split(';')[1]})
    await callback.message.answer("Введите новую инфу")
    await Editing_info_state.editing_state.set()



async def new_info(message: types.Message, state:FSMContext):
    doctor_id = await state.get_data()
    doctor = Doctor_info.select().where(Doctor_info.doctor_id == doctor_id['doctor_id']).get()
    doctor.DoctorInfo = message.text
    doctor.save()
    await message.answer("Инфа изменена ")
    await AdminStates.admin_state.set()




def register_editing_handler(dp:Dispatcher):
    dp.register_callback_query_handler(editing, lambda c: c.data.startswith('editing_info'), state='*')
    dp.register_message_handler(new_info, state=Editing_info_state.editing_state)