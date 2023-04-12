from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from tgbot.keyboards.callback_datas import make_menu_callback_data
from tgbot.keyboards.dynamic_inline_keyboards import make_themes_dynamic_inline
from tgbot.keyboards.misc_inline import live_status_inline_keyboard
from tgbot.models.db_commands import get_themes


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
            callback_data=make_menu_callback_data(CURRENT_LEVEL+1, 'themes')
        ),
        InlineKeyboardButton(
            text='Тренды 🔝',
            callback_data=make_menu_callback_data(CURRENT_LEVEL+1, 'trends')
        ),
        InlineKeyboardButton(
            text='Профиль 📂',
            callback_data=make_menu_callback_data(CURRENT_LEVEL+1, 'profile')
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
        statuses = {
            'started': 'Начатые 🥶',
            'favorite': 'В избранном 🥰',
            'finished': 'Законченные 🥵',
        }
        for status, text in statuses.items():
            markup.insert(
                InlineKeyboardButton(
                    text=text,
                    callback_data=make_menu_callback_data(
                        level=CURRENT_LEVEL+1,
                        category=category,
                        subcategory=status
                    )
                )
            )

    markup.row(
        InlineKeyboardButton(
            text='Назад',
            callback_data=make_menu_callback_data(
                level=CURRENT_LEVEL-1,
            )
        )
    )
    return markup


def for_lesson_inline_keyboard(telegraph_url, lesson_id, status) -> InlineKeyboardMarkup:
    """
    Кнопки, которые выходят на при команде /start
    """
    markup = InlineKeyboardMarkup(row_width=3)
    markup.row(
        InlineKeyboardButton(
            text='Смотреть 👁‍🗨',
            url=telegraph_url,
        )
    )
    markup = live_status_inline_keyboard(status, lesson_id, markup)
    return markup
