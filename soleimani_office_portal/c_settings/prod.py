from soleimani_office_portal.settings import *

SECRET_KEY = env('SECRET_KEY')

DEBUG = False

ALLOWED_HOSTS = ['*']

CSRF_TRUSTED_ORIGINS = ['https://s-office-portal.a-fathollahi.com/']

DATABASES['default'] = {
    'ENGINE': 'django.db.backends.sqlite3',
    'NAME': BASE_DIR / 'db.sqlite3',
}

DATABASES['log_db'] = {
    'ENGINE': 'django.db.backends.sqlite3',
    'NAME': BASE_DIR / 'log_db.sqlite3',
}

DATABASES['robot_db'] = {
    'ENGINE': 'django.db.backends.sqlite3',
    'NAME': BASE_DIR / 'robot_db.sqlite3',
}

CRONJOBS = [
    # minute, hours, day of month, month, day of week
    ('*/15 * * * *', 'robot.cron.check_requested_product_thread_is_active',),
    ('*/15 * * * *', 'robot.cron.check_product_warehouse_thread_is_active',),
]

# DATABASES['default'] = {
#     'ENGINE': 'django.db.backends.postgresql_psycopg2',
#     'NAME': '',
#     'USER': '',
#     'PASSWORD': '',
#     'HOST': 'localhost',
#     'PORT': '',
# }
#
# DATABASES['log_db'] = {
#     'ENGINE': 'django.db.backends.postgresql_psycopg2',
#     'NAME': '',
#     'USER': '',
#     'PASSWORD': '',
#     'HOST': 'localhost',
#     'PORT': '',
# }
