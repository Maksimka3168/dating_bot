from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

cancel_inline = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Назад", callback_data="cancel")
        ]
    ]
)