from aiogram import types, Dispatcher
from django.db import IntegrityError

from tgbot.keyboards.inline_keyboards import default_lesson_keyboards
from tgbot.misc.utils import to_caption, prepare_default_data
from tgbot.models.db_commands import (
    get_lesson,
    get_or_create_user,
    get_or_create_status_lesson,
)
from tgbot.services.logging import logger


async def catch_lesson_after_inline_mode(message: types.Message):
    await message.delete()
    array = message.text.split('|')
    try:
        lesson = await get_lesson(int(array[1]))

        user = await get_or_create_user(
            telegram_id=message.from_user.id,
            username=message.from_user.username,
            first_name=message.from_user.first_name,
            last_name=message.from_user.last_name,
        )

        status = await get_or_create_status_lesson(
            user=user,
            lesson=lesson
        )

        caption = to_caption(lesson)

        data = {
            'key': 'inline_mode_lesson',
            'lesson_id': lesson.id,
        }
        data = prepare_default_data(callback_data=data)

        await message.answer_photo(
            photo=lesson.photo_id,
            caption=caption,
            reply_markup=default_lesson_keyboards(lesson.url, data, status)
        )
    except IntegrityError as error:
        logger.exception(error)


def register_catch_lesson_after_inline_mode(dp: Dispatcher):
    dp.register_message_handler(
        catch_lesson_after_inline_mode, is_lesson=True
    )
