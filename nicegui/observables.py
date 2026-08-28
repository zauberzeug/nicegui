from __future__ import annotations

import abc
import time
import weakref
from collections.abc import Callable, Collection, Iterable
from collections.abc import Set as AbstractSet
from copy import deepcopy
from types import EllipsisType
from typing import TYPE_CHECKING, SupportsIndex, TypeVar, cast, overload

from typing_extensions import Self

from . import events, helpers

if TYPE_CHECKING:
    from _typeshed import SupportsKeysAndGetItem, SupportsRichComparison

_T = TypeVar('_T')
_T2 = TypeVar('_T2')
_KT = TypeVar('_KT')
_VT = TypeVar('_VT')
_KT2 = TypeVar('_KT2')
_VT2 = TypeVar('_VT2')


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
        self._change_handlers: list[tuple[Callable, bool]] = \
            [(on_change, helpers.expects_arguments(on_change))] if on_change else []
        self._observer_refs: list[weakref.ref[ObservableCollection]] = []

    @property
    def _parent(self) -> ObservableCollection | None:
        return self._parent_ref() if self._parent_ref is not None else None

    @_parent.setter
    def _parent(self, parent: ObservableCollection | None) -> None:
        # the reference is weak so that items don't keep discarded parent collections alive
        self._parent_ref = weakref.ref(parent) if parent is not None else None

    @property
    def change_handlers(self) -> list[Callable]:
        """Return a list of all change handlers registered on this collection and its parents and observers."""
        return [handler for handler, _ in self._change_handlers_with_args]

    @property
    def _change_handlers_with_args(self) -> list[tuple[Callable, bool]]:
        """Return change handlers with pre-resolved ``expect_args`` flag, including those of parents and observers."""
        change_handlers = self._change_handlers[:]
        observers = [ref() for ref in self._observer_refs]
        change_handlers.extend((observer._handle_change, False)  # pylint: disable=protected-access
                               for observer in observers if observer is not None)
        if self._parent is not None:
            change_handlers.extend(self._parent._change_handlers_with_args)  # pylint: disable=protected-access
        return change_handlers

    def _handle_change(self) -> None:
        self.last_modified = time.time()
        for handler, expect_args in self._change_handlers_with_args:
            events.handle_event(handler, events.ObservableChangeEventArguments(sender=self), expect_args=expect_args)

    def on_change(self, handler: Callable) -> None:
        """Register a handler to be called when the collection changes."""
        if handler != self._handle_change:  # pylint: disable=comparison-with-callable
            self._change_handlers.append((handler, helpers.expects_arguments(handler)))

    def _register_observer(self, observer: ObservableCollection) -> None:
        """Register a collection which contains this collection and should be notified about changes."""
        if observer is self or observer is self._parent:
            return
        alive_refs = [ref for ref in self._observer_refs if ref() is not None]
        if any(ref() is observer for ref in alive_refs):
            return
        self._observer_refs = [*alive_refs, weakref.ref(observer)]

    def _unregister_observer(self, observer: ObservableCollection) -> None:
        """Unregister a collection so that it is no longer notified about changes."""
        if self._parent is observer:
            self._parent = None
        self._observer_refs = [ref for ref in self._observer_refs if ref() is not None and ref() is not observer]

    @overload
    def _observe(self, data: dict[_KT, _VT]) -> ObservableDict[_KT, _VT]:
        ...

    @overload
    def _observe(self, data: list[_T]) -> ObservableList[_T]:
        ...

    @overload
    def _observe(self, data: set[_T]) -> ObservableSet[_T]:
        ...

    @overload
    def _observe(self, data: ObservableCollection) -> ObservableCollection:
        ...

    @overload
    def _observe(self, data: _T) -> _T:
        ...

    def _observe(self, data: _T | dict | list | set | ObservableCollection
                 ) -> _T | ObservableDict | ObservableList | ObservableSet | ObservableCollection:
        if isinstance(data, ObservableCollection):
            data._register_observer(self)  # pylint: disable=protected-access
            return data
        if isinstance(data, dict):
            return ObservableDict(data, _parent=self)
        if isinstance(data, list):
            return ObservableList(data, _parent=self)
        if isinstance(data, set):
            return ObservableSet(data, _parent=self)
        return data

    def _unobserve(self, *items: object) -> None:
        removed = [item for item in items if isinstance(item, ObservableCollection)]
        if not removed:
            return
        values: Iterable = self.values() if isinstance(self, dict) else cast(Iterable, self)
        contained_ids = {id(value) for value in values if isinstance(value, ObservableCollection)}
        for item in removed:
            if id(item) not in contained_ids:
                item._unregister_observer(self)  # pylint: disable=protected-access

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

    def __reduce__(self) -> tuple[type[Self], tuple]:
        # reconstruct from plain contents so that the observer wiring (weak references, which are not picklable)
        # is rebuilt by __init__ instead of being pickled; a freshly loaded tree has no observers yet.
        if isinstance(self, dict):
            return ObservableDict, (dict(self),)
        if isinstance(self, list):
            return ObservableList, (list(self),)
        if isinstance(self, set):
            return ObservableSet, (set(self),)
        raise NotImplementedError(f'ObservableCollection.__reduce__ not implemented for {type(self)}')


