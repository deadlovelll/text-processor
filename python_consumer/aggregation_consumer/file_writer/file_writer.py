import json

from aggregation_consumer.sentiment_getter import SentimentGetter


class FileWriter:
    
    __slots__ = ('_sentiment_getter')
    
    def __init__(
        self,
        sentiment_getter: SentimentGetter = SentimentGetter(),
    ) -> None:
        
        self._sentiment_getter = sentiment_getter
    
    def write(self, all: int, filepath: str, file_data) -> None:
        print(file_data)
        with open(filepath, 'a') as f:
            if all == 1:
                sentiment_percent: str = self._sentiment_getter.get(file_data)
                file_data['stats']['sentiment'] = sentiment_percent
            data = {
                'all': all,
                'recevied': 1,
                'stats': file_data['stats'],
            }                
            f.write(json.dumps(data))