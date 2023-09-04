from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from handlers.states import UserStates
from keyboards.user_keybords import docs_menu, services_type_menu, main_menu, services_name_menu, coupon_menu, back_button
from peewee import *
from db import Statistic, Client_info, Doctor_info, Doctor_service, Service_info, Service_type, Sales_info, Coupon
import datetime
from telegram_bot_calendar import DetailedTelegramCalendar, LSTEP
# from main import cmd_start



db = SqliteDatabase('vetbot.db')


RER = {'y': 'Год', 'm': 'Месяц', 'd': 'день'}
Noww = datetime.datetime.now()
Now_year = Noww.year
Now_month = Noww.month
Now_day = Noww.day



# @dp.callback_query_handler(lambda c: c.data.startswith("Услуги"), state=UserStates.user_state)
# async def serv (callback: types.callback_query):
#     await callback.message.answer(f"{services}")

async def Services_t(message: types.Message):
    await message.answer('Нажмите на кнопку с нужным вам типом услуги', reply_markup=services_type_menu())
    await UserStates.Services_t_state.set()

async def Services(message: types.Message):
    stm = Service_type.select()
    stms = [stm.ServiceType for stm in stm]
    if message.text not in stms:
        await message.answer("Пожалуйста, выберите тип, используя клавиатуру ниже.", reply_markup=services_type_menu())
        return
    qq = Service_info.select().join(Service_type).where(Service_type.ServiceType == f'{message.text}')
    for service in qq:
        await message.answer(f'{service.ServiceName}\nЦена услуги: {service.ServicePrice}', reply_markup=main_menu())
    await UserStates.user_state.set()


async def doctor_list(message: types.Message):
    await message.answer(f"Выберите какого врача вам показать", reply_markup=docs_menu())
    await UserStates.show_doctor_list_state.set()


async def show_doctor_list(message: types.Message):
    # Doctor_info.update(Photo=message.photo[-1].file_id).where(Doctor_info.DoctorFullName == 'павел').execute()
    # print(message.photo[-1].file_id)
    # await message.answer(f'id получено{message.photo[-1].file_id}')

    if message.text == 'Все врачи':
        for doctor in Doctor_info.select():
            await message.answer_photo(photo=doctor.Photo, caption=f'{doctor.DoctorFullName}\n{doctor.DoctorInfo}', reply_markup=main_menu())
    else:
        doctor_inf = Doctor_info.get(Doctor_info.DoctorFullName == message.text)
        await message.answer_photo(photo=doctor_inf.Photo, caption=f'{doctor_inf.DoctorFullName}\n{doctor_inf.DoctorInfo}',
                                   reply_markup=main_menu())
    await UserStates.user_state.set()


async def contact_list(message: types.Message):
    await message.answer(f"Наши контакты:\nПока пусто", reply_markup=main_menu())
    await UserStates.user_state.set()



async def record(message: types.Message | types.CallbackQuery , state: FSMContext):
    if await state.get_state() == UserStates.RecClientPhoneNumberState.state:
        await message.answer('')
        await message.message.answer('Введите ваше ФИО')
        await UserStates.RecClientFullNameState.set()
    else:
        await message.answer(f"Введите ваше ФИО")
        await UserStates.RecClientFullNameState.set()


async def RecordClientFullName(message: types.Message | types.CallbackQuery, state: FSMContext):
    if await state.get_state() == UserStates.RecClientEmail.state:
        await message.answer('')
        await message.message.answer('Введите ваш номер телефона', reply_markup=back_button())
        await UserStates.RecClientPhoneNumberState.set()
    else:
        for i in str(message.text):
            if i.isdigit() == True:
                await message.answer('Введите ФИО без чисел', reply_markup=back_button())
                return
        await state.update_data(ClientFullName=message.text)
        await message.answer('Введите ваш номер телефона', reply_markup=back_button())
        await UserStates.RecClientPhoneNumberState.set()


async def RecordClientPhoneNumber(message: types.Message | types.CallbackQuery, state: FSMContext):
    if await state.get_state() == UserStates.RecServiceTypeState.state:
        await message.answer('')
        await message.message.answer('Введите ваш Email', reply_markup=back_button())
        await UserStates.RecClientEmail.set()
    else:
        if str(message.text)[:4] == '+375':
            if str(message.text)[1:].isdigit():
                if len(str(message.text)) == 13:
                    await state.update_data(ClientPhoneNumber=message.text)
                    await message.answer('Введите ваш Email', reply_markup=back_button())
                    await UserStates.RecClientEmail.set()
                else:
                    await message.answer('Введите телефон правильно', reply_markup=back_button())
                    return
            else:
                await message.answer('Введите телефон правильно', reply_markup=back_button())
                return
        else:
            await message.answer('Введите телефон правильно', reply_markup=back_button())
            return



