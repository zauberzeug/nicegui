from __future__ import annotations

import abc
import weakref
from collections.abc import Callable, Collection, Iterable, Iterator
from contextlib import contextmanager
from copy import deepcopy
from time import time
from typing import TYPE_CHECKING, Any, ClassVar, Generic, SupportsIndex, TypeVar

from typing_extensions import Self

from . import core, events

if TYPE_CHECKING:
    from .element import Element

T = TypeVar('T', bound='Element')

# Deeply-immutable types that never need ObservableDict/List/Set wrapping overhead.
_OBSERVABLE_UNCHANGED_TYPES = frozenset({str, int, float, bool, type(None), tuple, bytes, frozenset})


class ObservableCollection(abc.ABC):  # noqa: B024

    def __init__(self, *,
                 factory: Callable,
                 data: Collection | None,
                 on_change: Callable | None,
                 _parent: ObservableCollection | None,
                 ) -> None:
        super().__init__(factory() if data is None else data)  # type: ignore
        self._parent = _parent
        self.last_modified = time()
        self._change_handlers: list[Callable] = [on_change] if on_change else []

    @property
    def change_handlers(self) -> list[Callable]:
        """Return a list of all change handlers registered on this collection and its parents."""
        change_handlers = self._change_handlers[:]
        if self._parent is not None:
            change_handlers.extend(self._parent.change_handlers)
        return change_handlers

    def _handle_change(self) -> None:
        self.last_modified = time()
        # Skip dispatch when a root collection has no registered change handlers.
        if self._parent is None and not self._change_handlers:
            return
        # Parent-chained collections or multiple handlers: use full dispatch for every handler.
        if self._parent is not None or len(self._change_handlers) != 1:
            for handler in self.change_handlers:
                events.handle_observable_change(handler, self)
            return
        # Optimised path: single handler on a root collection (no parent delegation).
        self._handle_single_root_change()

    def _handle_single_root_change(self) -> None:
        """Dispatch to the sole root-level handler, trying the direct hook first."""
        handler = self._change_handlers[0]
        try:
            if self._handle_direct_change_handler(handler):
                return
        except Exception as e:
            core.app.handle_exception(e)
            return
        events.handle_observable_change(handler, self)

    def _handle_direct_change_handler(self, handler: Callable) -> bool:
        """Subclass hook: process a known change handler without argument dispatch.

        _handle_change tries this hook before building ObservableChangeEventArguments
        and running expects_arguments checks. Return True to claim the handler and
        stop normal dispatch. Return False (the default) to let normal dispatch proceed.

        Props, Classes, and Style use ElementBoundObservableMixin to intercept their own _update
        handler and skip event-argument overhead on every mutation.
        """
        return False

    def on_change(self, handler: Callable) -> None:
        """Register a handler to be called when the collection changes."""
        if handler != self._handle_change:  # pylint: disable=comparison-with-callable
            self._change_handlers.append(handler)

    def _observe(self, data: Any) -> Any:
        """Wrap *data* in an observable collection, or register a change handler if it is already one.

        Uses ``type(data) is`` for the exact built-in types (avoids ``isinstance``
        MRO overhead), then :class:`ObservableCollection` so subclasses like
        ``ObservableDict`` register rather than re-wrap, then ``isinstance`` for
        any remaining dict/list/set subclasses.
        """
        data_type = type(data)
        if data_type in _OBSERVABLE_UNCHANGED_TYPES:
            return data
        if data_type is dict:
            return ObservableDict(data, _parent=self)
        if data_type is list:
            return ObservableList(data, _parent=self)
        if data_type is set:
            return ObservableSet(data, _parent=self)
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


class ElementBoundObservableMixin(Generic[T]):
    """Observable collection behavior shared by Props, Classes, and Style.

    Concrete classes still initialize their ObservableDict/ObservableList base with
    ``on_change=self._update``; this mixin binds that handler to the owning element
    and provides the shared hot-path dispatch and update-suspension behavior.
    """

    _element_kind: ClassVar[str]
    _change_handlers: list[Callable]
    _element: weakref.ReferenceType[T]
    _update_handler: Callable
    _suspend_count: int

    def _bind_element(self, element: T) -> None:
        self._update_handler = self._change_handlers[0]
        self._element = weakref.ref(element)
        self._suspend_count = 0

    def _update(self) -> None:
        """Update the bound element after a collection change."""
        raise NotImplementedError

    @contextmanager
    def suspend_updates(self) -> Iterator[None]:
        """Suspend updates."""
        self._suspend_count += 1
        try:
            yield
        finally:
            self._suspend_count -= 1

    def _handle_direct_change_handler(self, handler: Callable) -> bool:
        """Run _update directly, skipping ObservableChangeEventArguments dispatch.

        Generic dispatch builds event arguments and checks expects_arguments.
        Skip both when the handler is our own _update. Claim the handler even
        when suspended: suspended mutations should not fall through to generic dispatch.
        """
        if handler is self._update_handler:
            self._update()
            return True
        return False

    @property
    def element(self) -> T:
        """The element this observable collection belongs to."""
        element = self._element()
        if element is None:
            raise RuntimeError(f'The element this {self._element_kind} object belongs to has been deleted.')
        return element


