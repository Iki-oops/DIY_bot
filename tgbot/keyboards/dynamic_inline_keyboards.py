from typing import Union

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from django.core.paginator import Page
from django.db.models import QuerySet

from tg_django.tg_manage.models import Theme, PhotoPack
from tgbot.keyboards.inline_keyboards import make_menu_callback_data
from tgbot.keyboards.misc_inline import add_pagination_inline_keyboard


def theme_generate_and_add_buttons(markup: InlineKeyboardMarkup,
                                   objects: Union[QuerySet[Theme], list],
                                   curr_level: int,
                                   category: str) -> InlineKeyboardMarkup:
    buttons = [
        InlineKeyboardButton(
            text=obj.title,
            callback_data=make_menu_callback_data(
                level=curr_level+1,
                category=category,
                topic=obj.id,
            )
        ) for obj in objects
    ]

    markup.row(
        *buttons
    )
    return markup


def resolve_remind_buttons(markup: InlineKeyboardMarkup,
                           t_hash: dict,
                           curr_level: int,
                           category: str,
                           generate_and_add_buttons) -> InlineKeyboardMarkup:
    two_buttons, three_buttons, four_buttons = (
        t_hash.get('two_buttons'),
        t_hash.get('three_buttons'),
        t_hash.get('four_buttons'),
    )
    if two_buttons and three_buttons:
        objects = two_buttons + [three_buttons.pop()]
        markup = generate_and_add_buttons(
            markup, objects, curr_level, category
        )
        two_buttons = []
    if two_buttons and four_buttons:
        objects = two_buttons + [four_buttons.pop()]
        markup = generate_and_add_buttons(
            markup, objects, curr_level, category
        )
        two_buttons = []
    if two_buttons:
        markup = generate_and_add_buttons(
            markup, two_buttons, curr_level, category
        )

    if three_buttons and four_buttons:
        if len(three_buttons) == 2:
            objects = three_buttons + [four_buttons.pop()]
            markup = generate_and_add_buttons(
                markup, objects, curr_level, category
            )
        elif len(three_buttons) == 1:
            if len(four_buttons) == 3:
                last_four_button = four_buttons[-1:]
                objects = three_buttons + four_buttons[:2]
                markup = generate_and_add_buttons(
                    markup, objects, curr_level, category
                )
                markup = generate_and_add_buttons(
                    markup, last_four_button, curr_level, category
                )

            else:
                objects = three_buttons + four_buttons[:2]
                markup = generate_and_add_buttons(
                    markup, objects, curr_level, category
                )
            return markup
    else:
        markup = generate_and_add_buttons(
            markup, three_buttons, curr_level, category
        )
    if four_buttons:
        markup = generate_and_add_buttons(
            markup, four_buttons, curr_level, category
        )

    return markup


def make_themes_dynamic_inline(markup: InlineKeyboardMarkup,
                               curr_page: Page,
                               curr_level: int,
                               data: dict) -> InlineKeyboardMarkup:
    t_hash = {
        'four_buttons': [],
        'three_buttons': [],
        'two_buttons': [],
    }
    category = data.get('category')

    for obj in curr_page.object_list:
        title = obj.title
        if len(title) <= 6:
            t_hash['four_buttons'].append(obj)
            if len(t_hash.get('four_buttons')) == 4:
                markup = theme_generate_and_add_buttons(
                    markup, t_hash.get('four_buttons'),
                    curr_level, category
                )
                t_hash['four_buttons'] = []
        elif len(title) <= 10:
            t_hash['three_buttons'].append(obj)
            if len(t_hash.get('three_buttons')) == 3:
                markup = theme_generate_and_add_buttons(
                    markup, t_hash.get('three_buttons'),
                    curr_level, category
                )
                t_hash['three_buttons'] = []
        elif len(title) <= 15:
            t_hash['two_buttons'].append(obj)
            if len(t_hash.get('two_buttons')) == 2:
                markup = theme_generate_and_add_buttons(
                    markup, t_hash.get('two_buttons'),
                    curr_level, category
                )
                t_hash['two_buttons'] = []
        else:
            markup.row(
                InlineKeyboardButton(
                    text=obj.title,
                    callback_data=make_menu_callback_data(
                        level=curr_level+1,
                        category=category,
                        topic=obj.id,
                    )
                )
            )
    markup = resolve_remind_buttons(
        markup, t_hash, curr_level, category, theme_generate_and_add_buttons
    )

    back_keyboard = InlineKeyboardButton(
        text='Назад',
        callback_data=make_menu_callback_data(
            level=curr_level - 1,
            category=data.get('category'),
        )
    )
    if curr_page.has_other_pages():
        markup = add_pagination_inline_keyboard(
            data, markup, back_keyboard, curr_page
        )
    else:
        markup.row(back_keyboard)

    return markup


# Динамически меняем фото-паки для профиля
def profile_generate_and_add_buttons(markup: InlineKeyboardMarkup,
                                     objects: Union[QuerySet[PhotoPack], list],
                                     curr_level: int,
                                     category: str) -> InlineKeyboardMarkup:

    buttons = [
        InlineKeyboardButton(
            text=obj.name,
            callback_data=make_menu_callback_data(
                level=curr_level,
                category=category,
                topic='set_profile',
                item_id=obj.id,
            )
        ) for obj in objects
    ]

    markup.row(
        *buttons
    )
    return markup


def make_dynamic_profiles_inline(curr_page: Page,
                                 curr_level: int,
                                 data: dict) -> InlineKeyboardMarkup:
    markup = InlineKeyboardMarkup(row_width=4)
    t_hash = {
        'four_buttons': [],
        'three_buttons': [],
        'two_buttons': [],
    }
    category = data.get('category')

    for obj in curr_page.object_list:
        name = obj.name
        if len(name) <= 6:
            t_hash['four_buttons'].append(obj)
            if len(t_hash.get('four_buttons')) == 4:
                markup = profile_generate_and_add_buttons(
                    markup, t_hash.get('four_buttons'),
                    curr_level, category
                )
                t_hash['four_buttons'] = []
        elif len(name) <= 10:
            t_hash['three_buttons'].append(obj)
            if len(t_hash.get('three_buttons')) == 3:
                markup = profile_generate_and_add_buttons(
                    markup, t_hash.get('three_buttons'),
                    curr_level, category
                )
                t_hash['three_buttons'] = []
        elif len(name) <= 15:
            t_hash['two_buttons'].append(obj)
            if len(t_hash.get('two_buttons')) == 2:
                markup = profile_generate_and_add_buttons(
                    markup, t_hash.get('two_buttons'),
                    curr_level, category
                )
                t_hash['two_buttons'] = []
        else:
            markup.row(
                InlineKeyboardButton(
                    text=obj.name,
                    callback_data=make_menu_callback_data(
                        level=curr_level,
                        category=category,
                        topic='set_profile',
                        item_id=obj.id,
                    )
                )
            )
    markup = resolve_remind_buttons(
        markup, t_hash, curr_level, category, profile_generate_and_add_buttons
    )

    back_keyboard = InlineKeyboardButton(
        text='Назад',
        callback_data=make_menu_callback_data(
            level=curr_level - 1,
            category=data.get('category'),
        )
    )
    if curr_page.has_other_pages():
        markup = add_pagination_inline_keyboard(
            data, markup, back_keyboard, curr_page
        )
    else:
        markup.row(back_keyboard)

    return markup

