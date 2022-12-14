from aiogram import types
from loader import dp
from utils.admin.msg_correct import generate_profile_register


@dp.message_handler(commands=['start'], content_types=['text'])
async def message_commands_start(message: types.Message):
    # Проверка на регистрацию
    msg_text, keyboard = await generate_profile_register(message.from_user.id, "cmd_start_not_reg")
    await message.answer(msg_text, parse_mode="Markdown", reply_markup=keyboard)
