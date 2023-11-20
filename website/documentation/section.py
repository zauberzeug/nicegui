from typing import Protocol


class Section(Protocol):

    @property
    def name(self) -> str:
        ...

    @property
    def title(self) -> str:
        ...

    @property
    def description(self) -> str:
        ...

    def content(self) -> None:
        ...
