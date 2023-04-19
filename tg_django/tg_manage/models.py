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


class Theme(TimeBasedModel):
    class Meta:
        verbose_name = 'Тема'
        verbose_name_plural = 'Темы'

    id = models.AutoField(
        primary_key=True,
    )
    title = models.CharField(
        verbose_name='Название группы',
        max_length=100,
        unique=True,
    )

    def __str__(self):
        return f'{self.title}'


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
    photo_id = models.URLField(
        'URL картинки',
        default='https://telegra.ph//file/03f446be71d69a87288e6.jpg',
        null=True,
        blank=True,
    )
    url = models.URLField(
        'URL-telegraph урока',
    )

    def __str__(self):
        return f'{self.author} - {self.title}'


class LessonTheme(TimeBasedModel):
    class Meta:
        verbose_name = 'Урок с темой'
        verbose_name_plural = 'Уроки с темой'
        unique_together = ('lesson', 'theme')

    id = models.AutoField(
        primary_key=True,
    )
    lesson = models.ForeignKey(
        Lesson,
        on_delete=models.CASCADE,
        verbose_name='Урок',
        related_name='themes',
    )
    theme = models.ForeignKey(
        Theme,
        on_delete=models.CASCADE,
        verbose_name='Тема',
        related_name='lessons',
    )

    def __str__(self):
        return f'{self.lesson} в теме {self.theme}'


class StatusLesson(TimeBasedModel):
    class Meta:
        verbose_name = 'Статус'
        verbose_name_plural = 'Статусы'
        unique_together = ('profile', 'lesson')

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


class PhotoPack(TimeBasedModel):
    class Meta:
        verbose_name = 'Пак изображений'
        verbose_name_plural = 'Паки изображений'

    id = models.AutoField(
        primary_key=True,
    )
    name = models.CharField(
        verbose_name='Название пака',
        max_length=100,
    )

    def __str__(self):
        return f'{self.name}'


class Photo(models.Model):
    class Meta:
        verbose_name = 'Изображение'
        verbose_name_plural = 'Изображения'

    id = models.AutoField(
        primary_key=True,
    )
    photo_url = models.URLField(
        verbose_name='URL-изображения',
        unique=True,
    )
    type_photo = models.CharField(
        verbose_name='Тип изображения',
        max_length=100,
    )
    photo_pack = models.ForeignKey(
        PhotoPack,
        on_delete=models.SET_NULL,
        related_name='photos',
        verbose_name='Пак',
        null=True,
        blank=True,
    )

    def __str__(self):
        return self.photo_url


class ProfilePhotoPack(TimeBasedModel):
    class Meta:
        verbose_name = 'Пользователь и его фото-пак'
        verbose_name_plural = 'Пользователи и их фото-паки'
        unique_together = ('profile', 'photo_pack',)

    id = models.AutoField(
        primary_key=True,
    )
    profile = models.ForeignKey(
        Profile,
        on_delete=models.CASCADE,
        related_name='photo_pack',
        unique=True,
    )
    photo_pack = models.ForeignKey(
        PhotoPack,
        on_delete=models.CASCADE,
        related_name='profiles',
        null=True,
        blank=True,
    )

    def __str__(self):
        return f'{self.profile} - {self.photo_pack}'
