import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'soleimani_office_portal.c_settings.prod')

application = get_wsgi_application()
