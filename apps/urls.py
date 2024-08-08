from rest_framework.routers import DefaultRouter
from django.urls import path
from apps.views import SystemCommands, get_employee_count, get_employee_by_id

router = DefaultRouter()
router.register(r'systemcommands', SystemCommands, basename='systemcommands')
urlpatterns = router.urls + [
    path('employee_count/', get_employee_count, name='employee_count'),
    path('employee/<int:employee_id>/', get_employee_by_id, name='get_employee_by_id'),
]
"""
**Список URL-паттернов для API.**

Определяет набор URL-адресов для взаимодействия с API, используя `DefaultRouter` для автоматической генерации стандартных маршрутов для представлений (ViewSet).

* **`router.register(r'systemcommands', SystemCommands, basename='systemcommands')`:**
    - Регистрирует ViewSet `SystemCommands` для обработки запросов, связанных с системными командами.
    - Создает URL-паттерны для стандартных HTTP-методов (GET, POST, PUT, DELETE) для объектов `SystemCommands`.
    - Базовое имя `systemcommands` используется для формирования имен URL.

* **`path('employee_count/', get_employee_count, name='employee_count')`:**
    - Определяет URL-паттерн для получения общего количества сотрудников.
    - Функция `get_employee_count` будет вызвана при запросе по этому адресу.

* **`path('employee/<int:employee_id>/', get_employee_by_id, name='get_employee_by_id')`:**
    - Определяет URL-паттерн для получения информации о конкретном сотруднике по его идентификатору.
    - Функция `get_employee_by_id` будет вызвана при запросе по этому адресу с указанным идентификатором в URL.

**Пример использования:**

* **Получение списка всех системных команд:** `GET /systemcommands/`
* **Получение информации о конкретной системной команде:** `GET /systemcommands/<id>/`
* **Получение общего количества сотрудников:** `GET /employee_count/`
* **Получение информации о сотруднике с ID 1:** `GET /employee/1/`
"""