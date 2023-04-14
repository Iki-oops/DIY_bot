from aiogram import types, Dispatcher

from tgbot.handlers.lesson_callbacks import (
    handle_trend_lessons,
    handle_theme_lessons,
    handle_profile_lessons,
)
from tgbot.handlers.theme_callbacks import handle_themes_or_profile
from tgbot.handlers.user import user_start
from tgbot.keyboards.callback_datas import menu_callback_data


async def lessons_controller(call: types.CallbackQuery,
                             callback_data: dict):
    category = callback_data.get('category')
    categories = {
        'themes': handle_theme_lessons,
        'profile': handle_profile_lessons,
    }
    await categories.get(category)(call, callback_data)


async def category_controller(call: types.CallbackQuery, callback_data: dict):
    category = callback_data.get('category')
    categories = {
        'themes': handle_themes_or_profile,
        'trends': handle_trend_lessons,
        'profile': handle_themes_or_profile,
    }
    await categories.get(category)(call, callback_data)


async def all_controller(call: types.CallbackQuery, callback_data: dict):
    level = callback_data.get('level')
    levels = {
        '0': user_start,
        '1': category_controller,
        '2': lessons_controller,
    }
    await levels.get(level)(call, callback_data)


def register_catch_user_callbacks(dp: Dispatcher):
    dp.register_callback_query_handler(
        all_controller,
        menu_callback_data.filter()
    )
