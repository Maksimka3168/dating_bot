from aiogram import types
from aiogram.dispatcher import FSMContext

from loader import dp
from states.users.register.states import UserRegister
from utils.admin.msg_correct import message_correct, generate_profile_register


@dp.callback_query_handler(state=UserRegister.user_input_name)
async def user_register_input_name_callback_handler(call: types.CallbackQuery, state: FSMContext):
    if call.data == "stop_register":
        await call.message.edit_text("Вы успешно отменили регистрацию!")
        await state.finish()


@dp.message_handler(state=UserRegister.user_input_name, content_types=['text'])
async def user_register_input_message_handler(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        if len(message.text.split(" ")) == 3:
            data['dict_user_data']["full_name"] = message.text.split(" ")
            msg_text, keyboard = await generate_profile_register(message.from_user.id, data['dict_user_data'],
                                                                 "cmd_register_step_2")
            await UserRegister.user_input_age.set()
        else:
            msg_text, keyboard = await message_correct(message.from_user.id, "err_1")
        await message.delete()
        data['message_id'] = await data['message_id'].edit_text(text=msg_text, reply_markup=keyboard, parse_mode="HTML")


@dp.callback_query_handler(state=UserRegister.user_input_age)
async def user_register_input_age_call_handler(call: types.CallbackQuery, state: FSMContext):
    if call.data == "cancel":
        pass


@dp.message_handler(state=UserRegister.user_input_age, content_types=['text'])
async def user_register_input_age_message_handler(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        try:
            data['dict_user_data']['age'] = int(message.text)
        except:
            pass
