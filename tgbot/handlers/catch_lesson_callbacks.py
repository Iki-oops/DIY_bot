from aiogram import types, Dispatcher

from tg_django.tg_manage.models import Profile
from tgbot.keyboards.callback_datas import status_of_lesson_callback_data
from tgbot.keyboards.inline_keyboards import (
    for_lesson_inline_keyboard,
)
from tgbot.misc.utils import (
    response_for_callback_status,
    change_inline_markup_status,
)
from tgbot.models.db_commands import get_or_create_status_lesson, get_lesson


async def handle_status_lesson(call: types.CallbackQuery,
                               callback_data: dict,
                               user: Profile):
    lesson_id, query_status = (
        int(callback_data.get('lesson_id')),
        callback_data.get('status')
    )

    lesson = await get_lesson(pk=lesson_id)
    status_of_lesson = await get_or_create_status_lesson(
        user=user,
        lesson=lesson,
    )

    await call.answer(
        response_for_callback_status(status_of_lesson, query_status)
    )

    change_inline_markup_status(
        status=status_of_lesson,
        query_status=query_status
    )

    await call.message.edit_reply_markup(
        reply_markup=for_lesson_inline_keyboard(
            lesson.url,
            lesson_id,
            status_of_lesson
        )
    )


def register_handle_status_lesson(dp: Dispatcher):
    dp.register_callback_query_handler(
        handle_status_lesson,
        status_of_lesson_callback_data.filter()
    )
