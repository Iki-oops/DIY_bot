from aiogram import types
from aiogram.types import InputMediaPhoto
from aiogram.utils.exceptions import MessageNotModified
from django.core.paginator import Paginator
from django.db.models import QuerySet

from tg_django.tg_manage.models import Lesson
from tgbot.keyboards.inline_keyboards import pagination_lesson_keyboards
from tgbot.misc.utils import to_caption, response_for_callback_status, \
    change_status
from tgbot.models.db_commands import get_lesson, get_user, \
    get_or_create_status_lesson


async def get_tab_lesson(call: types.CallbackQuery,
                         data: dict,
                         lessons: QuerySet[Lesson]):
    page, prefix = data.get('page'), data.get('@')
    query_status = data.get('query_status')
    # print(data)

    pagination = Paginator(lessons, 1)
    curr_page = pagination.get_page(page)
    lesson = curr_page.object_list[0]

    if query_status and query_status != '0':
        query_status = data.get('query_status')
        lesson = await get_lesson(pk=lesson.id)
        user = await get_user(call.from_user.id)
        status_of_lesson = await get_or_create_status_lesson(
            user=user,
            lesson=lesson,
        )

        await call.answer(
            response_for_callback_status(status_of_lesson, query_status)
        )
        change_status(
            status=status_of_lesson,
            query_status=query_status,
        )
        await call.message.edit_reply_markup(
            reply_markup=await pagination_lesson_keyboards(
                data, call.from_user.id, curr_page
            )
        )
        return

    await call.answer()
    caption = to_caption(lesson)

    try:
        await call.message.edit_media(
            media=InputMediaPhoto(
                media=lesson.photo_id,
                caption=caption,
            ),
            reply_markup=await pagination_lesson_keyboards(
                data, call.from_user.id, curr_page
            )
        )
    except MessageNotModified:
        pass
