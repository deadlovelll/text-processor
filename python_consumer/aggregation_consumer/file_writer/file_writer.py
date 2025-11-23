from datetime import datetime, timezone
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
                sentiment_percent = self._sentiment_getter.get(file_data)
                current_ts = datetime.now(timezone.utc).isoformat()
                file_data['stats'].update({
                    'sentiment': sentiment_percent,
                    'start_time': file_data['start'],
                    'end_time': current_ts,
                    'time_spent': (
                        datetime.fromisoformat(current_ts) 
                        - datetime.fromisoformat(file_data['start'])
                    ).total_seconds()
                })
            data = {
                'all': all,
                'recevied': 1,
                'stats': file_data['stats'],
            }                
            f.write(json.dumps(data))