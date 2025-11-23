from collections import Counter
from typing import Union

from tqdm import tqdm

from shared.profane_detector import ProfaneDetecor
from shared.name_detector import NameDetector


class MessageProcessor:
    
    __slots__ = (
        '_profane_detector',
        '_name_detector',
    )
    
    def __init__(
        self,
        profane_detector: ProfaneDetecor = ProfaneDetecor(),
        name_detector: NameDetector = NameDetector(),
    ) -> None:
        
        self._profane_detector = profane_detector
        self._name_detector = name_detector
    
    def process(
        self, 
        text: list[str],
    ) -> dict[str, Union[int, dict[str, int]]]:
        
        text.sort(key=lambda x: len(x))
        
        result = {
            'word_count': 0,
            'bad_words': 0,
            'names': 0,
            'top_5': [],
        }
        next_text = []
        
        for word in tqdm(text):
            splitted_word = word.split('_')
            for subword in splitted_word:
                if not subword:
                    continue
                result['word_count'] += 1
                is_profane = self._profane_detector.is_profane(word)
                if is_profane:
                    result['bad_words'] += 1
                is_name = self._name_detector.is_name(subword)
                if is_name:
                    result['names'] += 1

                next_text.append(subword)
                
        counter = Counter(next_text)
        top_5 = counter.most_common(5)
        result['top_5'] = top_5
        
        return result