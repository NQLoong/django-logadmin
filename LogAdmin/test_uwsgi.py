"""
WSGI config for LogAdmin project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.8/howto/deployment/wsgi/
"""

import os
import sys
reload(sys)
sys.setdefaultencoding('utf8')
from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "LogAdmin.settings")

application = get_wsgi_application()
