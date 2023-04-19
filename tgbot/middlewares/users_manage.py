from aiogram import types
from aiogram.dispatcher.middlewares import BaseMiddleware

from tgbot.models.db_commands import (
    get_or_create_user,
    get_or_create_user_pack
)


class UsersManageMiddleware(BaseMiddleware):
    async def on_process_message(self, message: types.Message, data: dict):
        user = await get_or_create_user(
            message.from_user.id,
            message.from_user.username,
            message.from_user.first_name,
            message.from_user.last_name,
        )
        await get_or_create_user_pack(message.from_user.id, 8)
        data['user'] = user

    async def on_process_callback_query(self, call: types.CallbackQuery,
                                        data: dict):
        user = await get_or_create_user(
            call.from_user.id,
            call.from_user.username,
            call.from_user.first_name,
            call.from_user.last_name,
        )
        await get_or_create_user_pack(call.from_user.id, 8)
        data['user'] = user
