import json

from aggregation_consumer.stat_finalizer import StatFinalizer


class FileWriter:
    
    __slots__ = ('_stat_finalizer')
    
    def __init__(
        self,
        stat_finalizer: StatFinalizer = StatFinalizer(),
    ) -> None:
        
        self._stat_finalizer = stat_finalizer
    
    def write(self, all: int, filepath: str, file_data) -> None:
        print(file_data)
        with open(filepath, 'a') as f:
            if all == 1:
                self._stat_finalizer.finalize(file_data)
            data = {
                'all': all,
                'recevied': 1,
                'stats': file_data['stats'],
            }                
            f.write(json.dumps(data))