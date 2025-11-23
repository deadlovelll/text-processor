import aio_pika
from aio_pika.abc import (
    AbstractRobustConnection, 
    AbstractQueue,
    AbstractChannel,
    AbstractExchange,
)


class MessageClient:
    
    def __init__(
        self,
    ) -> None:
        
        self.address: str = "amqp://guest:guest@rabbitmq:5672"
        
    async def get_connection(self) -> AbstractRobustConnection:
        connection: AbstractRobustConnection
        connection = await aio_pika.connect_robust(self.address)
        return connection
    
    async def get_queue(
        self,
        connection: AbstractRobustConnection,
        queue_name: str,
    ) -> AbstractQueue:
        
        channel: AbstractChannel = await connection.channel()
        await channel.set_qos(prefetch_count=1)
        queue: AbstractQueue = await channel.declare_queue(
            queue_name,
            auto_delete=False,
            durable=True
        )
                
        return queue
    
    async def get_exchnage(
        self,
        connection: AbstractRobustConnection,
    ) -> AbstractExchange:
        
        channel: AbstractChannel = await connection.channel()
        return channel.default_exchange