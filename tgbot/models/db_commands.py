from asgiref.sync import sync_to_async
from django.db import IntegrityError
from django.db.models import Count, Q

from tg_django.tg_manage.models import (
    Profile,
    StatusLesson,
    Lesson,
    Theme,
    Photo, PhotoPack, ProfilePhotoPack
)
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
    ).order_by('-updated_at', '-created_at')
    return lessons


@sync_to_async
def get_lesson(pk: int):
    return Lesson.objects.select_related().get(id=pk)


# Добавить сортировку по favorites, order_by
# Неправильный запрос
@sync_to_async
def get_top_lessons():
    lessons = Lesson.objects.annotate(
        status_users_count=Count('id', filter=Q(status_users__favorite=True))
    ).order_by('-status_users_count')
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
    return Theme.objects.all().order_by('-updated_at', '-created_at')


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


@sync_to_async
def get_or_create_photo(url: str, type_photo: str, photo_pack: PhotoPack):
    return Photo.objects.get_or_create(
        photo_url=url, type_photo=type_photo, photo_pack=photo_pack
    )


@sync_to_async
def get_or_create_user_pack(telegram_id, pack_id):
    user = Profile.objects.get(telegram_id=telegram_id)
    pack = PhotoPack.objects.get(id=pack_id)
    return ProfilePhotoPack.objects.get_or_create(
        profile=user, photo_pack=pack)


@sync_to_async
def get_photo_packs():
    return PhotoPack.objects.all().order_by('-updated_at')


@sync_to_async
def get_photo_packs_without_user_pack(user_pack: PhotoPack):
    return PhotoPack.objects.exclude(id=user_pack.id).order_by('-updated_at')


@sync_to_async
def get_or_create_photo_pack(name):
    return PhotoPack.objects.get_or_create(name=name)


@sync_to_async
def get_photo_pack(pk):
    return PhotoPack.objects.get(id=pk)


@sync_to_async
def get_photo_via_type_photo(telegram_id: int, type_photo):
    user_pack = Profile.objects.get(
        telegram_id=telegram_id)
    user_pack = user_pack.photo_pack.first()
    return Photo.objects.get(
        photo_pack=user_pack.photo_pack, type_photo=type_photo).photo_url


@sync_to_async
def get_user_pack(telegram_id: int):
    user = Profile.objects.get(telegram_id=telegram_id)
    return user.photo_pack.first()
