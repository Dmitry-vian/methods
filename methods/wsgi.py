"""
WSGI конфиг для проекта methods.

Он предоставляет вызываемую функцию WSGI в качестве переменной уровня модуля с именем ``application``.
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'methods.settings')

application = get_wsgi_application()
