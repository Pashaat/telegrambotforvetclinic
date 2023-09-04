from handlers.admin.edit_info_handler import Editing_info_state
from aiogram.dispatcher import FSMContext
from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from db import Statistic, Client_info, Doctor_info, Doctor_service, Service_info, Service_type, Sales_info, Coupon
from handlers.states import AdminStates, Delete_Doctor_States
from keyboards.admin_keyboard import editing_doc, add_doctor_keyboard
from aiogram.dispatcher.filters.state import State, StatesGroup



async def admin_doctor_list(message: types.Message, state:FSMContext):
        for doctor in Doctor_info.select():
            await message.answer(f'{doctor.Photo}\n{doctor.DoctorFullName}\n{doctor.DoctorInfo}',
                                 reply_markup=editing_doc(doctor.doctor_id),)


async def delete_doctor(callback: types.callback_query, state:FSMContext):
    await Delete_Doctor_States.delete_state.set()

async def editing_info(callback: types.callback_query, state:FSMContext):
    await Editing_info_state.editing_state.set()



async def name_doctor(message: types.Message, state: FSMContext):
    await message.answer("Введите именя врача")
    await AdminStates.info_doctor.set()


async def info_doctor(message: types.Message, state: FSMContext):
    await message.answer("Введите информацию о враче")
    await AdminStates.create_doctor.set()
    await state.set_data({"name": message.text})

async def create_doctor(message: types.Message, state: FSMContext):
    data = await state.get_data()
    name = data['name']
    info = message.text
    Doctor_info.create(DoctorFullName=name, DoctorInfo=info, Photo='фото1')
    await AdminStates.admin_state.set()





def register_admin_handler(dp:Dispatcher):
    dp.register_message_handler(admin_doctor_list, lambda m: m.text.startswith("Врачи"), state=AdminStates.admin_state)
    dp.register_message_handler(name_doctor, lambda m: m.text.startswith("Добавить врача"),state=AdminStates.admin_state)
    dp.register_message_handler(info_doctor, state=AdminStates.info_doctor)
    dp.register_message_handler(create_doctor, state=AdminStates.create_doctor)
    dp.register_callback_query_handler(delete_doctor, lambda c: c.data.startswith(f'editing_info'))
    dp.register_callback_query_handler(editing_info, lambda c: c.data.startswith(f'delete_doctor'))
