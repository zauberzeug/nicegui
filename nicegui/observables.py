from __future__ import annotations

import abc
import time
from collections.abc import Callable, Collection, Iterable
from copy import deepcopy
from typing import Any, SupportsIndex

from typing_extensions import Self

from . import events


class ObservableCollection(abc.ABC):  # noqa: B024

    def __init__(self, *,
                 factory: Callable,
                 data: Collection | None,
                 on_change: Callable | None,
                 _parent: ObservableCollection | None,
                 ) -> None:
        super().__init__(factory() if data is None else data)  # type: ignore
        self._parent = _parent
        self.last_modified = time.time()
        self._change_handlers: list[Callable] = [on_change] if on_change else []

    @property
    def change_handlers(self) -> list[Callable]:
        """Return a list of all change handlers registered on this collection and its parents."""
        change_handlers = self._change_handlers[:]
        if self._parent is not None:
            change_handlers.extend(self._parent.change_handlers)
        return change_handlers

    def _handle_change(self) -> None:
        self.last_modified = time.time()
        for handler in self.change_handlers:
            events.handle_event(handler, events.ObservableChangeEventArguments(sender=self))

    def on_change(self, handler: Callable) -> None:
        """Register a handler to be called when the collection changes."""
        if handler != self._handle_change:  # pylint: disable=comparison-with-callable
            self._change_handlers.append(handler)

    def _observe(self, data: Any) -> Any:
        if isinstance(data, ObservableCollection):
            data.on_change(self._handle_change)
            return data
        if isinstance(data, dict):
            return ObservableDict(data, _parent=self)
        if isinstance(data, list):
            return ObservableList(data, _parent=self)
        if isinstance(data, set):
            return ObservableSet(data, _parent=self)
        return data

    def __copy__(self) -> Self:
        if isinstance(self, dict):
            return ObservableDict(self, _parent=self._parent)
        if isinstance(self, list):
            return ObservableList(self, _parent=self._parent)
        if isinstance(self, set):
            return ObservableSet(self, _parent=self._parent)
        raise NotImplementedError(f'ObservableCollection.__copy__ not implemented for {type(self)}')

    def __deepcopy__(self, memo: dict) -> Self:
        if isinstance(self, dict):
            return ObservableDict({key: deepcopy(self[key]) for key in self}, _parent=self._parent)
        if isinstance(self, list):
            return ObservableList([deepcopy(item) for item in self], _parent=self._parent)
        if isinstance(self, set):
            return ObservableSet({deepcopy(item) for item in self}, _parent=self._parent)
        raise NotImplementedError(f'ObservableCollection.__deepcopy__ not implemented for {type(self)}')


class ObservableDict(ObservableCollection, dict):

    def __init__(self,
                 data: dict | None = None,
                 *,
                 on_change: Callable | None = None,
                 _parent: ObservableCollection | None = None,
                 ) -> None:
        super().__init__(factory=dict, data=data, on_change=on_change, _parent=_parent)
        for key, value in self.items():
            super().__setitem__(key, self._observe(value))

    def pop(self, k: Any, d: Any = None) -> Any:
        item = super().pop(k, d)
        self._handle_change()
        return item

    def popitem(self) -> Any:
        item = super().popitem()
        self._handle_change()
        return item

    def update(self, *args: Any, **kwargs: Any) -> None:
        super().update(self._observe(dict(*args, **kwargs)))
        self._handle_change()

    def clear(self) -> None:
        super().clear()
        self._handle_change()

    def setdefault(self, __key: Any, __default: Any = None) -> Any:
        item = super().setdefault(__key, self._observe(__default))
        self._handle_change()
        return item

    def __setitem__(self, __key: Any, __value: Any) -> None:
        super().__setitem__(__key, self._observe(__value))
        self._handle_change()

    def __delitem__(self, __key: Any) -> None:
        super().__delitem__(__key)
        self._handle_change()

    def __or__(self, other: Any) -> Any:
        return super().__or__(other)

    def __ior__(self, other: Any) -> Any:
        other_dict = self._observe(dict(other))
        super().__ior__(other_dict)
        self._handle_change()
        return self