class ObservableDict(ObservableCollection, dict[_KT, _VT]):

    def __init__(self,
                 data: dict[_KT, _VT] | None = None,
                 *,
                 on_change: Callable | None = None,
                 _parent: ObservableCollection | None = None,
                 ) -> None:
        super().__init__(factory=dict, data=data, on_change=on_change, _parent=_parent)
        for key, value in self.items():
            super().__setitem__(key, self._observe(value))

    def pop(self, k: object, d: _T | EllipsisType = ...) -> _VT | _T:
        try:
            item = super().pop(cast(_KT, k))
        except KeyError:  # nothing was removed, so skip _unobserve/_handle_change below
            if d is ...:
                raise
            return d
        self._unobserve(item)
        self._handle_change()
        return item

    def popitem(self) -> tuple[_KT, _VT]:
        item = super().popitem()
        self._unobserve(item[1])
        self._handle_change()
        return item

    def update(self, m: SupportsKeysAndGetItem[_KT, _VT] | Iterable[tuple[_KT, _VT]] = (), /, **kwargs: _VT) -> None:
        new_items = cast(dict[_KT, _VT], dict(m, **kwargs))
        if not new_items:
            return
        old_values = [self[key] for key in new_items if key in self]
        super().update({key: self._observe(value) for key, value in new_items.items()})
        self._unobserve(*old_values)
        self._handle_change()

    def clear(self) -> None:
        values = list(self.values())
        super().clear()
        self._unobserve(*values)
        self._handle_change()

    @overload
    def setdefault(self: ObservableDict[_KT, _T | None], __key: _KT, __default: None = None) -> _T | None:
        ...

    @overload
    def setdefault(self, __key: _KT, __default: _VT) -> _VT:
        ...

    def setdefault(self, __key: _KT, __default: _VT | None = None) -> _VT | None:
        if __key in self:
            return super().__getitem__(__key)
        item = super().setdefault(__key, self._observe(cast(_VT, __default)))
        self._handle_change()
        return item

    def __setitem__(self, __key: _KT, __value: _VT) -> None:
        old_value = self.get(__key)
        super().__setitem__(__key, self._observe(__value))
        self._unobserve(old_value)
        self._handle_change()

    def __delitem__(self, __key: _KT) -> None:
        item = self[__key]
        super().__delitem__(__key)
        self._unobserve(item)
        self._handle_change()

    def __or__(self, other: dict[_KT2, _VT2]) -> dict[_KT | _KT2, _VT | _VT2]:
        return super().__or__(other)

    def __ior__(self,  # type: ignore[misc,override]  # See https://stackoverflow.com/a/78844946
                other:  SupportsKeysAndGetItem[_KT, _VT] | Iterable[tuple[_KT, _VT]]) -> Self:
        self.update(other)
        return self


