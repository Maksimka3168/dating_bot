from aiogram import types
from aiogram.dispatcher import FSMContext

from loader import dp
from states.users.additional_information.states import UserAdditInfo
from states.users.register.states import UserRegister
from utils.admin.msg_correct import generate_profile_register


@dp.callback_query_handler(lambda c: c.data == "cancel", state=UserRegister)
async def user_register_cancel_handler(call: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        data['msg_type'] = str(int(data['msg_type']) - 1)
        msg_text, keyboard = await generate_profile_register(call.message.chat.id,
                                                             data['msg_type'])
        data['message_id'] = await call.message.answer(text=msg_text, parse_mode="Markdown", reply_markup=keyboard)
        await call.message.delete()
        await UserRegister.previous()


@dp.callback_query_handler(lambda c: c.data in ['prev_month', 'prev_year', 'next_year', 'next_month', 'cancel'],
                           state=UserRegister.user_input_year)
async def user_register_calender_handler(call: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        if call.data == 'prev_month':
            if data['month'] == 1:
                data['month'] = 12
            else:
                data['month'] -= 1
        elif call.data == 'prev_year':
            if data['year'] > 0:
                data['year'] -= 1
        elif call.data == "next_month":
            if data['month'] == 12:
                data['month'] = 1
            else:
                data['month'] += 1
        elif call.data == "next_year":
            data['year'] += 1
        msg_text, keyboard = await generate_profile_register(call.message.chat.id,
                                                             data['msg_type'], data['day'], data['month'],
                                                             data['year'])
        await call.message.edit_text(msg_text, reply_markup=keyboard, parse_mode='Markdown')


@dp.callback_query_handler(lambda c: c.data.startswith("select_"), state=UserRegister.user_input_year)
async def user_register_calender_handler(call: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        data['select'] = [int(call.data[7:]), data['month'], data['year']]
        msg_text, keyboard = await generate_profile_register(call.message.chat.id,
                                                             data['msg_type'], data['select'], data['month'],
                                                             data['year'])
        await call.message.edit_text(text=msg_text, reply_markup=keyboard, parse_mode="Markdown")


@dp.callback_query_handler(lambda c: c.data.startswith("accept"), state=UserRegister.user_input_year)
async def user_register_calender_handler(call: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        data['msg_type'] = str(int(data['msg_type']) + 1)
        data['dict_user_data']["birthdate"] = {
            "day": data['select'][0],
            "month": data['select'][1],
            "year": data['select'][2]
        }
        msg_text, keyboard = await generate_profile_register(call.message.chat.id, data['msg_type'])
        await call.message.edit_text(text=msg_text, parse_mode="Markdown", reply_markup=keyboard)
        await UserRegister.user_input_gender.set()


@dp.callback_query_handler(state=UserRegister.user_input_gender)
async def user_register_input_gender_handler(call: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        data['msg_type'] = str(int(data['msg_type']) + 1)
        data['dict_user_data']["gender"] = call.data
        msg_text, keyboard = await generate_profile_register(call.message.chat.id,
                                                             data['msg_type'])
        data['message_id'] = await call.message.edit_text(text=msg_text, parse_mode="Markdown", reply_markup=keyboard)
        await UserRegister.user_input_name.set()


@dp.message_handler(state=UserRegister.user_input_name, content_types=['text'])
async def user_register_input_name_handler(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        await message.delete()
        data['msg_type'] = str(int(data['msg_type']) + 1)
        data['dict_user_data']["name"] = message.text  # Проверка имени
        msg_text, keyboard = await generate_profile_register(message.from_user.id, data['msg_type'])
        await data['message_id'].edit_text(text=msg_text, reply_markup=keyboard,
                                           parse_mode="Markdown")
        await UserRegister.user_accept_rule.set()


@dp.callback_query_handler(state=UserRegister.user_accept_rule)
async def user_register_accept_year_handler(call: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        data['msg_type'] = str(int(data['msg_type']) + 1)
        msg_text, keyboard = await generate_profile_register(call.message.chat.id,
                                                             data['msg_type'])
        await call.message.delete()
        data['message_id'] = await call.message.answer(text=msg_text, parse_mode="Markdown", reply_markup=keyboard)
        data['previous_type'] = "register"
        await UserAdditInfo.input_height.set()  # Переход на доп условия

# @dp.message_handler(state=UserRegister.user_get_location, content_types=['location'])
# async def user_register_get_location_handler(message: types.Message, state: FSMContext):
#     async with state.proxy() as data:
#         if message.location:
#             await data['message_id'].delete()
#             data['msg_type'] = str(int(data['msg_type']) + 1)
#             msg_text, keyboard = await generate_profile_register(message.from_user.id, data['msg_type'],
#                                                                  message.location.latitude, message.location.longitude)
#             data['message_id'] = await message.answer(text=msg_text, reply_markup=keyboard, parse_mode="Markdown")
#             await UserRegister.user_accept_location.set()
#         else:
#             pass
#
#
# @dp.message_handler(lambda message: message.text == "Назад", state=UserRegister.user_get_location,
#                     content_types=['text'])
# async def user_register_cancel_handler(message: types.Message, state: FSMContext):
#     async with state.proxy() as data:
#         data['msg_type'] = str(int(data['msg_type']) - 1)
#         msg_text, keyboard = await generate_profile_register(message.from_user.id,
#                                                              data['msg_type'])
#         await data['message_id'].delete()
#         await message.answer(text=msg_text, parse_mode="Markdown", reply_markup=keyboard)
#         await message.delete()
#         await UserRegister.previous()


# @dp.callback_query_handler(state=UserRegister.user_accept_location)
# async def user_register_accept_location_handler(call: types.CallbackQuery, state: FSMContext):
#     async with state.proxy() as data:
#         data['msg_type'] = str(int(data['msg_type']) + 1)
#         # msg_text, keyboard = await generate_profile_register(call.message.chat.id, data['msg_type'])
#         # data['message_id'] = await call.message.edit_text(text=msg_text, reply_markup=keyboard, parse_mode="Markdown")
#         # ----------------------------
#         data['message_id'] = await call.message.edit_text(text, reply_markup=keyboard, parse_mode='Markdown')
#         await UserRegister.user_input_year.set()
