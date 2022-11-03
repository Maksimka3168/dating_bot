from typing import Union

from config import admins
from database.db import Database
from aiogram import types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData

edit_msg_admin = CallbackData("edit_msg", "msg_type")

db = Database('database/db.db')

msg_ids_dict = {
    "cmd_start_not_reg": "r_1",  # Если пользователь не зарегестрирован
    "cmd_start_reg": "r_2",  # Если пользователь зарегестрирован
    "cmd_register_step_1": "r_3",  # Первый шаг регистрации(ввод имени)
    "cmd_register_step_2": "r_4",  # Второй шаг регистрации(ввод возраста)
    "err_1": "e_1",  # Ошибка №1 (при неправильном вводе ФИО)
}


async def generate_keyboard_message(user_id: int, msg_type: str) -> types.InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup()
    if msg_type == "cmd_start_not_reg":
        keyboard.add(InlineKeyboardButton(text="Зарегестрироваться", callback_data="register"))
    elif msg_type == "cmd_register_step_1":
        keyboard.add(InlineKeyboardButton(text="Отменить регистрацию", callback_data="stop_register"))
    elif msg_type == "cmd_register_step_2":
        keyboard.add(InlineKeyboardButton(text="Назад", callback_data="cancel"))
    elif msg_type == "err_1":
        keyboard.add(InlineKeyboardButton(text="Назад", callback_data="cancel"))
    if user_id in admins:
        keyboard.add(InlineKeyboardButton(text="Изменить текст сообщения(for admin)", callback_data=edit_msg_admin.new(
            f"{msg_type}"
        )))
    return keyboard


async def get_message(msg_type: str) -> str:
    """
    Данная функция получает отправляемый текст пользователю из базы данных.

    :param msg_type: тип сообщения
    :return: string, отправляемый текст
    """
    message_text = db.get_message_text(msg_type)
    if message_text is None:
        return "Произошла ошибка при получении текста!"
    return message_text


async def message_correct(user_id: int, msg_type: str):
    """
    Данная функция обрабаывает сообщения для обычного пользователя и для администратора, добавляя айди сообщения.
    :param user_id: user_id пользователя
    :param msg_type: тип сообщения
    :return: string, обработанный текст
    """
    msg_text = await get_message(msg_type)
    keyboard = await generate_keyboard_message(user_id, msg_type)
    if user_id in admins:
        return msg_text + f"\n\n<i>msg_id: {msg_ids_dict[msg_type]}</i>\n<i><s>Видно только администраторам</s></i>", keyboard
    else:
        return msg_text, keyboard


async def generate_profile_register(user_id: int, user_info: dict, msg_type: str):
    """
    Данная функция генерирует профиль пользователя при регситрации
    :param msg_type: тип сообщения
    :param user_id:  user_id пользователя
    :param user_info: информация о пользователе (словарь)
    :return: string, профиль пользователя
    """
    msg_text = await get_message(msg_type)
    keyboard_1 = await generate_keyboard_message(user_id, msg_type)
    keyboard = InlineKeyboardMarkup()
    keyboard.add(InlineKeyboardButton(text="Введённые данные:", callback_data="..."))
    for key in user_info:
        if key == "full_name":
            if user_info[key][0] is not None and user_info[key] is not None and user_info[key] is not None:
                keyboard.row()
                keyboard.insert(InlineKeyboardButton(text="Фамилия: ", callback_data="..."))
                keyboard.insert(InlineKeyboardButton(text=user_info[key][0], callback_data="..."))
                keyboard.row()
                keyboard.insert(InlineKeyboardButton(text="Имя: ", callback_data="..."))
                keyboard.insert(InlineKeyboardButton(text=user_info[key][1], callback_data="..."))
                keyboard.row()
                keyboard.insert(InlineKeyboardButton(text="Отчество: ", callback_data="..."))
                keyboard.insert(InlineKeyboardButton(text=user_info[key][2], callback_data="..."))
                keyboard.row()
            elif key == "age":
                if user_info[key] is not None:
                    keyboard.insert(InlineKeyboardButton(text="Возраст", callback_data="..."))
                    keyboard.insert(InlineKeyboardButton(text=user_info[key], callback_data="..."))
    if len(keyboard.inline_keyboard) == 1:
        keyboard.add(InlineKeyboardButton(text="Пусто", callback_data="..."))
    for key in keyboard_1.inline_keyboard:
        keyboard.add(InlineKeyboardButton(text=key[0]['text'], callback_data=key[0]['callback_data']))
    if user_id in admins:
        return msg_text + f"\n\n<i>msg_id: {msg_ids_dict[msg_type]}</i>\n<i><s>Видно только администраторам</s></i>", keyboard
    else:
        return msg_text, keyboard
