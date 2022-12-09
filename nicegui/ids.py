from typing import Dict


class IncrementingIds:
    '''Generates incrementing IDs'''

    def __init__(self) -> None:
        self.current_id = -1

    def get(self) -> int:
        self.current_id += 1
        return self.current_id


class IncrementingStringIds:
    '''Maps incrementing IDs to given strings'''

    def __init__(self) -> None:
        self.current_id = -1
        self.dict: Dict[str, int] = {}

    def get(self, name: str) -> int:
        if name not in self.dict:
            self.current_id += 1
            self.dict[name] = self.current_id
        return self.dict[name]
