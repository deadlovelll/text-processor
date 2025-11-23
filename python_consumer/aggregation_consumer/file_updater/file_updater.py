import json

from aggregation_consumer.sentiment_getter import SentimentGetter
from shared.result_merger import ResultMerger


class FileUpdater:
    
    __slots__ = (
        '_results_merger',
        '_sentiment_getter'
    )
    
    def __init__(
        self,
        results_merger: ResultMerger = ResultMerger(),
        sentiment_getter: SentimentGetter = SentimentGetter(),
    ) -> None:

        self._results_merger = results_merger
        self._sentiment_getter = sentiment_getter
    
    def update(self, filepath: str, stat) -> None:
        with open(filepath, 'r+') as f:
            file_data = json.load(f)
            initial_data = file_data['stats']
            merged_result = self._results_merger.merge(
                stat, 
                initial_data,
            )
            f.seek(0)
            f.truncate()
            file_data['recevied'] = file_data['recevied'] + 1
            file_data['stats'] = merged_result
            if file_data['received'] == file_data['all']:
                sentiment_percent: str = self._sentiment_getter.get(file_data)
                file_data['stats']['sentiment'] = sentiment_percent
            json.dump(file_data, f)
            print(f'merged result is: {merged_result}')