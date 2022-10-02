from dataclasses import dataclass


@dataclass
class Data:
    progress: int = 0

    @property
    def progress_float(self) -> float:
        return self.progress / 100.0

    @property
    def progress_str(self) -> str:
        return f'{self.progress_float:1.0%}'
