from aiogram import Dispatcher, Bot
from aiogram.contrib.fsm_storage.memory import MemoryStorage

import logging

import config

logging.basicConfig(level="WARNING")
logger = logging.getLogger()
bot_method = Bot(config.TELEGRAM_BOT_TOKEN)
dp = Dispatcher(bot_method, storage=MemoryStorage())


