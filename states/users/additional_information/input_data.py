from aiogram import types
from aiogram.dispatcher import FSMContext

from loader import dp
from states.users.additional_information.states import UserAdditInfo
from states.users.register.states import UserRegister
from utils.admin.msg_correct import generate_profile_register


@dp.callback_query_handler(lambda c: c.data == "cancel", state=UserAdditInfo)
async def user_addit_info_cancel_handler(call: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        data['msg_type'] = str(int(data['msg_type']) - 1)
        if data['previous_type'] == "register":  # Если user попал в этот модуль из регистрации
            msg_text, keyboard = await generate_profile_register(call.message.chat.id,
                                                                 data['msg_type'])
            data['message_id'] = await call.message.answer(text=msg_text, parse_mode="HTML", reply_markup=keyboard)
            await call.message.delete()
            if data['msg_type'] == "6":
                await UserRegister.user_input_name.set()
            else:
                await UserAdditInfo.previous()
        else:  # Если user попал в этот модуль при дозаполнении своей формы
            pass


@dp.message_handler(state=UserAdditInfo.input_height)
async def user_addit_info_input_height_handler(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['msg_type'] = str(int(data['msg_type']) + 1)
        data['dict_user_data']["height"] = message.text
        msg_text, keyboard = await generate_profile_register(message.from_user.id, data['msg_type'])
        await data['message_id'].delete()
        data['message_id'] = await message.answer(text=msg_text, reply_markup=keyboard, parse_mode="HTML")
        await message.delete()
        await UserAdditInfo.input_weight.set()


@dp.message_handler(state=UserAdditInfo.input_weight)
async def user_addit_info_input_weight_handler(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['msg_type'] = str(int(data['msg_type']) + 1)
        data['dict_user_data']["weight"] = message.text
        msg_text, keyboard = await generate_profile_register(message.from_user.id, data['msg_type'])
        await data['message_id'].delete()
        data['message_id'] = await message.answer(text=msg_text, reply_markup=keyboard, parse_mode="HTML")
        await message.delete()
        await UserAdditInfo.input_hair_color.set()


@dp.callback_query_handler(state=UserAdditInfo.input_hair_color)
async def user_addit_info_input_hair_color_handler(call: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        data['msg_type'] = str(int(data['msg_type']) + 1)
        data['dict_user_data']["hair_color"] = call.data
        msg_text, keyboard = await generate_profile_register(call.message.chat.id, data['msg_type'])
        await call.message.edit_text(text=msg_text, reply_markup=keyboard, parse_mode="HTML")
        await UserAdditInfo.input_the_type.set()


@dp.callback_query_handler(state=UserAdditInfo.input_the_type)
async def user_addit_info_input_the_type_handler(call: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        # data['msg_type'] = str(int(data['msg_type']) + 1)
        # msg_text, keyboard = await generate_profile_register(message.from_user.id, data['msg_type'])
        # data['message_id'] = await message.answer(text=msg_text, reply_markup=keyboard, parse_mode="HTML")
        data['dict_user_data']["type"] = call.data
        await call.message.edit_text(text="На этом регистрация закончена")
        print(data['dict_user_data'])
        await state.finish()
