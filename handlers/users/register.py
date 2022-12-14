from aiogram import types
from aiogram.dispatcher import FSMContext

from loader import dp
from states.users.register.states import UserRegister
from utils.admin.msg_correct import generate_profile_register


@dp.message_handler(commands=['register', 'reg'], content_types=['text'])
async def message_commands_reg(message: types.Message, state: FSMContext):
    # Проверка зарегестрирован ли пользователь
    async with state.proxy() as data:
        data['msg_type'] = "1"
        data['dict_user_data'] = {
            # Основная регистрация
            "birthdate": "",
            "gender": "",
            "name": "",
            "number_phone": "NULL",  # Вытягиваем из данных пользователя
            # Дополнительные данные
            "height": "",
            "weight": "",
            "hair_color": "",
            "type": ""

        }
        await message.delete()
        data['day'], data['month'], data['year'] = [], 1, 2000
        msg_text, keyboard = await generate_profile_register(message.from_user.id,
                                                             data['msg_type'], data['day'], data['month'], data['year'])
        await message.answer(text=msg_text, parse_mode="Markdown", reply_markup=keyboard)
        await UserRegister.user_input_year.set()


@dp.callback_query_handler(lambda c: c.data == "register")
async def callback_commands_reg(call: types.CallbackQuery, state: FSMContext):
    # Проверка зарегестрирован ли пользователь
    async with state.proxy() as data:
        data['msg_type'] = "1"
        data['dict_user_data'] = {
            # Основная регистрация
            "birthdate": "",
            "gender": "",
            "name": "",
            "number_phone": "NULL",  # Вытягиваем из данных пользователя
            # Дополнительные данные
            "height": "",
            "weight": "",
            "hair_color": "",
            "type": ""
        }
        await call.message.delete()
        data['day'], data['month'], data['year'] = [], 1, 2000
        msg_text, keyboard = await generate_profile_register(call.message.chat.id,
                                                             data['msg_type'], data['day'], data['month'], data['year'])
        await call.message.answer(text=msg_text, parse_mode="Markdown", reply_markup=keyboard)
        await UserRegister.user_input_year.set()
