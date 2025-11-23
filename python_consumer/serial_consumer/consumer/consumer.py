from client import MessageClient
from shared.message_processor import MessageProcessor

from aio_pika.abc import AbstractMessage


class SerialConsumer:
    
    __slots__ = (
        '_client',
        '_message_processor',
    )
    
    def __init__(
        self,
        client: MessageClient = MessageClient(),
        message_processor: MessageProcessor = MessageProcessor(),
    ) -> None:
        
        self._client = client
        self._message_processor = message_processor
    
    async def consume(self, message: AbstractMessage) -> None:
        print('message received')
        blocks: list[str] = message.body.decode('utf-8').split('\n')
        blocks = [
            b.split('\t', 1)[1] 
            if '\t' in b else b 
            for b in blocks
        ]
        if len(blocks) == 1:
            return
        self._message_processor.process(blocks)
        print('tasks performed')