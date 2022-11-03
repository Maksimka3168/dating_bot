from aiogram import types
from aiogram.dispatcher import FSMContext

from loader import dp
from states.users.register.states import UserRegister
from utils.admin.msg_correct import message_correct, generate_profile_register


@dp.message_handler(commands=['register', 'reg'], content_types=['text'])
async def message_commands_reg(message: types.Message, state: FSMContext):
    # Проверка зарегестрирован ли пользователь
    async with state.proxy() as data:
        data['dict_user_data'] = {
            "full_name": [None, None, None],
            "age": None,
        }
        await message.delete()
        msg_text, keyboard = await generate_profile_register(message.from_user.id, data['dict_user_data'],
                                                             "cmd_register_step_1")
        data['message_id'] = await message.answer(text=msg_text, parse_mode="HTML", reply_markup=keyboard)
        await UserRegister.user_input_name.set()


@dp.callback_query_handler(lambda c: c.data == "register")
async def callback_commands_reg(call: types.CallbackQuery, state: FSMContext):
    # Проверка зарегестрирован ли пользователь
    async with state.proxy() as data:
        data['dict_user_data'] = {
            "full_name": ["-", "-", "-"],
            "age": "-",
        }
        await call.message.delete()
        msg_text, keyboard = await generate_profile_register(call.message.chat.id, data['dict_user_data'],
                                                             "cmd_register_step_1")
        data['message_id'] = await call.message.answer(text=msg_text, parse_mode="HTML", reply_markup=keyboard)
        await UserRegister.user_input_name.set()
