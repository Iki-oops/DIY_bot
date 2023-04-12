from aiogram import Dispatcher
from aiogram.types import Message


async def tab_lesson(message: Message):
    pass


def register_lesson(dp: Dispatcher):
    dp.register_message_handler(tab_lesson, state='*')
