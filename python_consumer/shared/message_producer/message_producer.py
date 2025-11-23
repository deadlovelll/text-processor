
import json

import aio_pika
from aio_pika.abc import AbstractExchange

from client import MessageClient


class MessageProducer:
    
    __slots__ = ('_client')
    
    def __init__(
        self,
        client: MessageClient = MessageClient(),
    ) -> None:
        
        self._client = client
    
    async def produce(
        self, 
        data: dict,
        connection,
    ) -> None:
        
        exchange: AbstractExchange = await self._client.get_exchnage(
            connection,
            "message_exchange",
        )
        message = aio_pika.Message(
            body=json.dumps(data).encode("utf-8")
        )
        await exchange.publish(message, routing_key="message_exchange")