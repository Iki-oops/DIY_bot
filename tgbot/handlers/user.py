from aiogram import Dispatcher
from aiogram.types import Message


async def user_start(message: Message):
    user = message.from_user
    username = user.username
    if user.full_name:
        username = user.full_name
    await message.answer(
        f"Привет, <b>{username}</b>👋!\n\n"
        "Это бот архив💾 туториалов и DIY-идей.🪄\n"
        "Здесь ты точно найдешь, чем себя занять!☺️\n\n"
        "<b>!!! Инструкции: !!!</b>"
    )


def register_user(dp: Dispatcher):
    dp.register_message_handler(user_start, commands=["start"], state="*")
