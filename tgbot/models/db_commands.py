from asgiref.sync import sync_to_async
from django.db import IntegrityError
from django.db.models import Count, Q

from tg_django.tg_manage.models import Profile, StatusLesson, Lesson, Theme
from tgbot.services.logging import logger


@sync_to_async
def get_or_create_user(telegram_id, username,
                       first_name=None, last_name=None,
                       email=None, number=None):
    try:
        user = Profile.objects.create(
            telegram_id=telegram_id,
            username=username,
            first_name=first_name,
            last_name=last_name,
            email=email,
            number=number,
        )
        return user
    except IntegrityError:
        return Profile.objects.get(telegram_id=telegram_id)


@sync_to_async
def get_user(telegram_id):
    return Profile.objects.get(telegram_id=telegram_id)


@sync_to_async
def select_lessons(query=''):
    lessons = Lesson.objects.prefetch_related().filter(
        Q(author__username__contains=query) |
        Q(author__first_name__contains=query) |
        Q(author__last_name__contains=query) |
        Q(title__contains=query) |
        Q(description__contains=query)
    )
    return lessons


@sync_to_async
def get_lesson(pk: int):
    return Lesson.objects.select_related().get(id=pk)


# Добавить сортировку по favorites, ordering_by
@sync_to_async
def get_top_lessons():
    lessons = Lesson.objects.annotate(
        status_users_count=Count('status_users__favorite')
    ).order_by('status_users_count')
    return lessons


@sync_to_async
def get_or_create_status_lesson(user, lesson):
    try:
        status = StatusLesson.objects.get_or_create(
            profile=user,
            lesson=lesson
        )

        return status[0]
    except IntegrityError as error:
        logger.exception(error)


@sync_to_async
def get_themes():
    return Theme.objects.all()


@sync_to_async
def get_theme(theme_id: int):
    return Theme.objects.get(id=theme_id)


@sync_to_async
def get_theme_lessons(theme_id: int):
    lessons = Lesson.objects.filter(themes__theme__id=theme_id)
    return lessons


@sync_to_async
def get_status_lessons(status: str, telegram_id: int):
    user = Profile.objects.get(telegram_id=telegram_id)
    lessons = None
    if status == 'started':
        lessons = Lesson.objects.filter(
            Q(status_users__profile=user) & Q(status_users__started=True)
        )
    elif status == 'favorite':
        lessons = Lesson.objects.filter(
            Q(status_users__profile=user) & Q(status_users__favorite=True)
        )
    elif status == 'finished':
        lessons = Lesson.objects.filter(
            Q(status_users__profile=user) & Q(status_users__finished=True)
        )
    return lessons
