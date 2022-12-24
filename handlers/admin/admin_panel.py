from aiogram import types
from aiogram.dispatcher import FSMContext

from loader import dp
from database.db import Database

db = Database('database/db.db')

@dp.message_handler(commands=['/admin'])
async def admin_panel_start_handler(message: types.Message, state: FSMContext):
    pass