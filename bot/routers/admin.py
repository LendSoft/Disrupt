from aiogram import Router, F
from aiogram.types import Message

from bot.decorators.access import admin_only
from bot.keyboards.admin import admin_panel_kb
from bot.keyboards.common import main_menu_kb

router = Router()

@router.message(F.text == "Админ панель")
@admin_only
async def admin_panel(message: Message, **_):
    await message.answer("Админ панель:", reply_markup=admin_panel_kb())

@router.message(F.text == "Назначить модератора")
@admin_only
async def ask_add_mod(message: Message, **_):
    await message.answer("Пришлите user_id человека, которому выдать модератора.")

@router.message(F.text.regexp(r"^\d+$"))
async def numeric_message_router(message: Message, role, db, **_):
    # Примитивный режим: если админ открыл панель и прислал число — трактуем как действие.
    # В проде лучше сделать отдельные состояния FSM для админки.
    if not role.is_admin:
        return

    user_id = int(message.text)
    await db.add_moderator(user_id)
    await message.answer(f"Готово: user_id={user_id} теперь модератор.")

@router.message(F.text == "Снять модератора")
@admin_only
async def ask_remove_mod(message: Message, **_):
    await message.answer("Пришлите user_id человека, у которого снять модератора (числом).")

@router.message(F.text == "Список модераторов")
@admin_only
async def list_mods(message: Message, db, **_):
    mods = await db.list_moderators()
    if not mods:
        await message.answer("Модераторов нет.")
        return
    await message.answer("Модераторы:\n" + "\n".join(str(x) for x in mods))

@router.message(F.text == "Назад")
async def back_from_admin(message: Message, role, **_):
    if role.is_admin:
        await message.answer("Главное меню.", reply_markup=main_menu_kb(is_admin=True))