async def RecordClientEmail(message: types.Message | types.CallbackQuery, state: FSMContext):
    if await state.get_state() == UserStates.RecServiceNameState.state:
        await message.answer('')
        await message.message.answer('Нажмите на кнопку с нужным вам типом услуги', reply_markup=back_button())
        await UserStates.RecServiceTypeState.set()
    else:
        if '@' in str(message.text):
            if '.' in str(message.text)[str(message.text).index('@'):]:
                await state.update_data(ClientEmail=message.text)
                await message.answer('Нажмите на кнопку с нужным вам типом услуги', reply_markup=services_type_menu())
                # await message.answer('', reply_markup=back_button())
                userdata = await state.get_data()
                if not Client_info.select().where(Client_info.client_id == message.from_user.id).exists():
                    Client_info.create(client_id=message.from_user.id,
                                      ClientFullName=userdata['ClientFullName'],
                                      ClientPhoneNumber=userdata['ClientPhoneNumber'],
                                      ClientEmail=userdata['ClientEmail'],
                                      ClientTgUsername=f'{message.from_user.username}')
                await state.finish()
                await UserStates.RecServiceTypeState.set()
            else:
                await message.answer('Введите Email правильно', reply_markup=back_button())
                return
        else:
            await message.answer('Введите Email правильно', reply_markup=back_button())
            return


async def RecordServiceType(message: types.Message | types.CallbackQuery, state: FSMContext):
    if await state.get_state() == UserStates.RecProblemState.state:
        await message.answer('')
        await message.message.answer('Нажмите на кнопку с нужной вам услугой', reply_markup=back_button())
        await UserStates.RecServiceNameState.set()
    else:
        stm = Service_type.select()
        stms = [stm.ServiceType for stm in stm]
        if message.text not in stms:
            await message.answer("Пожалуйста, выберите тип, используя клавиатуру ниже.", reply_markup=services_type_menu())
            return
        await state.update_data(ServiceType=message.text)
        userdata = await state.get_data()
        await message.answer('Нажмите на кнопку с нужной вам услугой', reply_markup=services_name_menu(userdata['ServiceType']))
        await UserStates.RecServiceNameState.set()


async def RecordServiceName(message: types.Message | types.CallbackQuery, state: FSMContext):
    if await state.get_state() == UserStates.RecCouponState.state:
        await message.answer('')
        await message.message.answer('Укажите проблему', reply_markup=back_button())
        await UserStates.RecProblemState.set()
    else:
        snm = Service_info.select()
        snms = [snm.ServiceName for snm in snm]
        userdata = await state.get_data()
        if message.text not in snms:
            await message.answer("Пожалуйста, выберите услугу, используя клавиатуру ниже.",
                                 reply_markup=services_name_menu(userdata['ServiceType']))
            return
        await state.update_data(ServiceName=message.text)
        await message.answer('Укажите проблему', reply_markup=back_button())
        await UserStates.RecProblemState.set()




async def RecordProblem(message: types.Message | types.CallbackQuery, state: FSMContext):
    if await state.get_state() == UserStates.RecCoupon_nomb_State.state:
        await message.answer('')
        await message.message.answer('У вас есть купон?', reply_markup=back_button())
        await UserStates.RecCouponState.set()
    elif await state.get_state() == UserStates.CalendarChoiseState.state:
        await message.answer('')
        await message.message.answer('У вас есть купон?', reply_markup=back_button())
        await UserStates.RecCouponState.set()
    else:
        await state.update_data(Problem=message.text)
        await message.answer('У вас есть купон?', reply_markup=coupon_menu())
        await UserStates.RecCouponState.set()


async def RecordCoupon(message: types.Message | types.CallbackQuery, state: FSMContext):
    if await state.get_state() == UserStates.CalendarChoiseState.state:
        await message.answer('')
        await message.message.answer('Введите номер купона', reply_markup=back_button())
        await UserStates.RecCoupon_nomb_State.set()
    else:
        if message.text == 'Да':
            await message.answer('Введите номер купона', reply_markup=back_button())
            await UserStates.RecCoupon_nomb_State.set()
        elif message.text == 'Нет':
            await state.update_data(couponnomber=-1)
            calendar, step = DetailedTelegramCalendar(min_date=datetime.date(Now_year, Now_month, Now_day), locale='ru').build()
            await message.answer(f'Выберите дату, когда вы придёте\nВыберите {RER[step]}', reply_markup=calendar)
            await UserStates.CalendarChoiseState.set()
        else:
            await message.answer('Введите Да или Нет', reply_markup=back_button())
            return


