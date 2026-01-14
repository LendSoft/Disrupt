from functools import wraps
from aiogram.types import Message, CallbackQuery

def _get_role(kwargs):
    return kwargs.get("role")

def admin_only(handler):
    @wraps(handler)
    async def wrapper(event: Message | CallbackQuery, *args, **kwargs):
        role = _get_role(kwargs)
        if not role or not role.is_admin:
            if isinstance(event, CallbackQuery):
                await event.answer("Нет доступа.", show_alert=True)
            else:
                await event.answer("Нет доступа.")
            return
        return await handler(event, *args, **kwargs)
    return wrapper


def mod_or_admin(handler):
    @wraps(handler)
    async def wrapper(event: Message | CallbackQuery, *args, **kwargs):
        role = _get_role(kwargs)
        if not role or not (role.is_admin or role.is_moderator):
            if isinstance(event, CallbackQuery):
                await event.answer("Нет доступа.", show_alert=True)
            else:
                await event.answer("Нет доступа.")
            return
        return await handler(event, *args, **kwargs)
    return wrapper
