from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from django.core.paginator import Page

from tgbot.keyboards.callback_datas import make_menu_callback_data
from tgbot.keyboards.dynamic_inline_keyboards import make_themes_dynamic_inline
from tgbot.keyboards.misc_inline import (
    live_status_inline_keyboard, add_pagination_inline_keyboard,
)
from tgbot.models.db_commands import (
    get_themes,
    get_user,
    get_or_create_status_lesson,
)


def start_inline_keyboard() -> InlineKeyboardMarkup:
    CURRENT_LEVEL = 0

    markup = InlineKeyboardMarkup(row_width=3)
    markup.row(
        InlineKeyboardButton(
            text='Поиск 🔍',
            switch_inline_query_current_chat='',
        )
    )

    markup.row(
        InlineKeyboardButton(
            text='Темы 📚',
            callback_data=make_menu_callback_data(CURRENT_LEVEL + 1, 'themes')
        ),
        InlineKeyboardButton(
            text='Тренды 🔝',
            callback_data=make_menu_callback_data(CURRENT_LEVEL + 1, 'trends')
        ),
        InlineKeyboardButton(
            text='Профиль 📂',
            callback_data=make_menu_callback_data(CURRENT_LEVEL + 1, 'profile')
        ),
    )
    return markup


async def category_inline_keyboard(category: str) -> InlineKeyboardMarkup:
    CURRENT_LEVEL = 1

    markup = InlineKeyboardMarkup(row_width=4)

    if category == 'themes':
        themes = await get_themes()
        markup = make_themes_dynamic_inline(
            markup, themes, CURRENT_LEVEL, category
        )
    elif category == 'profile':
        markup.row(
            InlineKeyboardButton(
                text='Начатые 🥶',
                callback_data=make_menu_callback_data(
                    level=CURRENT_LEVEL + 1,
                    category=category,
                    topic='started',
                )
            ),
            InlineKeyboardButton(
                text='Законченные 🥵',
                callback_data=make_menu_callback_data(
                    level=CURRENT_LEVEL + 1,
                    category=category,
                    topic='finished',
                )
            )
        )
        markup.row(
            InlineKeyboardButton(
                text='В избранном 🥰',
                callback_data=make_menu_callback_data(
                    level=CURRENT_LEVEL + 1,
                    category=category,
                    topic='favorite',
                )
            )
        )

    markup.row(
        InlineKeyboardButton(
            text='Назад',
            callback_data=make_menu_callback_data(
                level=CURRENT_LEVEL - 1,
            )
        )
    )
    return markup


def default_lesson_keyboards(telegraph_url,
                             data, status) -> InlineKeyboardMarkup:
    """
    Плашка урока без пагинации.
    """
    markup = InlineKeyboardMarkup(row_width=3)
    markup.row(
        InlineKeyboardButton(
            text='Смотреть 👁‍🗨',
            url=telegraph_url,
        )
    )
    markup = live_status_inline_keyboard(
        markup, data, status
    )
    return markup


async def pagination_lesson_keyboards(data: dict,
                                      telegram_id: int,
                                      curr_page: Page) -> InlineKeyboardMarkup:
    """
    Плашка урока с пагинацией.
    """

    lesson = curr_page.object_list[0]
    user = await get_user(telegram_id)
    status = await get_or_create_status_lesson(user, lesson)

    markup = default_lesson_keyboards(
        telegraph_url=lesson.url,
        data=data,
        status=status,
    )

    back_keyboard = InlineKeyboardButton(
        text='Назад',
        callback_data=make_menu_callback_data(
            level=int(data.get('level')) - 1,
            category=data.get('category'),
        )
    )

    markup = add_pagination_inline_keyboard(
        data, markup, back_keyboard, curr_page
    )

    return markup
