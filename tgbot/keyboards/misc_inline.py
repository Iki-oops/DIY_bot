from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from django.core.paginator import Page

from tg_django.tg_manage.models import StatusLesson
from tgbot.keyboards.callback_datas import (
    make_lesson_callback_data
)


def add_pagination_inline_keyboard(data: dict,
                                   markup: InlineKeyboardMarkup,
                                   back_keyboard: InlineKeyboardButton,
                                   curr_page: Page) -> InlineKeyboardMarkup:
    key, topic, category = (
        data.get('key'), data.get('topic'), data.get('category')
    )
    prev_page = ''
    prev_page_text = '!<'
    prev_callback_data = make_lesson_callback_data(
        key=key, page=prev_page, topic=topic, category=category
    )

    next_page = curr_page.number
    next_page_text = '!>'
    next_callback_data = make_lesson_callback_data(
        key=key, page=next_page, topic=topic, category=category
    )

    if curr_page.has_previous():
        prev_page = curr_page.previous_page_number()
        prev_page_text = '<'
        prev_callback_data = make_lesson_callback_data(
            key=key, page=prev_page, topic=topic, category=category
        )

    if curr_page.has_next():
        next_page = curr_page.next_page_number()
        next_page_text = '>'
        next_callback_data = make_lesson_callback_data(
            key=key, page=next_page, topic=topic, category=category
        )

    markup.row(
        InlineKeyboardButton(
            text=prev_page_text,
            callback_data=prev_callback_data,
        ),
        back_keyboard,
        InlineKeyboardButton(
            text=next_page_text,
            callback_data=next_callback_data,
        )
    )

    return markup


def live_status_inline_keyboard(markup: InlineKeyboardMarkup,
                                callback_data: dict,
                                status: StatusLesson) -> InlineKeyboardMarkup:
    """
    Кнопки, которые менют статус урока и показывают актуальный статус
    """

    key, lesson_id, topic, page, category = (
        callback_data.get('key'), callback_data.get('lesson_id'),
        callback_data.get('topic'), callback_data.get('page'),
        callback_data.get('category')
    )
    started = 'Начать' if not status.started else 'Начал'
    favorite = 'Добавить в избранное'\
        if not status.favorite else 'Добавлено в избранное'
    finished = 'Закончить' if not status.finished else 'Закончил'
    markup.row(
        InlineKeyboardButton(
            text=started,
            callback_data=make_lesson_callback_data(
                key=key,
                topic=topic,
                page=page,
                lesson_id=lesson_id,
                query_status='started',
                category=category,
            )
        ),
        InlineKeyboardButton(
            text=finished,
            callback_data=make_lesson_callback_data(
                key=key,
                topic=topic,
                page=page,
                lesson_id=lesson_id,
                query_status='finished',
                category=category,
            )
        )
    )
    markup.row(
        InlineKeyboardButton(
            text=favorite,
            callback_data=make_lesson_callback_data(
                key=key,
                topic=topic,
                page=page,
                lesson_id=lesson_id,
                query_status='favorite',
                category=category,
            )
        ),
    )
    return markup
