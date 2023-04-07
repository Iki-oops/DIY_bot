from aiogram import Dispatcher
from aiogram.types import Message

from tgbot.models.tg_manage.models import Lesson


async def tab_lesson(message: Message):
    pass


def register_lesson(dp: Dispatcher):
    dp.register_message_handler(tab_lesson, state='*')
