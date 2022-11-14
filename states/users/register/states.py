from aiogram.dispatcher.filters.state import State, StatesGroup


class UserRegister(StatesGroup):
    # Основная регистрация
    user_input_gender = State()
    user_accept_year = State()
    user_get_location = State()
    user_accept_location = State()
    user_input_year = State()
    user_input_name = State()
    # Дополнительные данные


