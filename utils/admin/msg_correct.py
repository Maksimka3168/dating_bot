from config import admins
from database.db import Database
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup
from aiogram.utils.callback_data import CallbackData
from aiogram.utils.markdown import escape_md

from utils.admin.generate_calendar import generate_calendar_inline

edit_msg_admin = CallbackData("edit_msg", "msg_type")

db = Database('database/db.db')

msg_ids_dict = {
    # Основные текстовые команды
    "cmd_start_not_reg": "r_1",  # Если пользователь не зарегестрирован
    "cmd_start_reg": "r_2",  # Если пользователь зарегестрирован
    # Основная регистрация
    "1": "r_3",  # Пятый шаг регистрации(ввод возраста)
    "2": "r_4",  # Первый шаг регистрации(выбор пола)
    "3": "r_5",  # Шестой шаг регистрации(ввод имени)
    "4": "r_6",  # Второй шаг регистрации(подтверждение правил)
    # Дополнительные данные
    "5": "r_7",  # Первый шаг ввода доп. данных(рост)
    "6": "r_8",  # Первый шаг ввода доп. данных(вес)
    "7": "r_9",  # Первый шаг ввода доп. данных(цвет волос)
    "8": "r_10",  # Первый шаг ввода доп. данных(типаж)
    # Ошибки
    "err_1": "e_1",  # Ошибка №1
}

async def generate_keyboard_message(user_id: int, msg_type: str, *qwargs) -> ReplyKeyboardMarkup | InlineKeyboardMarkup:
    keyboard_inline = InlineKeyboardMarkup()
    keyboard_text = ReplyKeyboardMarkup()
    if msg_type == "cmd_start_not_reg":
        keyboard_inline.add(InlineKeyboardButton(text="Зарегестрироваться", callback_data="register"))
    elif msg_type == "1":
        keyboard_inline = generate_calendar_inline(qwargs[0], qwargs[1], qwargs[2])
    elif msg_type == "2":
        keyboard_inline.insert(InlineKeyboardButton(text="М", callback_data="male"))
        keyboard_inline.insert(InlineKeyboardButton(text="Ж", callback_data="female"))
    elif msg_type == "3":
        keyboard_inline.add(InlineKeyboardButton(text="Назад", callback_data="cancel"))
    elif msg_type == "4":
        keyboard_inline.add(InlineKeyboardButton(text="Согласен", callback_data="accept"))
        keyboard_inline.add(InlineKeyboardButton(text="Правила", callback_data="rule"))
        keyboard_inline.add(InlineKeyboardButton(text="Назад", callback_data="cancel"))
    elif msg_type == "5":
        keyboard_inline.add(InlineKeyboardButton(text="Назад", callback_data="cancel"))
    elif msg_type == "6":
        keyboard_inline.add(InlineKeyboardButton(text="Назад", callback_data="cancel"))
    elif msg_type == "7":
        keyboard_inline.add(InlineKeyboardButton(text="Назад", callback_data="cancel"))
    elif msg_type == "8":
        keyboard_inline.add(InlineKeyboardButton(text="Назад", callback_data="cancel"))
    elif msg_type == "9":
        keyboard_inline.add(InlineKeyboardButton(text="Назад", callback_data="cancel"))
    elif msg_type == "10":
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
        return msg_text + f"\n\n{escape_md(f'msg_id: {msg_ids_dict[msg_type]}')}", keyboard
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
    keyboard = await generate_keyboard_message(user_id, msg_type, *qwarks)
    if user_id in admins:
        return msg_text + f"\n\n{escape_md(f'msg_id: {msg_ids_dict[msg_type]}')}", keyboard
    else:
        return msg_text, keyboard
