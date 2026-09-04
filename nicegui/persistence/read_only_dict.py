from collections.abc import Iterator, MutableMapping
from typing import Any


class ReadOnlyDict(MutableMapping):

    def __init__(self, data: dict[Any, Any], write_error_message: str = 'Read-only dict') -> None:
        self._data: dict[Any, Any] = data
        self._write_error_message: str = write_error_message

    def __getitem__(self, item: Any) -> Any:
        return self._data[item]

    def __setitem__(self, key: Any, value: Any) -> None:
        raise TypeError(self._write_error_message)

    def __delitem__(self, key: Any) -> None:
        raise TypeError(self._write_error_message)

    def __iter__(self) -> Iterator:
        return iter(self._data)

    def __len__(self) -> int:
        return len(self._data)
