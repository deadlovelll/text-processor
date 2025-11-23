import asyncio
import time

from aio_pika.abc import (
    AbstractRobustConnection, 
    AbstractQueue, 
    AbstractMessage,
)

from client import MessageClient
from serial_consumer.consumer import SerialConsumer


class SerialCollector:
    
    __slots__ = (
        '_consumer',
        '_client',
    )
    
    def __init__(
        self,
        consumer: SerialConsumer = SerialConsumer(),
        client: MessageClient = MessageClient(),
    ) -> None:
        
        self._consumer = consumer
        self._client = client
        
    async def consume(self) -> None:
        message: AbstractMessage
        connection: AbstractRobustConnection = (
            await self._client.get_connection()
        )
        async with connection:
            queue: AbstractQueue = await self._client.get_queue(
                connection, 
                'content_parse2'
            )
            async with queue.iterator() as queue_iter:
                async for message in queue_iter:
                    start: float = time.perf_counter()
                    await self._consumer.consume(message)
                    end: float = time.perf_counter()
                    print(f'Overall time: {end-start}')
                    await message.ack()
                    if queue.name in message.body.decode():
                        break
                    
if __name__ == '__main__':
    collector = SerialCollector()
    asyncio.run(collector.consume())