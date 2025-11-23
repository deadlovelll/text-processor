from typing import Union


class SentimentGetter:
    
    def get(
        self, 
        file_data: dict[
            str, Union[str,  dict[str, int | list[tuple[str, int]]]]
        ],
    ) -> str:
        
        bad_words: int = file_data['stats']['bad_words']
        words: int = file_data['stats']['word_count']
        percent_from_words: float = words / 100
        sentiment: float = bad_words / percent_from_words
        sentiment_percent: str = f'{round(sentiment, 2)}%'
        return sentiment_percent