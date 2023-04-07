from asgiref.sync import sync_to_async

from tg_django.tg_manage.models import Profile, StatusLesson, Lesson


@sync_to_async
def select_users(telegram_id=None, username='', first_name='', last_name=''):
    users = Profile.objects.filter(
            telegram_id=telegram_id,
    ) | Profile.objects.filter(
        username=username,
    ) | Profile.objects.filter(
        first_name=first_name,
    ) | Profile.objects.filter(
        last_name=last_name,
    )
    return users


@sync_to_async
def add_user(telegram_id, username, first_name='', last_name='', email='', phone=''):
    try:
        Profile(
            telegram_id=int(telegram_id),
            username=username,
            first_name=first_name,
            last_name=last_name,
            email=email,
            phone=phone
        ).save()
    except Exception as err:
        return select_users(telegram_id=int(telegram_id))


@sync_to_async
def get_lessons(query=''):
    lessons = Lesson.objects.prefetch_related().filter(
        author=query,
    ) | Lesson.objects.filter(
        title=query,
    ) | Lesson.objects.filter(
        description=query,
    )
    return lessons
