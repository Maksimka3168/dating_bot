from config import admins

msg_ids_dict = {
    "cmd_start_not_reg": "r_1",
    "cmd_start_reg": "r_2",
    "cmd_register_step_1": "r_3",
    "cmd_register_step_2": "r_4",
    "err_1": "e_1",
}


async def get_message(msg_type: str) -> str:
    """
    Данная функция получает отправляемый текст пользователю из базы данных.

    :param msg_type: тип сообщения
    :return: string, отправляемый текст
    """
    # Процесс получения текста
    message_text = "Пример отправляемого текста!"
    return message_text


async def message_correct(user_id: int, msg_type: str):
    """
    Данная функция обрабаывает сообщения для обычного пользователя и для администратора, добавляя айди сообщения.
    :param user_id: user_id пользователя
    :param msg_type: тип сообщения
    :return: string, обработанный текст
    """
    msg_text = await get_message(msg_type)
    if user_id in admins:
        return msg_text + f"\n\n<i>msg_id: {msg_ids_dict[msg_type]}</i>\n<i><s>Видно только администраторам</s></i>"
    else:
        return msg_text
