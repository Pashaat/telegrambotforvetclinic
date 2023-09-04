from aiogram.dispatcher.filters.state import State,StatesGroup

from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from db import Statistic, Client_info, Doctor_info, Doctor_service, Service_info, Service_type, Sales_info, Coupon
from keyboards.admin_keyboard import editing_doc , add_doctor_keyboard



class StateMachine(StatesGroup):
    first_state = State()


class Editing_info_state(StatesGroup):
    editing_state = State()

class Delete_Doctor_States(StatesGroup):
        delete_state = State()


class AdminStates(StatesGroup):
    admin_state = State()
    info_doctor = State()
    create_doctor = State()

class UserStates(StatesGroup):
    user_state = State()
    show_doctor_list_state = State()
    RecClientFullNameState = State()
    RecClientPhoneNumberState = State()
    RecClientEmail = State()
    RecServiceTypeState = State()
    RecServiceNameState = State()
    RecProblemState = State()
    Services_t_state = State()
    RecCouponState = State()
    RecCoupon_nomb_State = State()
    CalendarChoiseState =State()
