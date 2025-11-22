import json

from shared.result_merger import ResultMerger


class FileUpdater:
    
    __slots__ = (
        '_results_merger',
    )
    
    def __init__(
        self,
        results_merger: ResultMerger = ResultMerger(),
    ) -> None:

        self._results_merger = results_merger
    
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
                bad_words: int = file_data['stats']['bad_words']
                words: int = file_data['stats']['word_count']
                percent_from_words: float = words / 100
                sentiment: float = bad_words / percent_from_words
                file_data['stats']['sentiment'] = sentiment
            json.dump(file_data, f)
            print(f'merged result is: {merged_result}')