from aiogram.utils.callback_data import CallbackData

menu_callback_data = CallbackData(
    'menu',
    'level',
    'category',
    'subcategory',
)

status_of_lesson_callback_data = CallbackData(
    'status_of_lesson',
    'lesson_id',
    'status'
)


def make_menu_callback_data(level, category='0', subcategory='0'):
    callback_data = menu_callback_data.new(
        level=level,
        category=category,
        subcategory=subcategory,
    )
    return callback_data