class ObservableList(ObservableCollection, list):

    def __init__(self,
                 data: list | None = None,
                 *,
                 on_change: Callable | None = None,
                 _parent: ObservableCollection | None = None,
                 ) -> None:
        super().__init__(factory=list, data=data, on_change=on_change, _parent=_parent)
        for i, item in enumerate(self):
            super().__setitem__(i, self._observe(item))

    def append(self, item: Any) -> None:
        super().append(self._observe(item))
        self._handle_change()

    def extend(self, iterable: Iterable) -> None:
        super().extend(self._observe(list(iterable)))
        self._handle_change()

    def insert(self, index: SupportsIndex, obj: Any) -> None:
        super().insert(index, self._observe(obj))
        self._handle_change()

    def remove(self, value: Any) -> None:
        super().remove(value)
        self._handle_change()

    def pop(self, index: SupportsIndex = -1) -> Any:
        item = super().pop(index)
        self._handle_change()
        return item

    def clear(self) -> None:
        super().clear()
        self._handle_change()

    def sort(self, **kwargs: Any) -> None:
        super().sort(**kwargs)
        self._handle_change()

    def reverse(self) -> None:
        super().reverse()
        self._handle_change()

    def __delitem__(self, key: SupportsIndex | slice) -> None:
        super().__delitem__(key)
        self._handle_change()

    def __setitem__(self, key: SupportsIndex | slice, value: Any) -> None:
        super().__setitem__(key, self._observe(value))
        self._handle_change()

    def __add__(self, other: Any) -> Any:
        return super().__add__(other)

    def __iadd__(self, other: Any) -> Any:
        super().__iadd__(self._observe(other))
        self._handle_change()
        return self


class ObservableSet(ObservableCollection, set):

    def __init__(self,
                 data: set | None = None,
                 *,
                 on_change: Callable | None = None,
                 _parent: ObservableCollection | None = None,
                 ) -> None:
        super().__init__(factory=set, data=data, on_change=on_change, _parent=_parent)
        for item in self:
            super().add(self._observe(item))

    def add(self, item: Any) -> None:
        super().add(self._observe(item))
        self._handle_change()

    def remove(self, item: Any) -> None:
        super().remove(item)
        self._handle_change()

    def discard(self, item: Any) -> None:
        super().discard(item)
        self._handle_change()

    def pop(self) -> Any:
        item = super().pop()
        self._handle_change()
        return item

    def clear(self) -> None:
        super().clear()
        self._handle_change()

    def update(self, *s: Iterable[Any]) -> None:
        super().update(self._observe(set(*s)))
        self._handle_change()

    def intersection_update(self, *s: Iterable[Any]) -> None:
        super().intersection_update(*s)
        self._handle_change()

    def difference_update(self, *s: Iterable[Any]) -> None:
        super().difference_update(*s)
        self._handle_change()

    def symmetric_difference_update(self, *s: Iterable[Any]) -> None:
        super().symmetric_difference_update(*s)
        self._handle_change()

    def __or__(self, other: Any) -> Any:
        return super().__or__(other)

    def __ior__(self, other: Any) -> Any:
        super().__ior__(self._observe(other))
        self._handle_change()
        return self

    def __and__(self, other: Any) -> set:
        return super().__and__(other)

    def __iand__(self, other: Any) -> Any:
        super().__iand__(self._observe(other))
        self._handle_change()
        return self

    def __sub__(self, other: Any) -> set:
        return super().__sub__(other)

    def __isub__(self, other: Any) -> Any:
        super().__isub__(self._observe(other))
        self._handle_change()
        return self

    def __xor__(self, other: Any) -> set:
        return super().__xor__(other)

    def __ixor__(self, other: Any) -> Any:
        super().__ixor__(self._observe(other))
        self._handle_change()
        return self
