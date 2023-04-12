from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from tgbot.keyboards.callback_datas import status_of_lesson_callback_data


def live_status_inline_keyboard(status,
                                lesson_id,
                                markup: InlineKeyboardMarkup) -> InlineKeyboardMarkup:
    """
    Кнопки, которые менют статус урока и показывают актуальный статус
    """
    started, favorite, finished = 'Начато ', 'В избранном ', 'Закончено '
    started += '🔴' if not status.started else '🟢'
    favorite += '🔴' if not status.favorite else '🟢'
    finished += '🔴' if not status.finished else '🟢'
    markup.row(
        InlineKeyboardButton(
            text=started,
            callback_data=status_of_lesson_callback_data.new(
                lesson_id=lesson_id,
                status='started'
            )
        ),
        InlineKeyboardButton(
            text=finished,
            callback_data=status_of_lesson_callback_data.new(
                lesson_id=lesson_id,
                status='finished'
            )
        )
    )
    markup.row(
        InlineKeyboardButton(
            text=favorite,
            callback_data=status_of_lesson_callback_data.new(
                lesson_id=lesson_id,
                status='favorite'
            )
        ),
    )
    return markup
