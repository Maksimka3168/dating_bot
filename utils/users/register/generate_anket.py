async def generate_profile_user_register(step: str, msg_data: dict) -> str:
    """
    Данная функция формирует анкету по данным, введёнными пользователем, для удобного просмотра и редактирования
    :param step: Этап прохождения регистрации
    :param msg_data: Данные введённые пользотвалем
    :return: string, отформатированная анкета пользователя
    """
    text = ""
    if step == "start":
        text = """
*АНКЕТА ПОЛЬЗОВАТЕЛЯ*

Введите ФИО:
(Пример: Зубов Павел Павлович)
"""
    if step == "input_name":
        text = f"""
*АНКЕТА ПОЛЬЗОВАТЕЛЯ*

Введённые параметры:

Фамилия: {msg_data["full_name"][0]} 
Имя: {msg_data["full_name"][1]}
Отчество: {msg_data["full_name"][2]}

Введите свой возраст:
(Пример: 25)
"""
    elif step == "input_age":
        text = f"""
        *АНКЕТА ПОЛЬЗОВАТЕЛЯ*

        Введённые параметры:

        Фамилия: {msg_data["full_name"][0]} 
        Имя: {msg_data["full_name"][1]}
        Отчество: {msg_data["full_name"][2]}
        Возраст: {msg_data["age"]}

        Введите свой возраст:
        (Пример: 25)
        """
    return text
