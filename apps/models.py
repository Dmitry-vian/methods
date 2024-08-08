from django.db import models


class CommandsResult(models.Model):
    """
    Модель для хранения информации о результатах выполнения команды ifconfig.

    Атрибуты:
        command (CharField): Название команды.
        name (CharField): Имя сетевого интерфейса или созданного файла.
        output (TextField): Текстовый вывод команды.
    """
    command = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    output = models.TextField()


class Employee(models.Model):
    """
    Модель для представления сотрудника.

    Каждый объект этой модели соответствует одному сотруднику.

    Attributes:
        id (AutoField): Уникальный идентификатор сотрудника (автоинкрементное поле).
        first_name (CharField): Имя сотрудника.
        email (EmailField): Электронная почта сотрудника.
    """
    id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=50)
    email = models.EmailField(max_length=150)



