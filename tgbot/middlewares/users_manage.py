from aiogram import types
from aiogram.dispatcher.middlewares import BaseMiddleware

from tgbot.models import db_commands as commands


class UsersManageMiddleware(BaseMiddleware):
    async def on_pre_process_message(self, message: types.Message, *args):
        telegram_id, username, first_name, last_name = (
            message.from_user.id,
            message.from_user.username,
            message.from_user.first_name,
            message.from_user.last_name,
        )
        print(args)
        # user = await add_user(telegram_id, username, first_name, last_name)
        # return user
