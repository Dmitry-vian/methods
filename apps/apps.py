from django.apps import AppConfig
from .signals import listen_to_db
import threading


class AppsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps'

    def ready(self):
        """
        Запускает фоновый поток для прослушивания изменений в базе данных.

        Этот метод вызывается при загрузке приложения. Он создает и запускает
        фоновый поток, который будет постоянно отслеживать изменения в базе данных
        с помощью функции listen_to_db.
        """
        threading.Thread(target=listen_to_db, daemon=True).start()