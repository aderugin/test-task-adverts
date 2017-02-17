# -*- coding: utf-8 -*-
"""
    Настройки среды для разработки
"""
from . import *  # NOQA


ALLOWED_HOSTS = ['localhost', 'adverts.dev']

SITE_ID = 1

DEBUG = True

COMPRESS_ENABLED = not DEBUG

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'postgres',
        'USER': 'postgres',
        'PASSWORD': 'postgres',
        'HOST': 'postgres.local',
        'PORT': '5432'
    }
}

INSTALLED_APPS += (  # NOQA
    'debug_toolbar',
)

MIDDLEWARE = (
    'debug_toolbar.middleware.DebugToolbarMiddleware',
) + MIDDLEWARE  # NOQA


def show_toolbar(request):
    return not request.is_ajax()

DEBUG_TOOLBAR_CONFIG = {  # NOQA
    'SHOW_TOOLBAR_CALLBACK': 'adverts.settings.develop.show_toolbar',
}
