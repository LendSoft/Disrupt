from aiogram import Router, F
from aiogram.filters import CommandStart
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from bot.texts import WELCOME_TEXT

from bot.keyboards.common import main_menu_kb
from bot.states.game import GameStates

router = Router()

@router.message(CommandStart())
async def cmd_start(message: Message, state: FSMContext, role, db, **_):
    await state.clear()
    await message.answer(WELCOME_TEXT, reply_markup=main_menu_kb(is_admin=role.is_admin))
    await message.answer("Введите ФИО капитана:")
    await state.set_state(GameStates.captain_name)
