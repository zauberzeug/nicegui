from typing import Protocol


class Section(Protocol):

    @property
    def name(self) -> str:
        ...

    @property
    def title(self) -> str:
        ...

    def intro(self) -> None:
        ...

    def content(self) -> None:
        ...
