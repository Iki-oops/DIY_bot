from aiogram.utils.callback_data import CallbackData

menu_callback_data = CallbackData(
    'menu',
    'level',
    'category',
    'topic',
)

lesson_callback_data = CallbackData(
    'lesson',
    'key',
    'topic',
    'lesson_id',
    'page',
    'query_status',
)

# status_of_lesson_callback_data = CallbackData(
#     'status_of_lesson',
#     'key',
#     'item_id',
#     'lesson_id',
#     'status',
#     'page'
# )
#
# pagination_callback_data = CallbackData(
#     'pagination',
#     'key',
#     'page',
#     'item_id',
# )


def make_lesson_callback_data(key='0', topic='0', lesson_id='0',
                              page='0', query_status='0',):
    callback_data = lesson_callback_data.new(
        key=key, topic=topic, lesson_id=lesson_id,
        page=page, query_status=query_status,
    )
    return callback_data


def make_menu_callback_data(level, category='0', topic='0'):
    callback_data = menu_callback_data.new(
        level=level,
        category=category,
        topic=topic,
    )
    return callback_data
