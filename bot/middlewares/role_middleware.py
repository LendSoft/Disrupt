from dataclasses import dataclass
from typing import Any, Awaitable, Callable, Dict

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject

from bot.config import Settings
from bot.services.json_db import JsonDB


@dataclass
class RoleContext:
    is_admin: bool
    is_moderator: bool


class RoleMiddleware(BaseMiddleware):
    def __init__(self, settings: Settings):
        self.settings = settings
        self.db = JsonDB(settings)

    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any],
    ) -> Any:
        tg_user = data.get("event_from_user")
        user_id = int(tg_user.id) if tg_user else 0

        is_admin = user_id in self.settings.admins
        is_moderator = await self.db.is_moderator(user_id)

        data["role"] = RoleContext(is_admin=is_admin, is_moderator=is_moderator)
        data["settings"] = self.settings
        data["db"] = self.db
        return await handler(event, data)
