from tg_django.tg_manage.models import Profile, StatusLesson, Lesson


def change_inline_markup_status(status: StatusLesson,
                                query_status: str):
    """
    Меняет булевые поля в базе данных при нажатии пользователем
    (favorite, started, finished).

    :param status: Модель StatusLesson
    :param query_status: Тип статуса (favorite, started, finished)
    :return: Ничего
    """

    status.favorite = not status.favorite \
        if query_status == 'favorite' else status.favorite

    if query_status == 'started':
        status.started = not status.started
        status.finished = not status.finished \
            if status.finished and status.started else status.finished
    elif query_status == 'finished':
        status.finished = not status.finished
        status.started = not status.started \
            if status.finished and status.started else status.started

    status.save()


def response_for_callback_status(status_of_lesson: StatusLesson,
                                 query_status: str):
    """
    Выбирает нужный текст для определенного запроса

    :param status_of_lesson: Модель StatusLesson
    :param query_status: Тип статуса (favorite, started, finished)
    :return: Текст для callback
    """

    statuses = {
        'favorite': ('Удалено из избранного' if status_of_lesson.favorite else
                     'Добавлено в избранное'),
        'started': ('Удалено из начатого' if status_of_lesson.started else
                    'Добавлено в начатое'),
        'finished': ('Удалено из законченных' if status_of_lesson.finished else
                     'Добавлено в законченные')
    }
    return statuses.get(query_status)


def to_caption(lesson: Lesson):
    """
    Форматирует текст в нужный формат для caption.

    :param lesson: Модель Lesson
    :return: Текст, в которой информация урока
    """

    counts = 'раз'
    favorites = lesson.status_users.filter(favorite=True).count()
    if favorites in range(2, 5) or \
            (favorites % 10 in range(2, 5) and
             favorites not in range(12, 15)):
        counts = 'раза'

    themes = lesson.themes.all()
    themes_text = 'не состоит в темах'
    if themes:
        themes_text = ', '.join(theme.theme.title for theme in themes)

    result = (
        f'Автор: <code>{lesson.author.username}</code> 😑\n\n'
        f'<b>{lesson.title}</b>\n'
        f'Темы: <b>{themes_text}</b>\n\n'
        f'{lesson.description}\n\n'
        f'Добавили в избранное <b>{favorites} {counts}</b> ⭐️⭐️⭐️'
    )

    return result
