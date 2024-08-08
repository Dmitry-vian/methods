import psycopg2
import select
import json
import logging
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from psycopg2 import extensions


logger = logging.getLogger(__name__)


def listen_to_db():
    """
    Слушает уведомления о новых сотрудниках в базе данных PostgreSQL
    и транслирует их клиентам через WebSocket.

    Эта функция устанавливает соединение с базой данных PostgreSQL,
    подписывается на канал "new_employee" для получения уведомлений о новых записях,
    и затем входит в бесконечный цикл, ожидая уведомлений.

    - При получении уведомления, функция:
    - Декодирует полезную нагрузку уведомления из JSON
    - Записывает информацию о новом сотруднике в лог
    - Асинхронно отправляет сообщение всем клиентам, подключенным к группе "employees" через WebSocket-канал.

    Функция обрабатывает исключения и закрывает соединение с базой данных
    по завершении работы.

    **Ошибки:**
    - **RuntimeError**: Ошибки конфигурации канала, если он не настроен.
    """
    try:
        conn = psycopg2.connect("dbname=dmitry user=postgres password=GooGleMaN")
        conn.set_isolation_level(extensions.ISOLATION_LEVEL_AUTOCOMMIT)
        with conn.cursor() as cur:
            cur.execute("LISTEN new_employee;")
        channel_layer = get_channel_layer()

        if channel_layer is None:
            raise RuntimeError("Канал был неправильно настроен.")

        while True:
            if select.select([conn], [], [], 5) == ([], [], []):
                continue
            conn.poll()
            while conn.notifies:
                notify = conn.notifies.pop(0)
                payload = json.loads(notify.payload)
                logger.info(f"New employee added: {payload}")

                async_to_sync(channel_layer.group_send)(
                    "employees",
                    {
                        "type": "async_send_message",
                        "message": payload,
                    })
    except Exception as e:
        logger.error(f"Ошибка при прослушивании базы данных: {e}")
    finally:
        cur.close()
