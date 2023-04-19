from aiogram import types, Dispatcher
from django.core.cache import cache

from tg_django.tg_manage.models import Profile
from tgbot.handlers.tab_lesson import get_tab_lesson
from tgbot.handlers.updating_profile_photo import update_profile_photo
from tgbot.keyboards.callback_datas import lesson_callback_data
from tgbot.keyboards.inline_keyboards import (
    default_lesson_keyboards,
)
from tgbot.misc.utils import (
    response_for_callback_status,
    change_status, prepare_default_data,
)
from tgbot.models.db_commands import (
    get_or_create_status_lesson,
    get_lesson,
    get_top_lessons,
    get_theme_lessons,
    get_status_lessons
)


async def handle_profile_lessons(call: types.CallbackQuery,
                                 callback_data: dict):
    topic = callback_data.get('topic')
    data = prepare_default_data(
        callback_data, key='profile_lessons', level=2, category='profile'
    )
    lessons = await get_status_lessons(topic, call.from_user.id)
    if topic == 'set_profile':
        await update_profile_photo(call, data)
    else:
        if lessons:
            await get_tab_lesson(call, data, lessons)
        else:
            await call.answer('Нет уроков')


async def handle_theme_lessons(call: types.CallbackQuery, callback_data: dict):
    condition = callback_data.get('topic')
    data = prepare_default_data(
        callback_data, key='theme_lessons', level=2, category='themes'
    )
    lessons = await get_theme_lessons(condition)
    if lessons:
        await get_tab_lesson(call, data, lessons)
    else:
        await call.answer('Нет уроков')


async def handle_trend_lessons(call: types.CallbackQuery,
                               callback_data: dict):
    await call.answer()
    lessons = cache.get('lessons')
    if not lessons:
        lessons = await get_top_lessons()
        cache.set('lessons', lessons, 300)

    data = prepare_default_data(callback_data, key='trend_lessons', page=1)
    await get_tab_lesson(call, data, lessons)


async def handle_inline_mode_lesson(call: types.CallbackQuery,
                                    callback_data: dict,
                                    user: Profile):
    """
    Обрабатывает только уроки, выбранные в инлайн режиме.
    """
    data = prepare_default_data(callback_data, key='inline_mode_lesson')

    lesson = await get_lesson(pk=data.get('lesson_id'))
    status_of_lesson = await get_or_create_status_lesson(
        user=user,
        lesson=lesson,
    )

    await call.answer(
        response_for_callback_status(
            status_of_lesson, data.get('query_status')
        )
    )

    change_status(
        status=status_of_lesson,
        query_status=data.get('query_status')
    )

    await call.message.edit_reply_markup(
        reply_markup=default_lesson_keyboards(
            lesson.url,
            data,
            status_of_lesson,
        )
    )


def register_handle_lesson(dp: Dispatcher):
    dp.register_callback_query_handler(
        handle_inline_mode_lesson,
        lesson_callback_data.filter(key='inline_mode_lesson')
    )
    dp.register_callback_query_handler(
        handle_trend_lessons,
        lesson_callback_data.filter(key='trend_lessons')
    )
    dp.register_callback_query_handler(
        handle_theme_lessons,
        lesson_callback_data.filter(key='theme_lessons')
    )
    dp.register_callback_query_handler(
        handle_profile_lessons,
        lesson_callback_data.filter(key='profile_lessons')
    )

