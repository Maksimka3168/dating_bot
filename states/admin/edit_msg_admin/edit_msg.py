from aiogram import types
from aiogram.dispatcher import FSMContext

from keyboard.inline_keyboard import cancel_inline
from loader import dp
from states.admin.edit_msg_admin.states import AdminEditMsg
from utils.admin.msg_correct import generate_profile_register, message_correct


@dp.callback_query_handler(state=AdminEditMsg.input_message)
async def admin_edit_input_call_handler(call: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        if call.data == "cancel":
            if data['msg_type'].startswith("cmd_register"):
                try:
                    msg_text, keyboard = await generate_profile_register(call.message.from_user.id, data['user_info'],
                                                                         data['msg_type'])
                    await call.message.edit_text(text=msg_text, reply_markup=keyboard)
                    await state.set_state(data['state_previous'])
                except Exception as error:
                    print(error)
                    msg_text = "Произошла ошибка при получении предыдущего сообщения, вы были перенаправлены на стандартный ответ."
                    await call.message.edit_text(text=msg_text)
                    await state.finish()
            else:
                try:
                    msg_text, keyboard = await message_correct(call.message.from_user.id, data['msg_type'])
                    await call.message.edit_text(text=msg_text, reply_markup=keyboard)
                    await state.set_state(data['state_previous'])
                except Exception as error:
                    print(error)
                    msg_text = "Произошла ошибка при получении предыдущего сообщения, вы были перенаправлены на стандартный ответ."
                    await call.message.edit_text(text=msg_text)
                    await state.finish()


@dp.message_handler(state=AdminEditMsg.input_message)
async def admin_edit_input_msg_handler(message: types.Message, state: FSMContext):
    pass
