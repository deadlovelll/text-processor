import json


class FileWriter:
    
    def write(self, all:int, filepath: str, stat) -> None:
        with open(filepath, 'a') as f:
            data = {
                'all': all,
                'recevied': 0,
                'stats': stat,
            }
            f.write(json.dumps(data))