class ObservableDict(ObservableCollection, dict):

    def __init__(self,
                 data: dict | None = None,
                 *,
                 on_change: Callable | None = None,
                 _parent: ObservableCollection | None = None,
                 ) -> None:
        super().__init__(factory=dict, data=data, on_change=on_change, _parent=_parent)
        if self:
            for key, value in self.items():
                dict.__setitem__(self, key, self._observe(value))

    def pop(self, k: Any, d: Any = None) -> Any:
        item = dict.pop(self, k, d)
        self._handle_change()
        return item

    def popitem(self) -> Any:
        item = dict.popitem(self)
        self._handle_change()
        return item

    def update(self, *args: Any, **kwargs: Any) -> None:
        dict.update(self, self._observe(dict(*args, **kwargs)))
        self._handle_change()

    def clear(self) -> None:
        dict.clear(self)
        self._handle_change()

    def setdefault(self, __key: Any, __default: Any = None) -> Any:
        item = dict.setdefault(self, __key, self._observe(__default))
        self._handle_change()
        return item

    def __setitem__(self, __key: Any, __value: Any) -> None:
        if type(__value) not in _OBSERVABLE_UNCHANGED_TYPES:
            __value = self._observe(__value)
        dict.__setitem__(self, __key, __value)
        self._handle_change()

    def __delitem__(self, __key: Any) -> None:
        dict.__delitem__(self, __key)
        self._handle_change()

    def __or__(self, other: Any) -> Any:
        return dict.__or__(self, other)

    def __ior__(self, other: Any) -> Any:
        other_dict = self._observe(dict(other))
        dict.__ior__(self, other_dict)
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
        if self:
            for i, item in enumerate(self):
                list.__setitem__(self, i, self._observe(item))

    def append(self, item: Any) -> None:
        if type(item) not in _OBSERVABLE_UNCHANGED_TYPES:
            item = self._observe(item)
        list.append(self, item)
        self._handle_change()

    def extend(self, iterable: Iterable) -> None:
        list.extend(self, self._observe(list(iterable)))
        self._handle_change()

    def insert(self, index: SupportsIndex, obj: Any) -> None:
        list.insert(self, index, self._observe(obj))
        self._handle_change()

    def remove(self, value: Any) -> None:
        list.remove(self, value)
        self._handle_change()

    def pop(self, index: SupportsIndex = -1) -> Any:
        item = list.pop(self, index)
        self._handle_change()
        return item

    def clear(self) -> None:
        list.clear(self)
        self._handle_change()

    def sort(self, **kwargs: Any) -> None:
        list.sort(self, **kwargs)
        self._handle_change()

    def reverse(self) -> None:
        list.reverse(self)
        self._handle_change()

    def __delitem__(self, key: SupportsIndex | slice) -> None:
        list.__delitem__(self, key)
        self._handle_change()

    def __setitem__(self, key: SupportsIndex | slice, value: Any) -> None:
        list.__setitem__(self, key, self._observe(value))
        self._handle_change()

    def __add__(self, other: Any) -> Any:
        return list.__add__(self, other)

    def __iadd__(self, other: Any) -> Any:
        list.__iadd__(self, self._observe(other))
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
        if self:
            for item in self:
                set.add(self, self._observe(item))

    def add(self, item: Any) -> None:
        set.add(self, self._observe(item))
        self._handle_change()

    def remove(self, item: Any) -> None:
        set.remove(self, item)
        self._handle_change()

    def discard(self, item: Any) -> None:
        set.discard(self, item)
        self._handle_change()

    def pop(self) -> Any:
        item = set.pop(self)
        self._handle_change()
        return item

    def clear(self) -> None:
        set.clear(self)
        self._handle_change()

    def update(self, *s: Iterable[Any]) -> None:
        set.update(self, self._observe(set(*s)))
        self._handle_change()

    def intersection_update(self, *s: Iterable[Any]) -> None:
        set.intersection_update(self, *s)
        self._handle_change()

    def difference_update(self, *s: Iterable[Any]) -> None:
        set.difference_update(self, *s)
        self._handle_change()

    def symmetric_difference_update(self, *s: Iterable[Any]) -> None:
        set.symmetric_difference_update(self, *s)
        self._handle_change()

    def __or__(self, other: Any) -> Any:
        return set.__or__(self, other)

    def __ior__(self, other: Any) -> Any:
        set.__ior__(self, self._observe(other))
        self._handle_change()
        return self

    def __and__(self, other: Any) -> set:
        return set.__and__(self, other)

    def __iand__(self, other: Any) -> Any:
        set.__iand__(self, self._observe(other))
        self._handle_change()
        return self

    def __sub__(self, other: Any) -> set:
        return set.__sub__(self, other)

    def __isub__(self, other: Any) -> Any:
        set.__isub__(self, self._observe(other))
        self._handle_change()
        return self

    def __xor__(self, other: Any) -> set:
        return set.__xor__(self, other)

    def __ixor__(self, other: Any) -> Any:
        set.__ixor__(self, self._observe(other))
        self._handle_change()
        return self
