import asyncio
from asyncio import AbstractEventLoop, Task
import json
from typing import Generator
from concurrent.futures import InterpreterPoolExecutor

from aio_pika.abc import (
    AbstractMessage,
    AbstractConnection,
)

from client import MessageClient
from shared.message_processor import MessageProcessor
from parallel_consumer.worker_count import WorkerCountGetter
from shared.text_splitter import TextSplitter
from shared.message_producer import MessageProducer
from shared.result_merger import ResultMerger


class ParallelConsumer:
    
    __slots__ = (
        '_client',
        '_message_processor',
        '_worker_counter',
        '_text_splitter',
        '_message_producer',
        '_result_merger',
    )
    
    def __init__(
        self,
        client: MessageClient = MessageClient(),
        message_processor: MessageProcessor = MessageProcessor(),
        worker_counter: WorkerCountGetter = WorkerCountGetter(),
        text_splitter: TextSplitter = TextSplitter(),
        message_producer: MessageProducer = MessageProducer(),
        result_merger: ResultMerger = ResultMerger(),
    ) -> None:
        
        self._client = client
        self._message_processor = message_processor
        self._worker_counter = worker_counter
        self._text_splitter = text_splitter
        self._message_producer = message_producer
        self._result_merger = result_merger
    
    async def consume(
        self, 
        message: AbstractMessage, 
        connection: AbstractConnection,
    ) -> None:
        
        count: int = self._worker_counter.get() 
        loop: AbstractEventLoop = asyncio.get_running_loop()
        executor: InterpreterPoolExecutor = InterpreterPoolExecutor(
            max_workers=count
        )
        print('message received')
        tasks: list[Task] = []
        results: list[dict[str, int | dict[str, int]]] = []
        decoded_msg = json.loads(message.body.decode('utf-8'))
        blocks: list[str] = decoded_msg['value'].split('\n')
        blocks = [
            b.split('\t', 1)[1] 
            if '\t' in b else b 
            for b in blocks
        ]
        if len(blocks) == 1:
            return
        chunks: Generator[list[str], None, None] = self._text_splitter.gen(
            blocks, 
            count,
        )
        print('start to process the text')
        async with asyncio.TaskGroup() as tg:
            for chunk in chunks:
                task = tg.create_task(
                    self._run_task(loop, executor, chunk)
                )
                tasks.append(task)
        for task in tasks:  
            result = task.result()
            results.append(result)
        
        merged_result = self._result_merger.merge(results)
        agg_message = {
            'taskId': decoded_msg['taskId'],
            'all': decoded_msg['all'],
            'stats': merged_result,
        }
        print(f'pre-merged result: {merged_result}')
        await self._message_producer.produce(agg_message, connection)
        print('message sent to aggregator')
                    
    async def _run_task(
        self, 
        loop: AbstractEventLoop, 
        executor: InterpreterPoolExecutor, 
        data: list,
    ) -> dict[str, int | dict[str, int]]:
        
        result: dict[str, int | dict[str, int]]
        result = await loop.run_in_executor(
            executor,
            self._message_processor.process,
            data,
        )
        return result