from aiogram import types
from aiogram.dispatcher.middlewares.base import BaseMiddleware
from typing import Callable, Any, Awaitable
import logging

logger = logging.getLogger(__name__)

class LoggingMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[types.Update, dict[str, Any]], Awaitable[Any]],
        event: types.Update,
        data: dict[str, Any],
    ) -> Any:
        if event.message:
            logger.info(f"User {event.message.from_user.id}: {event.message.text}")
        return await handler(event, data)