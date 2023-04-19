from django.contrib import admin

from .models import Lesson, StatusLesson, Profile, Theme, LessonTheme, Photo, \
    PhotoPack, ProfilePhotoPack


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'description', 'author', 'photo_id', 'url',)
    empty_value_display = '-- пусто --'


@admin.register(StatusLesson)
class StatusLessonAdmin(admin.ModelAdmin):
    list_display = ('id', 'profile', 'lesson', 'favorite', 'started', 'finished',)
    empty_value_display = '-- пусто --'


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('id', 'telegram_id', 'first_name', 'last_name', 'username', 'email', 'number',)
    empty_value_display = '-- пусто --'


@admin.register(Theme)
class ThemeAdmin(admin.ModelAdmin):
    list_display = ('id', 'title')
    empty_value_display = '-- пусто --'


@admin.register(LessonTheme)
class LessonThemeAdmin(admin.ModelAdmin):
    list_display = ('id', 'lesson', 'theme')
    empty_value_display = '-- пусто --'


@admin.register(Photo)
class PhotoAdmin(admin.ModelAdmin):
    list_display = ('id', 'photo_url', 'type_photo', 'photo_pack')
    empty_value_display = '-- пусто --'


@admin.register(PhotoPack)
class PhotoPackAdmin(admin.ModelAdmin):
    list_display = ('id', 'name',)
    empty_value_display = '-- пусто --'


@admin.register(ProfilePhotoPack)
class ProfilePhotoPackAdmin(admin.ModelAdmin):
    list_display = ('id', 'profile', 'photo_pack')
    empty_value_display = '-- пусто --'
