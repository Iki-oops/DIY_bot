from aiogram.utils.callback_data import CallbackData

menu_callback_data = CallbackData(
    'menu',
    'level',
    'category',
    'topic',
    'page',
)

lesson_callback_data = CallbackData(
    'lesson',
    'key',
    'topic',
    'lesson_id',
    'page',
    'query_status',
    'category'
)


def make_lesson_callback_data(key='0', topic='0', lesson_id='0',
                              page='0', query_status='0', category='0'):
    callback_data = lesson_callback_data.new(
        key=key, topic=topic, lesson_id=lesson_id,
        page=page, query_status=query_status,
        category=category
    )
    return callback_data


def make_menu_callback_data(level, category='0', topic='0', page=''):
    callback_data = menu_callback_data.new(
        level=level,
        category=category,
        topic=topic,
        page=page,
    )
    return callback_data
