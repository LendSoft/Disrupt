from aiogram import Router, F
from aiogram.types import Message

from bot.keyboards.common import main_menu_kb
from bot.keyboards.solutions import solutions_kb
from bot.decorators.access import mod_or_admin

router = Router()

@router.message(F.text == "Решения")
async def solutions_menu(message: Message, role, **_):
    is_staff = role.is_admin or role.is_moderator
    await message.answer("Выберите режим просмотра:", reply_markup=solutions_kb(is_staff=is_staff))

@router.message(F.text == "Назад")
async def back(message: Message, role, **_):
    await message.answer("Главное меню.", reply_markup=main_menu_kb(is_admin=role.is_admin))

@router.message(F.text == "Мои решения")
async def my_solutions(message: Message, db, **_):
    rows = await db.list_my_solutions(message.from_user.id)
    if not rows:
        await message.answer("Пока нет решений.")
        return

    # без таблиц, чтобы не раздувать вывод
    for r in rows[-10:]:
        await message.answer(
            f"Раунд #{r['round_id']} | этап: {r['stage']}\n"
            f"Оценка: {r['score']}/10\n\n"
            f"Решение:\n{r['text']}\n\n"
            f"Отчет:\n{r['gigachat_report']}"
        )

@router.message(F.text == "Все решения (staff)")
@mod_or_admin
async def all_solutions(message: Message, db, **_):
    rows = await db.list_all_solutions()
    if not rows:
        await message.answer("Пока нет решений.")
        return

    for r in rows[-20:]:
        await message.answer(
            f"User: {r['owner_user_id']} | Раунд #{r['round_id']} | этап: {r['stage']}\n"
            f"Оценка: {r['score']}/10\n\n"
            f"Решение:\n{r['text']}\n\n"
            f"Отчет:\n{r['gigachat_report']}"
        )
