from aiogram import types, Dispatcher
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from tgbot.models.db_commands import get_lessons


async def searching(query: types.InlineQuery):
    lessons = await get_lessons(query=query.query)
    results = []
    for lesson in lessons:
        try:
            results.append(
                types.InlineQueryResultPhoto(
                    id=str(lesson.id),
                    photo_url=lesson.photo_id,
                    thumb_url=lesson.photo_id,
                    title=lesson.title,
                    description=lesson.description,
                    reply_markup=InlineKeyboardMarkup(
                        row_width=2,
                        inline_keyboard=[
                            [
                                InlineKeyboardButton('Кнопка', callback_data='button'),
                            ]
                        ]
                    )
                )
            )
        except Exception as error:
            print(error)
    print(results)
    try:
        await query.answer(
            results=results,
        )
    except Exception as err:
        print(err)


def register_searching(dp: Dispatcher):
    dp.register_inline_handler(searching)
