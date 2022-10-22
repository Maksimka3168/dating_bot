from aiogram import types
from loader import dp
from states.users.register.states import UserRegister
from utils.admin.msg_correct import message_correct


@dp.message_handler(commands=['register', 'reg'], content_types=['text'])
async def message_commands_reg(message: types.Message):
    # Проверка зарегестрирован ли пользователь
    await message.delete()
    msg_text = await message_correct(message.from_user.id, "cmd_start_not_reg")
    await message.answer(text=msg_text, parse_mode="HTML")
    await UserRegister.user_input_name.set()

@dp.callback_query_handler(lambda c: c.data == "register")
async def callback_commands_reg(call: types.CallbackQuery):
    # Проверка зарегестрирован ли пользователь
    await call.message.delete()
    msg_text = await message_correct(call.message.chat.id, "cmd_start_not_reg")
    await call.message.answer(text=msg_text, parse_mode="HTML")
    await UserRegister.user_input_name.set()