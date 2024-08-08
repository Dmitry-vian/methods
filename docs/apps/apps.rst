Содержимое приложения apps
==========================

Подпакеты
---------

.. toctree::
   :maxdepth: 4

   apps.migrations

Подмодули
---------

Модуль apps.apps
----------------

.. automodule:: apps.apps
   :members:
   :undoc-members:
   :show-inheritance:

Модуль apps.consumers
---------------------

.. automodule:: apps.consumers
   :members:
   :undoc-members:
   :show-inheritance:

Модуль apps.models
------------------

.. automodule:: apps.models
   :members:
   :undoc-members:
   :show-inheritance:

Модуль apps.routing
-------------------

.. code-block:: python

    from django.urls import re_path
    from apps.consumers import EmployeeConsumer


    websocket_urlpatterns = [
        re_path(r'^ws/employees/$', EmployeeConsumer.as_asgi()),
    ]

.. automodule:: apps.routing
   :members:
   :undoc-members:
   :show-inheritance:

Модуль apps.serializers
-----------------------

.. automodule:: apps.serializers
   :members:
   :undoc-members:
   :show-inheritance:

Модуль apps.signals
-----------------------

.. automodule:: apps.signals
   :members:
   :undoc-members:
   :show-inheritance:

Модуль apps.urls
----------------

.. code-block:: python

    router = DefaultRouter()
    app_name = 'apps'
    router.register(r'systemcommands', SystemCommands, basename='ifconfig-apps')
    router.register(r'systemcommands', SystemCommands, basename='touchfile-apps')
    urlpatterns = router.urls

.. automodule:: apps.urls
   :members:
   :undoc-members:
   :show-inheritance:

Модуль apps.views
-----------------

.. automodule:: apps.views
   :members:
   :undoc-members:
   :show-inheritance:

Модуль apps.websocket_client
---------------------------------

.. literalinclude:: ../../apps/websocket_client.html

