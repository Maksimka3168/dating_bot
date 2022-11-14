from typing import Union

from config import admins
from database.db import Database
from aiogram import types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.callback_data import CallbackData

from utils.users.register.get_address import get_address

edit_msg_admin = CallbackData("edit_msg", "msg_type")

db = Database('database/db.db')

msg_ids_dict = {
    "cmd_start_not_reg": "r_1",  # Если пользователь не зарегестрирован
    "cmd_start_reg": "r_2",  # Если пользователь зарегестрирован
    "cmd_register_step_1": "r_3",  # Первый шаг регистрации(выбор пола)
    "cmd_register_step_2": "r_4",  # Второй шаг регистрации(подтверждение года)
    "cmd_register_step_3": "r_5",  # Третий шаг регистрации(получение геолокации)
    "cmd_register_step_4": "r_6",  # Четвёртый шаг регистрации(подтверждение геолокации)
    "cmd_register_step_5": "r_7",  # Пятый шаг регистрации(ввод возраста)
    "cmd_register_step_6": "r_8",  # Шестой шаг регистрации(ввод имени)
    "err_1": "e_1",  # Ошибка №1
}


async def generate_keyboard_message(user_id: int, msg_type: str) -> ReplyKeyboardMarkup | InlineKeyboardMarkup:
    keyboard_inline = InlineKeyboardMarkup()
    keyboard_text = ReplyKeyboardMarkup()
    if msg_type == "cmd_start_not_reg":
        keyboard_inline.add(InlineKeyboardButton(text="Зарегестрироваться", callback_data="register"))
    elif msg_type == "cmd_register_step_1":
        keyboard_inline.insert(InlineKeyboardButton(text="М", callback_data="male"))
        keyboard_inline.insert(InlineKeyboardButton(text="Ж", callback_data="female"))
        keyboard_inline.add(InlineKeyboardButton(text="Отменить регистрацию", callback_data="stop_register"))
    elif msg_type == "cmd_register_step_2":
        keyboard_inline.insert(InlineKeyboardButton(text="Да, подтверждаю", callback_data="accept"))
        keyboard_inline.insert(InlineKeyboardButton(text="сомневаюсь", callback_data="doubt"))
        keyboard_inline.add(InlineKeyboardButton(text="Правила", callback_data="rule"))
        keyboard_inline.add(InlineKeyboardButton(text="Назад", callback_data="cancel"))
    elif msg_type == "cmd_register_step_3":
        keyboard_text.add(KeyboardButton(text="Поделиться геолокацией", request_location=True))
        keyboard_text.add(KeyboardButton(text="Назад"))
        return keyboard_text
    elif msg_type == "cmd_register_step_4":
        keyboard_inline.insert(InlineKeyboardButton(text="Всё верно!", callback_data="accept"))
        keyboard_inline.insert(InlineKeyboardButton(text="Переопределить", callback_data="update"))
        keyboard_inline.add(InlineKeyboardButton(text="Назад", callback_data="cancel"))
    elif msg_type == "cmd_register_step_5":
        keyboard_inline.add(InlineKeyboardButton(text="Назад", callback_data="cancel"))
    elif msg_type == "cmd_register_step_6":
        keyboard_inline.add(InlineKeyboardButton(text="Назад", callback_data="cancel"))
    elif msg_type == "cmd_register_step_7":
        keyboard_inline.add(InlineKeyboardButton(text="Назад", callback_data="cancel"))
    elif msg_type == "cmd_register_step_8":
        keyboard_inline.add(InlineKeyboardButton(text="Назад", callback_data="cancel"))
    elif msg_type == "err_1":
        keyboard_inline.add(InlineKeyboardButton(text="Назад", callback_data="cancel"))
    if user_id in admins:
        keyboard_inline.add(InlineKeyboardButton(text="Изменить текст сообщения(for admin)", callback_data=edit_msg_admin.new(
            f"{msg_type}"
        )))
    return keyboard_inline


async def get_message(msg_type: str) -> str:
    """
    Данная функция получает и обрабатывает отправляемый текст пользователю из базы данных.

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
        return msg_text + f"\n\n<i>msg_id: {msg_ids_dict[msg_type]}</i>", keyboard
    else:
        return msg_text, keyboard


async def generate_profile_register(user_id: int, msg_type: str, *qwarks):
    """
    Данная функция генерирует профиль пользователя при регситрации
    :param msg_type: тип сообщения
    :param user_id:  user_id пользователя
    :param user_info: информация о пользователе (словарь)
    :return: string, профиль пользователя
    """
    msg_text = await get_message(msg_type)
    keyboard = await generate_keyboard_message(user_id, msg_type)
    if msg_type == "cmd_register_step_4":
        address_msg = await get_address(qwarks[0], qwarks[1])
        msg_text += "\n\n" + address_msg
    if user_id in admins:
        return msg_text + f"\n\n<i>msg_id: {msg_ids_dict[msg_type]}</i>", keyboard
    else:
        return msg_text, keyboard
