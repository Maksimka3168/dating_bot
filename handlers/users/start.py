from aiogram import types
from loader import dp
from utils.admin.msg_correct import message_correct


@dp.message_handler(commands=['start'], content_types=['text'])
async def message_commands_start(message: types.Message):
    # Проверка на регистрацию
    msg_text, keyboard = await message_correct(message.from_user.id, "cmd_start_not_reg")
    await message.answer(msg_text, parse_mode="HTML", reply_markup=keyboard)
