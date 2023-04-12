from aiogram import types
from aiogram.dispatcher.middlewares import BaseMiddleware
from django.db import IntegrityError

from tgbot.keyboards.inline_keyboards import for_lesson_inline_keyboard
from tgbot.misc.utils import to_caption
from tgbot.models.db_commands import (
    get_lesson,
    get_or_create_status_lesson,
    get_or_create_user
)
from tgbot.services.logging import logger


class GetLessonMiddleware(BaseMiddleware):
    async def on_pre_process_message(self, message: types.Message, *args):
        try:
            array = message.text.split('|')
            if message.via_bot.id == 6122852095 and 'lesson' in array:
                await message.delete()
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

                    await message.answer_photo(
                        photo=lesson.photo_id,
                        caption=caption,
                        reply_markup=for_lesson_inline_keyboard(
                            lesson.url,
                            lesson.id,
                            status
                        )
                    )
                except IntegrityError as error:
                    logger.exception(error)
        except AttributeError as error:
            pass
