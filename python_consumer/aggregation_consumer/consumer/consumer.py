from asyncio import Lock
import json
from pathlib import Path

from client import MessageClient
from shared.message_processor import MessageProcessor
from aggregation_consumer.file_writer import FileWriter
from aggregation_consumer.file_updater import FileUpdater

from aio_pika.abc import AbstractMessage


class AggregationConsumer:
    
    __slots__ = (
        '_client',
        '_message_processor',
        '_file_writer',
        '_file_updater'
    )
    
    def __init__(
        self,
        client: MessageClient = MessageClient(),
        message_processor: MessageProcessor = MessageProcessor(),
        file_writer: FileWriter = FileWriter(),
        file_updater: FileUpdater = FileUpdater(),
    ) -> None:
        
        self._client = client
        self._message_processor = message_processor
        self._file_writer = file_writer
        self._file_updater = file_updater
    
    async def consume(self, message: AbstractMessage) -> None:
        print('message received')
        data = json.loads(message.body.decode('utf-8'))
        print(data)
        task_id: str = data['taskId']
        all: int = data['all']
        filepath: str = f"results/{task_id}.json"
        file: Path = Path(filepath)
        lock = Lock()
        
        print(f'task id is {task_id}')
            
        async with lock:
            if not file.exists():
                self._file_writer.write(all, filepath, data)
            else:
                self._file_updater.update(filepath, data)