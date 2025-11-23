from shared.consts import EN_NAMES, STOPWORDS


class NameDetector:
    
    def is_name(self, word: str) -> bool:
        if word in EN_NAMES:
            return True
        
        return (
            word.istitle() and word.lower() 
            not in STOPWORDS and 2 <= len(word) <= 12
        )