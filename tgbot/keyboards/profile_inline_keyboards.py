from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from tgbot.keyboards.callback_datas import make_menu_callback_data


def profile_inline_keyboard(markup: InlineKeyboardMarkup,
                            data: dict,
                            curr_level: int) -> InlineKeyboardMarkup:
    category = data.get('category')
    markup.row(
        InlineKeyboardButton(
            text='Начатые 🥶',
            callback_data=make_menu_callback_data(
                level=curr_level + 1,
                category=category,
                topic='started',
            )
        ),
        InlineKeyboardButton(
            text='Законченные 🥵',
            callback_data=make_menu_callback_data(
                level=curr_level + 1,
                category=category,
                topic='finished',
            )
        )
    )
    markup.row(
        InlineKeyboardButton(
            text='В избранном 🥰',
            callback_data=make_menu_callback_data(
                level=curr_level + 1,
                category=category,
                topic='favorite',
            )
        )
    )

    markup.row(
        InlineKeyboardButton(
            text='⬅️ Назад',
            callback_data=make_menu_callback_data(
                level=curr_level - 1,
            )
        ),
        InlineKeyboardButton(
            text='SET профиль ➡️',
            callback_data=make_menu_callback_data(
                level=curr_level + 1,
                category=category,
                topic='set_profile',
            )
        )
    )
    return markup
