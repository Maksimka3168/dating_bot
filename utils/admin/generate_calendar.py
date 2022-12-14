import calendar
import datetime

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


class TimeNow:
    @property
    def now_time_sec(self):
        tzinfo = datetime.timezone(datetime.timedelta(hours=+6.0))
        time = datetime.datetime.now(tz=tzinfo)
        return time

    @property
    def now_time(self):
        tzinfo = datetime.timezone(datetime.timedelta(hours=+6.0))
        time = datetime.datetime.now(tz=tzinfo)
        return time.day, time.month, time.year

    def get_time_database(self):
        return self.now_time

    def get_time_user(self):
        return self.now_time_sec


t = TimeNow()

months = {
    1: "Январь",
    2: "Ферваль",
    3: "Март",
    4: "Апрель",
    5: "Май",
    6: "Июнь",
    7: "Июль",
    8: "Август",
    9: "Сентябрь",
    10: "Октябрь",
    11: "Ноябрь",
    12: "Декабрь",
}


def generate_calendar_inline(day, month, year):
    monthdays = calendar.monthrange(year, month)
    inline_keyboard = InlineKeyboardMarkup(row_width=7)
    inline_keyboard.insert(InlineKeyboardButton(text="<----", callback_data="prev_year"))
    inline_keyboard.insert(InlineKeyboardButton(text=f"{year}", callback_data="..."))
    inline_keyboard.insert(InlineKeyboardButton(text="---->", callback_data="next_year"))
    inline_keyboard.row()
    inline_keyboard.insert(InlineKeyboardButton(text="<----", callback_data="prev_month"))
    inline_keyboard.insert(InlineKeyboardButton(text=f"{months[month]}", callback_data="..."))
    inline_keyboard.insert(InlineKeyboardButton(text="---->", callback_data="next_month"))
    inline_keyboard.row()
    for d in ["Пн", "Вт", "Ср", "Чт", "Пт", "Сб", "Вс"]:
        inline_keyboard.insert(InlineKeyboardButton(text=d, callback_data="..."))
    weekday = calendar.weekday(year, month, 1)
    for i in range(0, weekday):
        inline_keyboard.insert(InlineKeyboardButton(text="-", callback_data="..."))
    for d in range(1, monthdays[1] + 1):
        if len(day) == 3:
            if (d == int(day[0])) and (month == day[1]) and (year == day[2]):
                inline_keyboard.insert(InlineKeyboardButton(text=f"✅ {d}", callback_data=f"select_{d}"))
            else:
                inline_keyboard.insert(InlineKeyboardButton(text=f"{d}", callback_data=f"select_{d}"))
        else:
            inline_keyboard.insert(InlineKeyboardButton(text=f"{d}", callback_data=f"select_{d}"))
    weekday = calendar.weekday(year, month, monthdays[1])
    for i in range(1, (7 - weekday)):
        inline_keyboard.insert(InlineKeyboardButton(text="-", callback_data="..."))
    inline_keyboard.row()
    if len(day) == 3:
        inline_keyboard.insert(InlineKeyboardButton(text=f"Вы выбрали: {day[0]}.{day[1]}.{day[2]}", callback_data="..."))
        inline_keyboard.insert(InlineKeyboardButton(text="Подтвердить", callback_data="accept"))

    return inline_keyboard


