from aiogram.dispatcher.filters.state import State, StatesGroup


class UserRegister(StatesGroup):
    # Основная регистрация
    user_input_year = State()  # Ввод даты рождения
    user_input_gender = State()  # Ввод пола
    user_input_name = State()  # Ввод имени
    user_accept_rule = State()  # Согласие с правилами проекта
    # user_get_location = State()  # Получение геолокации
    # user_accept_location = State()  # Подтверждение геолокации
    # Доп. информация в другом классе стейтов
