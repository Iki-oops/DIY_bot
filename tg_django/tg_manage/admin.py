from django.contrib import admin

from .models import Lesson, StatusLesson, Profile


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'description', 'author', 'img_id', 'url',)
    empty_value_display = '-- пусто --'


@admin.register(StatusLesson)
class StatusLessonAdmin(admin.ModelAdmin):
    list_display = ('id', 'profile', 'lesson', 'favorite', 'started', 'finished',)
    empty_value_display = '-- пусто --'


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('id', 'telegram_id', 'first_name', 'last_name', 'username', 'email', 'number',)
    empty_value_display = '-- пусто --'
