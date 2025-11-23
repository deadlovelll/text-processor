from typing import Generator

class TextSplitter:
    
    def gen(
        self, 
        text: list[str], 
        worker_count: int,
    ) -> Generator[list[str], None, None]:
        
        batch_size = int(len(text) / worker_count)
        for i in range(0, len(text), batch_size):
            yield text[i:i+batch_size]