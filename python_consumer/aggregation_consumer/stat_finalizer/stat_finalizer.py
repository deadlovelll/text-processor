from datetime import datetime, timezone

from aggregation_consumer.sentiment_getter import SentimentGetter


class StatFinalizer:
    
    __slots__ = ('_sentiment_getter')
    
    def __init__(
        self,
        sentiment_getter: SentimentGetter = SentimentGetter(),
    ) -> None:
        
        self._sentiment_getter = sentiment_getter
    
    def finalize(self, file_data):
        current_ts = datetime.now(timezone.utc).isoformat()
        start_time = file_data['stats']['start_time']  
        file_data['stats'].update({
            'end_time': current_ts,
            'time_spent': (
                datetime.fromisoformat(current_ts) 
                - datetime.fromisoformat(start_time)
            ).total_seconds()
        })
        sentiment_percent = self._sentiment_getter.get(file_data)
        file_data['stats']['sentiment'] = sentiment_percent