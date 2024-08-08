from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import action, permission_classes, api_view
from rest_framework import status
from .models import CommandsResult, Employee
from .serializers import CommandsResultSerializer, EmployeeSerializer
import subprocess
import platform
import os


def execute_command(command):
    """
    Выполняет системную команду в терминале и возвращает ее вывод.

    Args:
        command (str): Команда для выполнения.

    Returns:
        str: Вывод команды в стандартный поток вывода или сообщение об ошибке.

    Raises:
        subprocess.CalledProcessError: Если при выполнении команды возникла ошибка.

    **Примечания:**
    * Использует `subprocess.run` для надежного и безопасного выполнения команд.
    * Автоматически определяет кодировку вывода в зависимости от операционной системы.
    """
    try:
        # Используем subprocess.run для более удобного интерфейса
        result = subprocess.run(command, shell=True, capture_output=True, text=True, check=True, encoding='cp866')
        return result.stdout
    except subprocess.CalledProcessError as e:
        return f"Ошибка выполнения команды: {e}"


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_employee_count(request):
    from rest_framework import viewsets
    from rest_framework.permissions import IsAuthenticated
    from rest_framework.response import Response
    from rest_framework.decorators import api_view
    from rest_framework import status
    from .models import Employee
    from .serializers import EmployeeSerializer

    @api_view(['GET'])
    @permission_classes([IsAuthenticated])
    def get_employee_count(request):
        """
    Получает общее количество сотрудников в системе.

    **Требуется авторизация.**

    **Ответ:**
    * `count` (int): Общее количество сотрудников.

    **Пример ответа:**
    ```json
    {
    "count": 10
    }
    ```
    """
    count = Employee.objects.count()
    return Response({'count': count})


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_employee_by_id(request, employee_id):
    """
    Получает информацию о конкретном сотруднике по его идентификатору.

    **Требуется авторизация.**

    **Параметры:**
    * `employee_id` (int): Уникальный идентификатор сотрудника.

    **Ответ:**
    * Сериализованные данные сотрудника, содержащие его поля (например, `id`, `first_name`, `email`).

    **Ошибки:**
    * `404 Not Found`: Если сотрудник с указанным идентификатором не найден.

    **Пример ответа (успешный):**
    ```json
    {
    "id": 1,
    "first_name": "Иван",
    "email": "[удаленный электронный адрес]"
    }
    ```
    **Пример ответа (ошибка):**
    ```json
    {
    "error": "Employee not found"
    }
    ```
    """
    try:
        employee = Employee.objects.get(id=employee_id)
        serializer = EmployeeSerializer(employee)
        return Response(serializer.data)
    except Employee.DoesNotExist:
        return Response({'error': 'Employee not found'}, status=404)


class SystemCommands(viewsets.ViewSet):
    """
    ViewSet для выполнения системных команд и сохранения результатов.

    Позволяет выполнять различные системные команды через API и сохранять их результаты в базе данных.
    Поддерживаемые команды:
    * `ifconfig` (или `ipconfig` на Windows): Получение информации о сетевых интерфейсах.
    * `touchfile`: Создание нового файла.

    **Методы:**
    * `command_ifconfig`: Выполняет команду `ifconfig` или `ipconfig`.
    * `command_touchfile`: Создает новый файл.

    **Результаты:**
    * Результаты выполнения команд сохраняются в базе данных в модели `CommandsResult`.
    * При успешном выполнении возвращается HTTP-код 201 (Создано) и сериализованные данные результата.
    * При ошибках возвращается соответствующий HTTP-код и сообщение об ошибке.
    """
    queryset = CommandsResult.objects.all()
    serializer_class = CommandsResultSerializer

    @action(detail=False, methods=['post'], url_path='ifconfig')
    def command_ifconfig(self, request):
        command = request.data.get('command')
        if command != 'ifconfig':
            return Response({'error': 'Неверная команда'}, status=status.HTTP_400_BAD_REQUEST)

        # Определяем команду в зависимости от ОС
        system_command = 'ipconfig' if platform.system() == 'Windows' else 'ifconfig'

        output = execute_command(system_command)
        ifconfig_instance = CommandsResult.objects.create(name=command, output=output)
        serializer = CommandsResultSerializer(ifconfig_instance)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=['post'], url_path='touchfile')
    def command_touchfile(self, request):
        filename = request.data.get('filename')
        if not filename:
            return Response({'error': 'Имя файла не указано'}, status=status.HTTP_400_BAD_REQUEST)

        if os.path.exists(filename):
            return Response({'error': 'Файл уже существует'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            with open(filename, 'w') as f:
                pass  # Файл будет создан при открытии
            touchfile_instance = CommandsResult.objects.create(name='touchfile', output=f"Файл {filename} создан")
            serializer = CommandsResultSerializer(touchfile_instance)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({'error': f'Ошибка создания файла: {e}'}, status=status.HTTP_400_BAD_REQUEST)
