# Generated by Django 4.2 on 2023-04-09 11:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('tg_manage', '0006_alter_lesson_photo_id'),
    ]

    operations = [
        migrations.CreateModel(
            name='Theme',
            fields=[
                ('created_at', models.DateTimeField(auto_now_add=True, null=True, verbose_name='Дата создания')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Дата обновления')),
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=100, unique=True, verbose_name='Название группы')),
            ],
            options={
                'verbose_name': 'Тема',
                'verbose_name_plural': 'Темы',
            },
        ),
        migrations.AlterUniqueTogether(
            name='statuslesson',
            unique_together={('profile', 'lesson')},
        ),
        migrations.CreateModel(
            name='LessonTheme',
            fields=[
                ('created_at', models.DateTimeField(auto_now_add=True, null=True, verbose_name='Дата создания')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Дата обновления')),
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('lesson', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='themes', to='tg_manage.lesson', verbose_name='Урок')),
                ('theme', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='lessons', to='tg_manage.theme', verbose_name='Тема')),
            ],
            options={
                'verbose_name': 'Урок с темой',
                'verbose_name_plural': 'Уроки с темой',
                'unique_together': {('lesson', 'theme')},
            },
        ),
    ]
