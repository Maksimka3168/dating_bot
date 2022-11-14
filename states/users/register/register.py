from aiogram import types
from aiogram.dispatcher import FSMContext

from loader import dp
from states.users.register.states import UserRegister
from utils.admin.msg_correct import generate_profile_register
from utils.users.register.get_address import get_address


@dp.callback_query_handler(state=UserRegister.user_input_gender)
async def user_register_input_gender_handler(call: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        msg_text, keyboard = await generate_profile_register(call.message.chat.id,
                                                             "cmd_register_step_2")
        await call.message.edit_text(text=msg_text, parse_mode="HTML", reply_markup=keyboard)
        await UserRegister.user_accept_year.set()


@dp.callback_query_handler(state=UserRegister.user_accept_year)
async def user_register_accept_year_handler(call: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        msg_text, keyboard = await generate_profile_register(call.message.chat.id,
                                                             "cmd_register_step_3")
        await call.message.delete()
        data['message_id'] = await call.message.answer(text=msg_text, parse_mode="HTML", reply_markup=keyboard)
        await UserRegister.user_get_location.set()


@dp.message_handler(state=UserRegister.user_get_location, content_types=['location', 'text'])
async def user_register_get_location_handler(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        if message.location:
            await data['message_id'].delete()
            msg_text, keyboard = await generate_profile_register(message.from_user.id, "cmd_register_step_4", message.location.latitude, message.location.longitude)
            await message.answer(text=msg_text, reply_markup=keyboard, parse_mode="HTML")
            await UserRegister.user_accept_location.set()
        else:
            pass


@dp.callback_query_handler(state=UserRegister.user_accept_location)
async def user_register_accept_location_handler(call: types.CallbackQuery, state: FSMContext):
    pass
