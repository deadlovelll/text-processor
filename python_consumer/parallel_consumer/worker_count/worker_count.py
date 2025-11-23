import psutil


class WorkerCountGetter:
    
    def get(self) -> int:
        count: int | None = psutil.cpu_count()
        if not count:
            count = 1
        return int(count / 2)