from aiogram.dispatcher import FSMContext

from keyboard.inline_keyboard import cancel_inline
from utils.admin.msg_correct import edit_msg_admin, get_message
from states.admin.edit_msg_admin.states import AdminEditMsg
from loader import dp
from aiogram import types


@dp.callback_query_handler(edit_msg_admin.filter(), state='*')
async def edit_msg_admin_handler(call: types.CallbackQuery, callback_data: dict, state: FSMContext):
    print("Сработало")
    await call.answer()
    async with state.proxy() as data:
        data['state_previous'] = await state.get_state()
        data['msg_type'] = callback_data['msg_type']
    msg_text = await get_message(callback_data['msg_type'])
    await call.message.edit_text(
        text=f"*ИЗМЕНЕНИЕ СООБЩЕНИЯ*\n\nТекущий текст: {msg_text}\n\nВведите текст, на который вы хотите изменить текущий:",
        reply_markup=cancel_inline,
        parse_mode="Markdown")
    await AdminEditMsg.input_message.set()

