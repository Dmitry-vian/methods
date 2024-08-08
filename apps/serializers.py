from rest_framework import serializers
from .models import CommandsResult
from .models import Employee


class CommandsResultSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели CommandsResult, представляющей результаты выполнения команд.

    Преобразует объекты модели CommandsResult в формат JSON, подходящий для передачи через API.
    Используется для представления результатов выполнения системных команд, таких как ifconfig или ipconfig.

    Fields:
    - command (str): Название выполненной команды.
    - name (str): Имя сетевого интерфейса или файла, связанного с командой.
    - output (str): Текстовый вывод команды.

    Пример сериализованных данных:
    ```json
    {
    "command": "ifconfig",
    "name": "eth0",
    "output": "eth0: flags=4163<UP,BROADCAST,RUNNING,MULTICAST>  mtu 1500"
    }
    ```
    """
    class Meta:
        model = CommandsResult
        fields = ['command', 'name', 'output']


class EmployeeSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели Employee, представляющей информацию о сотруднике.

    Преобразует объекты модели Employee в формат JSON, подходящий для передачи через API.
    Используется для представления данных о сотрудниках в системе.

    Fields:
    - id (int): Уникальный идентификатор сотрудника.
    - first_name (str): Имя сотрудника.
    - email (str): Адрес электронной почты сотрудника.

    Пример сериализованных данных:
    ```json
    {"id": 1,
    "first_name": "Иван",
    "email": "[удаленный электронный адрес]"}
    ```
    """
    class Meta:
        model = Employee
        fields = ['id', 'first_name', 'email']
