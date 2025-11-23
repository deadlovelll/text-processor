class TextSplitter:
    
    def gen(self, text: list, worker_count: int):
        batch_size = int(len(text) / worker_count)
        for i in range(0, len(text), batch_size):
            yield text[i:i+batch_size]