from typing import Union

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from django.db.models import QuerySet

from tg_django.tg_manage.models import Theme
from tgbot.keyboards.inline_keyboards import make_menu_callback_data


def generate_and_add_buttons(markup: InlineKeyboardMarkup,
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
                           category: str) -> InlineKeyboardMarkup:
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
                last_four_button = four_buttons[-1]
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
    if four_buttons:
        markup = generate_and_add_buttons(
            markup, four_buttons, curr_level, category
        )

    return markup


def make_themes_dynamic_inline(markup: InlineKeyboardMarkup,
                               objects: QuerySet[Theme],
                               curr_level: int,
                               category: str) -> InlineKeyboardMarkup:
    t_hash = {
        'four_buttons': [],
        'three_buttons': [],
        'two_buttons': [],
    }

    for obj in objects:
        title = obj.title
        if len(title) <= 6:
            t_hash['four_buttons'].append(obj)
            if len(t_hash.get('four_buttons')) == 4:
                markup = generate_and_add_buttons(
                    markup, t_hash.get('four_buttons'), curr_level, category
                )
                t_hash['four_buttons'] = []
        elif len(title) <= 10:
            t_hash['three_buttons'].append(obj)
            if len(t_hash.get('three_buttons')) == 3:
                markup = generate_and_add_buttons(
                    markup, t_hash.get('three_buttons'), curr_level, category
                )
                t_hash['three_buttons'] = []
        elif len(title) <= 15:
            t_hash['two_buttons'].append(obj)
            if len(t_hash.get('two_buttons')) == 2:
                markup = generate_and_add_buttons(
                    markup, t_hash.get('two_buttons'), curr_level, category
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
        markup, t_hash, curr_level, category
    )
    return markup
