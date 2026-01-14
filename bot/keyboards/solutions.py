from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

def solutions_kb(is_staff: bool) -> ReplyKeyboardMarkup:
    rows = []
    if is_staff:
        rows.append([KeyboardButton(text="Все решения (staff)")])
    rows.append([KeyboardButton(text="Мои решения")])
    rows.append([KeyboardButton(text="Назад")])
    return ReplyKeyboardMarkup(keyboard=rows, resize_keyboard=True)
