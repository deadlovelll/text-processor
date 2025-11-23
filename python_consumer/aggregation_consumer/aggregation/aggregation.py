import asyncio

from aio_pika.abc import (
    AbstractRobustConnection, 
    AbstractQueue, 
    AbstractMessage,
)

from client import MessageClient
from aggregation_consumer.consumer import AggregationConsumer


class AggregationCollector:
    
    __slots__ = (
        '_consumer',
        '_client',
    )
    
    def __init__(
        self,
        consumer: AggregationConsumer = AggregationConsumer(),
        client: MessageClient = MessageClient(),
    ) -> None:
        
        self._consumer = consumer
        self._client = client
        
    async def consume(self) -> None:
        message: AbstractMessage
        connection: AbstractRobustConnection = (
            await self._client.get_connection()
        )
        print('started aggregation consumer')
        async with connection:
            queue: AbstractQueue = await self._client.get_queue(
                connection, 
                'message_exchange'
            )
            async with queue.iterator() as queue_iter:
                async for message in queue_iter:
                    await self._consumer.consume(message)
                    await message.ack()
                    if queue.name in message.body.decode():
                        break
                    
if __name__ == '__main__':
    collector = AggregationCollector()
    asyncio.run(collector.consume())