class ObservableList(ObservableCollection, list[_T]):

    def __init__(self,
                 data: list[_T] | None = None,
                 *,
                 on_change: Callable | None = None,
                 _parent: ObservableCollection | None = None,
                 ) -> None:
        super().__init__(factory=list, data=data, on_change=on_change, _parent=_parent)
        for i, item in enumerate(self):
            super().__setitem__(i, self._observe(item))

    def append(self, item: _T) -> None:
        super().append(self._observe(item))
        self._handle_change()

    def extend(self, iterable: Iterable[_T]) -> None:
        items = [self._observe(item) for item in iterable]
        if not items:
            return
        super().extend(items)
        self._handle_change()

    def insert(self, index: SupportsIndex, obj: _T) -> None:
        super().insert(index, self._observe(obj))
        self._handle_change()

    def remove(self, value: _T) -> None:
        self.pop(super().index(value))

    def pop(self, index: SupportsIndex = -1) -> _T:
        item = super().pop(index)
        self._unobserve(item)
        self._handle_change()
        return item

    def clear(self) -> None:
        items = list(self)
        super().clear()
        self._unobserve(*items)
        self._handle_change()

    def sort(self, key: Callable[[_T], SupportsRichComparison] | None = None, reverse: bool = False) -> None:
        super().sort(key=key, reverse=reverse)
        self._handle_change()

    def reverse(self) -> None:
        super().reverse()
        self._handle_change()

    def __delitem__(self, key: SupportsIndex | slice[SupportsIndex | None]) -> None:
        items = self[key] if isinstance(key, slice) else [self[key]]
        super().__delitem__(key)
        self._unobserve(*items)
        self._handle_change()

    def __setitem__(self, key: SupportsIndex | slice[SupportsIndex | None], value: _T | Iterable[_T]) -> None:
        if isinstance(key, slice):
            old_items = self[key]
            super().__setitem__(key, [self._observe(item) for item in cast(Iterable[_T], value)])
            self._unobserve(*old_items)
        else:
            old_item = self[key]
            super().__setitem__(key, self._observe(cast(_T, value)))
            self._unobserve(old_item)
        self._handle_change()

    def __add__(self, other: list[_T2]) -> list[_T | _T2]:
        return super().__add__(other)

    def __iadd__(self, other: Iterable[_T]) -> Self:  # type: ignore[misc,override]
        self.extend(other)
        return self

    def __mul__(self, other: SupportsIndex) -> list[_T]:
        return super().__mul__(other)

    def __imul__(self, other: SupportsIndex) -> Self:
        old_items = list(self)
        super().__imul__(other)
        if len(self) == len(old_items):
            return self
        self._unobserve(*old_items)
        self._handle_change()
        return self


class ObservableSet(ObservableCollection, set[_T]):

    def __init__(self,
                 data: set[_T] | None = None,
                 *,
                 on_change: Callable | None = None,
                 _parent: ObservableCollection | None = None,
                 ) -> None:
        super().__init__(factory=set, data=data, on_change=on_change, _parent=_parent)
        for item in self:
            super().add(self._observe(item))

    def add(self, item: _T) -> None:
        if item in self:
            return
        super().add(self._observe(item))
        self._handle_change()

    def remove(self, item: _T) -> None:
        super().remove(item)
        self._unobserve(item)
        self._handle_change()

    def discard(self, item: object) -> None:
        if item in self:
            self.remove(cast(_T, item))

    def pop(self) -> _T:
        item = super().pop()
        self._unobserve(item)
        self._handle_change()
        return item

    def clear(self) -> None:
        items = list(self)
        super().clear()
        self._unobserve(*items)
        self._handle_change()

    def update(self, *s: Iterable[_T]) -> None:
        items = set().union(*s)
        if items <= self:
            return
        super().update({self._observe(item) for item in items})
        self._handle_change()

    def intersection_update(self, *s: Iterable[object]) -> None:
        old_items = list(self)
        super().intersection_update(*s)
        if len(self) == len(old_items):
            return
        self._unobserve(*old_items)
        self._handle_change()

    def difference_update(self, *s: Iterable[object]) -> None:
        old_items = list(self)
        super().difference_update(*s)
        if len(self) == len(old_items):
            return
        self._unobserve(*old_items)
        self._handle_change()

    def symmetric_difference_update(self, *s: Iterable[_T]) -> None:
        items = set().union(*s)
        if not items:
            return
        old_items = list(self)
        super().symmetric_difference_update({self._observe(item) for item in items})
        self._unobserve(*old_items)
        self._handle_change()

    def __or__(self, other: AbstractSet[_T2]) -> set[_T | _T2]:
        return super().__or__(other)

    def __ior__(self, other: AbstractSet[_T]) -> Self:  # type: ignore[misc,override]
        self.update(other)
        return self

    def __and__(self, other: AbstractSet[object]) -> set[_T]:
        return super().__and__(other)

    def __iand__(self, other: AbstractSet[object]) -> Self:
        self.intersection_update(other)
        return self

    def __sub__(self, other: AbstractSet[object]) -> set[_T]:
        return super().__sub__(cast(AbstractSet, other))

    def __isub__(self, other: AbstractSet[object]) -> Self:
        self.difference_update(other)
        return self

    def __xor__(self, other: AbstractSet[_T2]) -> set[_T | _T2]:
        return super().__xor__(other)

    def __ixor__(self, other: AbstractSet[_T]) -> Self:  # type: ignore[misc,override]
        self.symmetric_difference_update(other)
        return self
