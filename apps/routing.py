from django.urls import re_path
from apps.consumers import EmployeeConsumer


websocket_urlpatterns = [
    re_path(r'^ws/employees/$', EmployeeConsumer.as_asgi()),
]
"""
Список URL-паттернов для WebSocket-соединений.

Этот список определяет маршруты для WebSocket-соединений в вашем Django-приложении.
Каждый элемент списка представляет собой кортеж, состоящий из регулярного выражения для
сопоставления URL и соответствующего обработчика.

В данном случае, мы определяем один маршрут:

* **'^ws/employees/$'**: Регулярное выражение, которое соответствует URL-пути '/ws/employees/'. 
  Все запросы, соответствующие этому шаблону, будут направлены на обработчик 
  `EmployeeConsumer.as_asgi()`.

* **EmployeeConsumer.as_asgi()**: Это асинхронный обработчик WebSocket-соединений,
  определенный в модуле `apps.consumers`. Он будет обрабатывать входящие WebSocket-сообщения 
  и отправлять ответы клиентам.

**Использование:**
Когда клиент подключается к WebSocket-серверу по адресу '/ws/employees/', 
Django будет использовать класс `EmployeeConsumer` для обработки этого соединения.
"""