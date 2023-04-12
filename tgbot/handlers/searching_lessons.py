from aiogram import types, Dispatcher
from aiogram.types import InputTextMessageContent

from tgbot.models.db_commands import select_lessons


async def searching(query: types.InlineQuery):
    lessons = await select_lessons(query=query.query)
    results = []
    for lesson in lessons:
        results.append(
            types.InlineQueryResultArticle(
                id=lesson.id,
                thumb_url=lesson.photo_id,
                input_message_content=InputTextMessageContent(
                    message_text=f'lesson|{lesson.id}'),
                title=lesson.title,
                description=lesson.description,
            )
        )
    await query.answer(
        results=results,
    )


def register_searching(dp: Dispatcher):
    dp.register_inline_handler(searching)
