# Generated by Django 4.2 on 2023-04-18 15:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('tg_manage', '0011_photo_category'),
    ]

    operations = [
        migrations.CreateModel(
            name='PhotoPack',
            fields=[
                ('created_at', models.DateTimeField(auto_now_add=True, null=True, verbose_name='Дата создания')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Дата обновления')),
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100, verbose_name='Название пака')),
            ],
            options={
                'verbose_name': 'Пак изображений',
                'verbose_name_plural': 'Паки изображений',
            },
        ),
        migrations.RemoveField(
            model_name='photo',
            name='category',
        ),
        migrations.AddField(
            model_name='photo',
            name='photo_pack',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='photos', to='tg_manage.photopack', verbose_name='Пак'),
        ),
        migrations.CreateModel(
            name='ProfilePhotoPack',
            fields=[
                ('created_at', models.DateTimeField(auto_now_add=True, null=True, verbose_name='Дата создания')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Дата обновления')),
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('photo_pack', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='profiles', to='tg_manage.photopack')),
                ('profile', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='photo_pack', to='tg_manage.profile')),
            ],
            options={
                'verbose_name': 'Пользователь и его фото-пак',
                'verbose_name_plural': 'Пользователи и их фото-паки',
                'unique_together': {('profile', 'photo_pack')},
            },
        ),
    ]
