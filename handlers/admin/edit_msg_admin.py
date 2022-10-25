from aiogram.dispatcher import FSMContext

from utils.admin.msg_correct import edit_msg_admin
from loader import dp
from aiogram import types

@dp.callback_query_handler(edit_msg_admin.filter())
async def edit_msg_admin_handler(call: types.CallbackQuery, callback_data: dict, state: FSMContext):
    msg_type = callback_data['msg_type']
    state_current = state.get_state()
    print(msg_type)
    print(state_current)

