from config import token
import logging
from handlers.states import AdminStates
from keyboards.user_keybords import main_menu
from handlers.user.user_handler import UserStates
from handlers.admin.edit_info_handler import register_editing_handler
from handlers.user.user_handler import register_user_handler
from handlers.admin.admin_handler import register_admin_handler
from handlers.admin.delete_doctor_handler import register_delete_handler
from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from keyboards.admin_keyboard import admin_keyboard
from handlers.admin.sending_handler import register_sending_handlers

logging.basicConfig(level=logging.DEBUG)

bot = Bot(token=token)
dp = Dispatcher(bot, storage=MemoryStorage())
dp.middleware.setup(LoggingMiddleware())




@dp.message_handler(commands=['start'], state="*")
async def cmd_start(message: types.Message):
    await message.answer('Привет, тут должно быть описание но его пока нет ', reply_markup=main_menu())
    await UserStates.user_state.set()


@dp.callback_query_handler(lambda c: c.data == 'mainmenu', state="*")
async def cmd_start(query: types.CallbackQuery):
    await query.message.answer('Привет, тут должно быть описание но его пока нет ', reply_markup=main_menu())
    await UserStates.user_state.set()

@dp.message_handler(commands=['admin'])
async def cmd_admin(message:types.Message):
    user_id = message.from_user.id
    id_admin = [934752610, 683138076]
    if user_id in id_admin:
        await message.answer('Панель админа', reply_markup=admin_keyboard())
        await AdminStates.admin_state.set()

if __name__ == '__main__':
    register_user_handler(dp)
    register_admin_handler(dp)
    register_delete_handler(dp)
    register_editing_handler(dp)
    register_sending_handlers(dp)
    executor.start_polling(dp, skip_updates=True)



