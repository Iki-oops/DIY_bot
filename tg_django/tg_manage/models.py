from django.db import models


class TimeBasedModel(models.Model):
    class Meta:
        abstract = True

    created_at = models.DateTimeField(
        'Дата создания',
        auto_now_add=True,
        blank=True,
        null=True
    )
    updated_at = models.DateTimeField(
        'Дата обновления',
        auto_now=True,
        blank=True,
    )


class Profile(TimeBasedModel):
    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    telegram_id = models.BigIntegerField(
        'Id-телеграма',
        unique=True,
    )
    first_name = models.CharField(
        'Имя',
        max_length=100,
        null=True,
        blank=True,
    )
    last_name = models.CharField(
        'Фамилия',
        max_length=100,
        null=True,
        blank=True,
    )
    username = models.CharField(
        'Псевдоним',
        max_length=100,
        unique=True,
        null=True
    )
    email = models.EmailField(
        'Почта',
        null=True,
        blank=True,
    )
    number = models.CharField(
        'Номер телефона',
        null=True,
        blank=True,
    )

    def __str__(self):
        return f'{self.username}'


class Lesson(TimeBasedModel):
    class Meta:
        ordering = ('-created_at', '-updated_at')
        verbose_name = 'Урок'
        verbose_name_plural = 'Уроки'

    id = models.AutoField(
        primary_key=True,
    )
    author = models.ForeignKey(
        Profile,
        on_delete=models.SET_NULL,
        related_name='lessons',
        null=True,
        verbose_name='Автор',
    )
    title = models.CharField(
        'Заглавие урока',
        max_length=100,
    )
    description = models.TextField(
        'Описание урока',
    )
    photo_id = models.CharField(
        'Id картинки',
        max_length=200,
        default='AgACAgIAAxkBAAOlZDBAK24zrhv8PuXvI8Groa-CfGUAAqnFMRvKcIFJoV0paVg5cyQBAAMCAAN4AAMvBA',
        null=True,
        blank=True,
    )
    url = models.URLField(
        'URL-telegraph урока',
    )

    def __str__(self):
        return f'{self.author} - {self.title}'


class StatusLesson(TimeBasedModel):
    class Meta:
        verbose_name = 'Статус'
        verbose_name_plural = 'Статусы'

    id = models.AutoField(
        primary_key=True,
    )
    profile = models.ForeignKey(
        Profile,
        on_delete=models.CASCADE,
        related_name='status_lessons',
    )
    lesson = models.ForeignKey(
        Lesson,
        on_delete=models.CASCADE,
        related_name='status_users',
    )
    favorite = models.BooleanField(
        'В избранное',
        default=False,
    )
    started = models.BooleanField(
        'Урок начат',
        default=False,
    )
    finished = models.BooleanField(
        'Урок закончен',
        default=False,
    )

    def __str__(self):
        return f'{self.profile} - {self.lesson}'
