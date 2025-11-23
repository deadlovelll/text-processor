import json
from typing import Union

from aggregation_consumer.stat_finalizer import StatFinalizer
from shared.result_merger import ResultMerger


class FileUpdater:
    
    __slots__ = (
        '_results_merger',
        '_stat_finalizer'
    )
    
    def __init__(
        self,
        results_merger: ResultMerger = ResultMerger(),
        stat_finalizer: StatFinalizer = StatFinalizer(),
    ) -> None:

        self._results_merger = results_merger
        self._stat_finalizer = stat_finalizer
    
    def update(
        self, 
        filepath: str, 
        data: dict[str, Union[str,  dict[str, int | list[tuple[str, int]]]]],
    ) -> None:
        
        file_data: dict[str, Union[str,  dict[str, int | list[tuple[str, int]]]]]
        initial_data: dict[str, int | list[tuple[str, int]]]
        merged_result: dict[str, int | list[tuple[str, int]]]
        
        with open(filepath, 'r+') as f:
            file_data = json.load(f)
            initial_data = file_data['stats']
            merged_result = self._results_merger.merge(
                [data['stats']], 
                initial_data,
            )
            file_data['stats'] = merged_result
            file_data['received'] = file_data.get('received', 0) + 1
            
            if file_data['received'] == file_data['all']:
                self._stat_finalizer.finalize(file_data, data['taskId'])

            f.seek(0)
            f.truncate()
            json.dump(file_data, f)
            print(f'merged result is: {merged_result}')