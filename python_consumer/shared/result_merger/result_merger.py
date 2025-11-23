from collections import Counter


class ResultMerger:
    
    def merge(
        self, 
        inital: list[dict[str, int | dict[str, int]]],
        merged_result: dict[str, int | dict[str, int]] | None = None,
    ) -> dict[str, int | list[tuple]]:
        
        if not merged_result:
            merged_result = {
                'word_count': 0,
                'bad_words': 0,
                'names': 0,
                'top_5': [],
            }

        all_top_words: list[tuple] = []

        for r in inital:
            merged_result['word_count'] += r['word_count']
            merged_result['bad_words'] += r['bad_words']
            merged_result['names'] += r['names']
            all_top_words.extend(r['top_5'])
                    
        counter: Counter = Counter(all_top_words)
        merged_result['top_5'] = [word for word, _ in counter.most_common(5)]
        return merged_result