"""
**ASGI конфигурация для проекта methods**

Этот модуль определяет точку входа для ASGI сервера, объединяя обработку HTTP-запросов и WebSocket-соединений.

**Ключевые элементы:**

* **`get_asgi_application()`:** Получает объект ASGI приложения Django для обработки HTTP-запросов.
* **`ProtocolTypeRouter`:** Маршрутизатор, который определяет, какой обработчик использовать в зависимости от протокола (HTTP или WebSocket).
* **`AuthMiddlewareStack`:** Обеспечивает аутентификацию пользователей для WebSocket-соединений.
* **`URLRouter`:** Маршрутизатор для WebSocket-сообщений, использующий `websocket_urlpatterns` из приложения `apps`.

**Логика работы:**

1. **Загрузка настроек Django:** Устанавливается переменная окружения `DJANGO_SETTINGS_MODULE` для загрузки настроек проекта.
2. **Создание маршрутизатора:** Создается объект `ProtocolTypeRouter`, который направляет запросы либо на HTTP-обработчик Django, либо на WebSocket-маршрутизатор.
3. **Обработка WebSocket-сообщений:** Для WebSocket-сообщений используется `AuthMiddlewareStack` для аутентификации и `URLRouter` для маршрутизации к соответствующим обработчикам, определенным в `websocket_urlpatterns`.

**Использование:**

Этот модуль должен быть указан как точка входа для ASGI сервера (например, в файле `wsgi.py`).
"""

import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from apps.routing import websocket_urlpatterns

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'methods.settings')

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AuthMiddlewareStack(
        URLRouter(
            websocket_urlpatterns
        )
    ),
})
