from aiogram.dispatcher.filters.state import State, StatesGroup


class UserRegister(StatesGroup):
    user_input_name = State()
    user_input_age = State()
