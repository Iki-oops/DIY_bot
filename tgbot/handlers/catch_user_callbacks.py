from aiogram import types, Dispatcher
from aiogram.types import InputMediaPhoto

from tgbot.handlers.user import user_start
from tgbot.keyboards.callback_datas import menu_callback_data
from tgbot.keyboards.inline_keyboards import (
    category_inline_keyboard,
)
from tgbot.models.db_commands import (
    get_top_lessons,
    get_theme_lessons,
    get_status_lessons,
)


# Доделать пагинатор и плашки
async def handle_trend_lessons(call: types.CallbackQuery, callback: dict):
    await call.answer()
    # await call.message.delete()
    lessons = await get_top_lessons()
    print(lessons)
    # await call.message.answer_photo(
    #
    # )


async def handle_themes_profile(call: types.CallbackQuery,
                                callback_data: dict):
    await call.answer()

    category = callback_data.get('category')
    if category == 'themes':
        caption = ('Все темы, которые есть в базе 😎\n'
                   'Выбирай интересующую тебя область 😏👇')
        photo = call.bot.get('config').misc.themes_photo
    else:
        caption = ('Здесь находятся все твои начинания, 🥳\n'
                   'добавленные в избранное и законченные')
        photo = call.bot.get('config').misc.profile_photo

    await call.message.edit_media(
        media=InputMediaPhoto(
            media=photo,
            caption=caption
        ),
        reply_markup=await category_inline_keyboard(category),
    )


async def category_controller(call: types.CallbackQuery, callback_data: dict):
    category = callback_data.get('category')
    categories = {
        'themes': handle_themes_profile,
        'trends': handle_trend_lessons,
        'profile': handle_themes_profile,
    }
    await categories.get(category)(call, callback_data)


async def subcategory_controller(call: types.CallbackQuery, callback_data: dict):
    category = callback_data.get('category')
    subcategory = callback_data.get('subcategory')
    if category == 'themes':
        lessons = await get_theme_lessons(subcategory)
        print(lessons)
        # Плашка с пагинатором
    elif category == 'profile':
        lessons = await get_status_lessons(
            subcategory,
            call.from_user.id,
        )
        print(lessons)
        # плашка с пагинатором
    await call.answer()

    # Неправильно нужны плашки вместо инлайн кнопок

    # category = callback_data.get('category')
    # subcategory = callback_data.get('subcategory')
    # if category == 'themes':
    #     theme = await get_theme(subcategory)
    #     photo = call.message.bot.get('config').misc.lessons_photo
    #     caption = (f'Здесь находятся все уроки с темой {theme.title}'
    #                 'Выирай ')
    #     await call.message.answer_photo(
    #         photo=photo,
    #         caption=
    #     )


async def all_controller(call: types.CallbackQuery, callback_data: dict):
    level = callback_data.get('level')
    levels = {
        '0': user_start,
        '1': category_controller,
        '2': subcategory_controller,
    }
    await levels.get(level)(call, callback_data)


def register_catch_user_callbacks(dp: Dispatcher):
    dp.register_callback_query_handler(
        all_controller,
        menu_callback_data.filter()
    )
