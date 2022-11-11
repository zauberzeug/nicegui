from abc import ABC, abstractmethod


class Updatable(ABC):

    @abstractmethod
    def update(self) -> None:
        pass