async def RecordCouponnomb(message: types.Message | types.CallbackQuery, state: FSMContext):
    if Statistic.select().where(Statistic.Coupon == message.text).exists():
        await message.answer('Этот купон уже использован', reply_markup=back_button())
        return
    else:
        for i in str(message.text):
            if not i.isdigit():
                await message.answer('Введите номер купона правильно', reply_markup=back_button())
                return
    await state.update_data(couponnomber=int(message.text))
    calendar, step = DetailedTelegramCalendar(min_date=datetime.date(Now_year, Now_month, Now_day), locale='ru').build()
    await message.answer(f'Выберите дату, когда вы придёте\nВыберите {RER[step]}', reply_markup=calendar)
    await UserStates.CalendarChoiseState.set()


async def calendarchoise(query: types.CallbackQuery, state: FSMContext):
    userdata = await state.get_data()
    doc = Doctor_service.select().join(Service_info).where(Service_info.ServiceName == {userdata['ServiceName']}).get()
    serviceid = Service_info.get(Service_info.ServiceName == userdata['ServiceName'])
    result, key, step = DetailedTelegramCalendar(min_date=datetime.date(Now_year, Now_month, Now_day), locale='ru').process(query.data)
    cl_id = Client_info.select().where(Client_info.ClientTgUsername == query.from_user.username).get()
    if not result and key:
        await query.message.answer(f"Выберите {RER[step]}", reply_markup=key)
        await query.message.delete()
    elif result:
        await query.message.delete()
        Statistic.create(client_fk=cl_id.client_id,
                   service_fk=serviceid.id,
                   doctor_fk=doc.id,
                   DateOfApplication=datetime.datetime.now().strftime('%d.%m.%Y; %H:%M'),
                   Coupon=userdata['couponnomber'],
                   Status='в обработке',
                   DateOfReceipt=result,  # на когда заказан
                   ProblemDescription=userdata['Problem'])
        await query.message.answer('Ваша зявка принята, скоро с вами свяжутся.', reply_markup=main_menu())
        await query.bot.send_message(chat_id=683138076, text=f'Новая заявка от пользователя @{query.from_user.username}')
        await UserStates.user_state.set()


def register_user_handler(dp:Dispatcher):
    dp.register_message_handler(doctor_list, lambda m: m.text.startswith("Врачи"), state=UserStates.user_state)
    dp.register_message_handler(Services_t, lambda a: a.text.startswith("Услуги"), state=UserStates.user_state)
    dp.register_message_handler(Services, state=UserStates.Services_t_state)
    dp.register_message_handler(contact_list, lambda c: c.text.startswith("Контакты"), state=UserStates.user_state)
    dp.register_message_handler(record, lambda k: k.text.startswith("Запись на прием"), state=UserStates.user_state)
    dp.register_message_handler(show_doctor_list, state=UserStates.show_doctor_list_state)
    dp.register_message_handler(RecordClientFullName, state=UserStates.RecClientFullNameState)

    dp.register_message_handler(RecordClientPhoneNumber, state=UserStates.RecClientPhoneNumberState)
    dp.register_callback_query_handler(RecordClientFullName, lambda c: c.data == 'back', state=UserStates.RecClientEmail)
    dp.register_callback_query_handler(record, lambda c: c.data == 'back', state=UserStates.RecClientPhoneNumberState)
    dp.register_callback_query_handler(RecordClientPhoneNumber, lambda c: c.data == 'back', state=UserStates.RecServiceTypeState)
    dp.register_callback_query_handler(RecordClientEmail, lambda c: c.data == 'back', state=UserStates.RecServiceNameState)
    dp.register_callback_query_handler(RecordServiceType, lambda c: c.data == 'back', state=UserStates.RecProblemState)
    dp.register_callback_query_handler(RecordProblem, lambda c: c.data == 'back', state=UserStates.RecCoupon_nomb_State)
    dp.register_callback_query_handler(RecordProblem, lambda c: c.data == 'back', state=UserStates.CalendarChoiseState)
    dp.register_callback_query_handler(RecordCoupon, lambda c: c.data == 'back', state=UserStates.CalendarChoiseState)

    dp.register_message_handler(RecordClientEmail, state=UserStates.RecClientEmail)
    dp.register_message_handler(RecordServiceType, state=UserStates.RecServiceTypeState)
    dp.register_message_handler(RecordServiceName, state=UserStates.RecServiceNameState)
    dp.register_message_handler(RecordProblem, state=UserStates.RecProblemState)
    dp.register_message_handler(RecordCoupon, state=UserStates.RecCouponState)
    dp.register_message_handler(RecordCouponnomb, state=UserStates.RecCoupon_nomb_State)
    dp.register_callback_query_handler(calendarchoise, DetailedTelegramCalendar.func(), state=UserStates.CalendarChoiseState)
    # dp.register_callback_query_handler(cmd_start, lambda c: c.data == 'back', state=UserStates.RecClientFullNameState)
    # dp.register_callback_query_handler(cmd_start, lambda c: c.data == 'mainmenu', state='*')
