from aiogram.dispatcher.filters.state import State, StatesGroup


class UserAdditInfo(StatesGroup):
    # Дополнительная информация(Пока что для всех, потом будет разеделение на М и Ж)
    input_height = State()  # Рост
    input_weight = State()  # Вес
    input_hair_color = State()  # Цвет волос
    input_the_type = State()  # Типаж
