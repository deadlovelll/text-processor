import json
from typing import Union

from aggregation_consumer.stat_finalizer import StatFinalizer


class FileWriter:
    
    __slots__ = ('_stat_finalizer')
    
    def __init__(
        self,
        stat_finalizer: StatFinalizer = StatFinalizer(),
    ) -> None:
        
        self._stat_finalizer = stat_finalizer
    
    def write(
        self, 
        all: int, 
        filepath: str, 
        file_data: dict[
            str, Union[str,  dict[str, int | list[tuple[str, int]]]]
        ],
    ) -> None:
        
        print(file_data)
        with open(filepath, 'a') as f:
            if all == 1:
                self._stat_finalizer.finalize(file_data, file_data['taskId'])
            data = {
                'all': all,
                'received': 1,
                'stats': file_data['stats'],
            }
            data['stats']['start_time'] = file_data['start']         
            f.write(json.dumps(data))