Содержимое проекта methods
==========================

Подмодули
---------

Модуль methods.asgi
-------------------
.. code-block:: python

    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'methods.settings')

    application = ProtocolTypeRouter({
        "http": get_asgi_application(),
        "websocket": AuthMiddlewareStack(
            URLRouter(
                websocket_urlpatterns
            )
        ),
    })

.. automodule:: methods.asgi
   :members:
   :undoc-members:
   :show-inheritance:

Модуль methods.settings
-----------------------
.. code-block:: python

    INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'apps',
    'django_extensions',
    'rest_framework',
    'markdown',
    'channels',
    ]

.. automodule:: methods.settings
   :members:
   :undoc-members:
   :show-inheritance:

Модуль methods.urls
-------------------
.. code-block:: python

    urlpatterns = [
        path('apps/', include('apps.urls')),
    ]

.. automodule:: methods.urls
   :members:
   :undoc-members:
   :show-inheritance:

Модуль methods.wsgi
-------------------
.. code-block:: python

    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'methods.settings')

    application = get_wsgi_application()

.. automodule:: methods.wsgi
   :members:
   :undoc-members:
   :show-inheritance:

