import os

from django.core.wsgi import get_wsgi_application

# WSGI Settings
os.environ.setdefault(
    "DJANGO_SETTINGS_MODULE", "MySocial.settings"
)
# WSGI App
application = get_wsgi_application()
