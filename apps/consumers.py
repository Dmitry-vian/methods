import json
import asyncio
import asyncpg
from channels.generic.websocket import AsyncWebsocketConsumer
import logging

logger = logging.getLogger(__name__)


class EmployeeConsumer(AsyncWebsocketConsumer):
    """
    Вебсокет-консьюмер для обработки запросов и уведомлений о сотрудниках.

    Этот консьюмер обрабатывает соединения с веб-клиентами,
    заинтересованными в данных о сотрудниках. Он может получать JSON-сообщения,
    содержащие идентификаторы записей, извлекать данные о сотрудниках из
    базы данных PostgreSQL и отправлять ответы обратно клиенту.
    Кроме того, он может слушать уведомления базы данных и транслировать их
    подключенным клиентам.
    """
    async def connect(self):
        """
        Подключается к вебсокету и пулу соединений с базой данных.

        Этот метод пытается установить вебсокет-соединение и создать пул
        соединений с базой данных PostgreSQL.
        В случае успеха он добавляет консьюмер в канал "employees"
        и запускает задачу для прослушивания уведомлений базы данных.
        """
        try:
            await self.channel_layer.group_add("employees", self.channel_name)
            await self.accept()
            self.db_pool = await asyncpg.create_pool(dsn='postgresql://postgres:GooGleMaN@localhost/dmitry')
            asyncio.create_task(self.listen_for_notifications())
            logger.info(f"Вебсокет подключен: {self.channel_name}")

        except Exception as e:
            logger.error(f"Ошибка подключения вебсокета или прослушивания уведомлений: {e}")

    async def disconnect(self, close_code):
        """
        Отключается от вебсокета и закрывает пул соединений с базой данных.

        Этот метод удаляет консьюмер из канала "employees",
        закрывает пул соединений с базой данных и
        записывает информацию об отключении.
        """
        try:
            await self.channel_layer.group_discard("employees", self.channel_name)
            await self.db_pool.close()
            logger.info(f"Вебсокет отключен: {self.channel_name}, код: {close_code}")

        except Exception as e:
            logger.error(f"Ошибка отключения от вебсокета: {e}")

    async def receive(self, text_data):
        """
        Обрабатывает входящие JSON-сообщения, содержащие идентификаторы записей сотрудников.

        Этот метод получает JSON-строку от клиента, анализирует ее и
        извлекает поле "record_id". Если идентификатор отсутствует,
        отправляется сообщение об ошибке.
        В противном случае он извлекает данные о сотруднике из базы данных
        и отправляет ответ клиенту. Он обрабатывает потенциальные ошибки
        во время разбора JSON, операций с базой данных и других исключений.
        """
        try:
            data = json.loads(text_data)
            record_id = data.get("record_id")

            if record_id is None:
                await self.send(text_data=json.dumps({"error": "Не указан идентификатор записи"}))
                return

            async with self.db_pool.acquire() as conn:
                query = "SELECT * FROM employee WHERE id = $1"  # Выбираем все поля для проверки
                result = await conn.fetchrow(query, record_id)

                if result:
                    await self.send(text_data=json.dumps(dict(result)))
                else:
                    await self.send(text_data=json.dumps({"error": "Запись не найдена"}))
        except (ValueError, asyncpg.exceptions.InvalidDataError) as e:
            # Обработка ошибок при парсинге JSON и работе с базой данных
            await self.send(text_data=json.dumps({"error": str(e)}))
        except Exception as e:
            # Обработка других исключений
            await self.send(text_data=json.dumps({"error": "Произошла внутренняя ошибка", "error_code": 404}))

        except Exception as e:
            logger.error(f"Error processing request: {e}")
            await self.send(text_data=json.dumps({"error": "Internal server error", "error_code": 500}))


    async def listen_for_notifications(self):
        try:
            async with self.db_pool.acquire() as conn:
                await conn.add_listener('data_update', self.handle_notification)
                logger.info("Listening for notifications on 'data_update' channel")
        except Exception as e:
            logger.error(f"Error in listen_for_notifications: {e}")

    async def handle_notification(self, connection, pid, channel, payload):
        try:
            logger.info(f"Notification received: {payload}")
            await self.send(text_data=payload)
        except Exception as e:
            logger.error(f"Failed to send notification: {e}")

    async def async_send_message(self, event):  # Имя метода изменено
        try:
            # Отправка уведомления клиенту через WebSocket
            await self.send(text_data=json.dumps(event["message"]))
        except Exception as e:
            logger.error(f"Failed to send message: {e}")