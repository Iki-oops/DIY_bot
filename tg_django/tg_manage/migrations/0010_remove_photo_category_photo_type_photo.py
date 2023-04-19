# Generated by Django 4.2 on 2023-04-18 11:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tg_manage', '0009_alter_photo_category'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='photo',
            name='category',
        ),
        migrations.AddField(
            model_name='photo',
            name='type_photo',
            field=models.CharField(default='  ', max_length=100, verbose_name='Тип изображения'),
            preserve_default=False,
        ),
    ]