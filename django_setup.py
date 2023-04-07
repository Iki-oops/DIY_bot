import os

import django

os.environ.setdefault(
        'DJANGO_SETTINGS_MODULE',
        'tg_django.tg_django.settings',
)
os.environ.update(
    {
        'DJANGO_ALLOW_ASYNC_UNSAFE': 'true',
    }
)
django.setup()
