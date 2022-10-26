from aiogram.dispatcher.filters.state import State, StatesGroup


class AdminEditMsg(StatesGroup):
    input_message = State()
    accept_input = State()
    error_state = State()
