from better_profanity import profanity


class ProfaneDetecor:
    
    def is_profane(self, word: str) -> bool:
        return profanity.contains_profanity(word)