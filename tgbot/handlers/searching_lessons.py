from aiogram import types, Dispatcher

from tgbot.models.db_commands import get_lessons


async def searching(query: types.InlineQuery):
    results = await get_lessons(query=query.query)
    text = query.query
    print(text)
    print(results)


def register_searching(dp: Dispatcher):
    dp.register_inline_handler(searching)
