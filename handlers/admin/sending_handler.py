from aiogram.dispatcher import FSMContext
from peewee import SqliteDatabase
from keyboards.admin_keyboard import send_message
from peewee import *
import db
from aiogram import Dispatcher,  types
from aiogram.dispatcher.filters.state import State, StatesGroup
from handlers.states import AdminStates

class AdminSendMessageStateMachine(StatesGroup):
    admin_message_state = State()


# Подтверждение рассылки
async def accepted_message(callback_query: types.CallbackQuery, state: FSMContext):
    separated_data = callback_query.data.split(";")
    users = db.Client_info.select().dicts()
    if separated_data[1] == 'go':
        message = await state.get_data()
        message = message['message']
        for user in users:
            await message.send_copy(chat_id=user['client_id'])
    elif separated_data[1] == 'reject':
        await callback_query.message.answer(text='Рассылка отменена')
    await state.set_state(AdminStates.admin_state)


# Отправка рассылки
async def admin_send_message(message: types.Message, state: FSMContext):
    print(message.content_type)
    await state.set_data({'message': message})
    await message.send_copy(chat_id=message.chat.id, reply_markup=send_message())


async def sendings(message: types.Message, state: FSMContext):
    await message.answer("Введите сообщение, которое хотите отправить")
    await AdminSendMessageStateMachine.admin_message_state.set()


def register_sending_handlers(dp: Dispatcher):
    dp.register_message_handler(sendings, lambda m: m.text == 'Рассылка', state=AdminStates.admin_state)
    dp.register_message_handler(admin_send_message, content_types=types.ContentType.ANY,
                                state=AdminSendMessageStateMachine.admin_message_state)
    dp.register_callback_query_handler(accepted_message, lambda c: c.data.startswith('send'),
                                state=AdminSendMessageStateMachine.admin_message_state)
