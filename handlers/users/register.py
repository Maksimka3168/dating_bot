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
            "gender": "",
            "accept_year": "",
            "location": "",
            "year": "",
            "name": ""
        }
        await message.delete()
        msg_text, keyboard = await generate_profile_register(message.from_user.id,
                                                             "cmd_register_step_1")
        await message.answer(text=msg_text, parse_mode="HTML", reply_markup=keyboard)
        await UserRegister.user_input_gender.set()


@dp.callback_query_handler(lambda c: c.data == "register")
async def callback_commands_reg(call: types.CallbackQuery, state: FSMContext):
    # Проверка зарегестрирован ли пользователь
    async with state.proxy() as data:
        data['dict_user_data'] = {
            "gender": "",
            "accept_year": "",
            "location": "",
            "year": "",
            "name": ""
        }
        await call.message.delete()
        msg_text, keyboard = await generate_profile_register(call.message.chat.id,
                                                             "cmd_register_step_1")
        await call.message.answer(text=msg_text, parse_mode="HTML", reply_markup=keyboard)
        await UserRegister.user_input_gender.set()
