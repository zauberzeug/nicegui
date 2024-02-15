from __future__ import annotations

import abc
from typing import (
    Any,
    Callable,
    Collection,
    Dict,
    Iterable,
    List,
    Optional,
    SupportsIndex,
    Union,
)

from . import events


class ObservableCollection(abc.ABC):
    """
    An abstract base class for observable collections.

    This class provides a foundation for creating collections that can be observed for changes.
    It allows registering change handlers and propagating change events to the registered handlers.

    Attributes:
        change_handlers (List[Callable]): A list of all change handlers registered on this collection and its parents.

    Methods:
        on_change(handler: Callable) -> None:
            Register a handler to be called when the collection changes.

    """

    def __init__(self, *,
                 factory: Callable,
                 data: Optional[Collection],
                 on_change: Optional[Callable],
                 _parent: Optional[ObservableCollection],
                 ) -> None:
        """
        Initializes a new instance of the ObservableCollection class.

        Args:
            factory (Callable): A callable object that creates a new instance of the collection.
            data (Optional[Collection]): The initial data for the collection.
            on_change (Optional[Callable]): A callback function to be called when the collection changes.
            _parent (Optional[ObservableCollection]): The parent collection of this collection.

        """
        super().__init__(factory() if data is None else data)  # type: ignore
        self._parent = _parent
        self._change_handlers: List[Callable] = [on_change] if on_change else []

    @property
    def change_handlers(self) -> List[Callable]:
        """
        Return a list of all change handlers registered on this collection and its parents.

        Returns:
            List[Callable]: A list of change handlers.

        """
        change_handlers = self._change_handlers[:]
        if self._parent is not None:
            change_handlers.extend(self._parent.change_handlers)
        return change_handlers

    def _handle_change(self) -> None:
        """
        Handle the change event by calling all registered change handlers.

        """
        for handler in self.change_handlers:
            events.handle_event(handler, events.ObservableChangeEventArguments(sender=self))

    def on_change(self, handler: Callable) -> None:
        """
        Register a handler to be called when the collection changes.

        Args:
            handler (Callable): The handler function to be registered.

        """
        self._change_handlers.append(handler)

    def _observe(self, data: Any) -> Any:
        """
        Observe the given data and return an observable version of it.

        Args:
            data (Any): The data to be observed.

        Returns:
            Any: The observable version of the data.

        """
        if isinstance(data, dict):
            return ObservableDict(data, _parent=self)
        if isinstance(data, list):
            return ObservableList(data, _parent=self)
        if isinstance(data, set):
            return ObservableSet(data, _parent=self)
        return data


class ObservableDict(ObservableCollection, dict):

    def __init__(self,
                 data: Dict = None,  # type: ignore
                 *,
                 on_change: Optional[Callable] = None,
                 _parent: Optional[ObservableCollection] = None,
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
        super().__ior__(self._observe(dict(other)))
        self._handle_change()
        return self


class ObservableList(ObservableCollection, list):
    """
        A dictionary subclass that provides observation capabilities.

        This class extends the functionality of the built-in `dict` class by adding observation capabilities.
        It inherits from the `ObservableCollection` class, which provides the observation functionality.

        Usage:
        - Create an instance of `ObservableDict` by passing an optional initial `data` dictionary.
        - Specify an optional `on_change` callback function to be called whenever the dictionary changes.
        - The `_parent` parameter is used internally and should not be set manually.

        Example:
        ```
        def handle_change():
            print("Dictionary changed!")

        my_dict = ObservableDict(on_change=handle_change)
        my_dict["key1"] = "value1"  # Triggers the `on_change` callback
        my_dict.update({"key2": "value2"})  # Triggers the `on_change` callback
        ```

        Methods:
        - `pop(k: Any, d: Any = None) -> Any`: Remove and return the value associated with key `k`. If `k` is not found, return `d` (default to `None`).
        - `popitem() -> Any`: Remove and return an arbitrary `(key, value)` pair from the dictionary.
        - `update(*args: Any, **kwargs: Any) -> None`: Update the dictionary with the key/value pairs from `*args` and `**kwargs`.
        - `clear() -> None`: Remove all items from the dictionary.
        - `setdefault(__key: Any, __default: Any = None) -> Any`: If `__key` is in the dictionary, return its value. If not, insert `__key` with a value of `__default` and return `__default`.
        - `__setitem__(__key: Any, __value: Any) -> None`: Set the value of `__key` to `__value`.
        - `__delitem__(__key: Any) -> None`: Remove `__key` from the dictionary.
        - `__or__(other: Any) -> Any`: Return the union of the dictionary and `other`.
        - `__ior__(other: Any) -> Any`: Update the dictionary with the union of itself and `other`.

        Note:
        - The observation capabilities are provided by the `ObservableCollection` base class.
        - The `ObservableDict` class overrides certain methods to ensure that changes to the dictionary trigger the `on_change` callback.
        """
    def __init__(self,
                 data: List = None,  # type: ignore
                 *,
                 on_change: Optional[Callable] = None,
                 _parent: Optional[ObservableCollection] = None,
                 ) -> None:
        super().__init__(factory=list, data=data, on_change=on_change, _parent=_parent)
        for i, item in enumerate(self):
            super().__setitem__(i, self._observe(item))

    def append(self, item: Any) -> None:
            """
            Appends an item to the observable list.

            Args:
                item (Any): The item to be appended.

            Returns:
                None

            Raises:
                None
            """
            super().append(self._observe(item))
            self._handle_change()

    def extend(self, iterable: Iterable) -> None:
            """
            Extends the observable list by appending elements from the given iterable.

            Args:
                iterable (Iterable): An iterable containing elements to be appended to the list.

            Returns:
                None

            Raises:
                None
            """
            super().extend(self._observe(list(iterable)))
            self._handle_change()

    def insert(self, index: SupportsIndex, obj: Any) -> None:
            """
            Inserts the given object at the specified index in the observable list.

            Args:
                index (SupportsIndex): The index at which the object should be inserted.
                obj (Any): The object to be inserted.

            Returns:
                None

            Raises:
                TypeError: If the index is not a valid index type.
            
            Notes:
                - This method internally observes the inserted object using the `_observe` method.
                - After inserting the object, it calls the `_handle_change` method to notify any observers of the change.
            """
            super().insert(index, self._observe(obj))
            self._handle_change()

    def remove(self, value: Any) -> None:
            """
            Removes the specified value from the observable list.

            Args:
                value (Any): The value to be removed.

            Returns:
                None

            Raises:
                None

            Notes:
                This method removes the specified value from the observable list.
                After removing the value, it triggers the `_handle_change` method
                to notify any observers of the change.
            """
            super().remove(value)
            self._handle_change()

    def pop(self, index: SupportsIndex = -1) -> Any:
            """
            Remove and return an item from the observable list.

            Args:
                index (Optional): The index of the item to remove. Defaults to -1, which removes the last item.

            Returns:
                Any: The removed item.

            Raises:
                IndexError: If the index is out of range.

            This method removes and returns an item from the observable list. It also triggers a change event to notify
            any observers of the list that a change has occurred.
            """
            item = super().pop(index)
            self._handle_change()
            return item

    def clear(self) -> None:
            """
            Clears the observable object.

            This method clears the observable object by calling the `clear` method of the base class
            and then triggers the `_handle_change` method to notify any observers of the change.

            Returns:
                None
            """
            super().clear()
            self._handle_change()

    def sort(self, **kwargs: Any) -> None:
        """
        Sorts the elements in the observable.

        This method sorts the elements in the observable in ascending order
        based on the provided sorting criteria. The sorting is performed in-place,
        meaning that the original order of the elements will be modified.

        Args:
            **kwargs: Additional keyword arguments to customize the sorting behavior.
                These arguments are passed to the underlying sorting algorithm.

        Returns:
            None

        Raises:
            Any exceptions raised by the underlying sorting algorithm.
        """
        super().sort(**kwargs)
        self._handle_change()

    def reverse(self) -> None:
        super().reverse()
        self._handle_change()

    def __delitem__(self, key: Union[SupportsIndex, slice]) -> None:
        super().__delitem__(key)
        self._handle_change()

    def __setitem__(self, key: Union[SupportsIndex, slice], value: Any) -> None:
        super().__setitem__(key, self._observe(value))
        self._handle_change()

    def __add__(self, other: Any) -> Any:
        return super().__add__(other)

    def __iadd__(self, other: Any) -> Any:
        super().__iadd__(self._observe(other))
        self._handle_change()
        return self


class ObservableSet(ObservableCollection, set):
    """
    A subclass of `ObservableCollection` that represents an observable set.

    An `ObservableSet` is a collection that behaves like a set and provides
    notifications when its contents change. It inherits from both `ObservableCollection`
    and `set`.

    ```

    Parameters:
    - data (set, optional): The initial data to populate the set with. Defaults to None.
    - on_change (Callable, optional): A callback function to be called when the set changes. Defaults to None.
    - _parent (ObservableCollection, optional): The parent collection, if any. Defaults to None.

    Methods:
    - add(item: Any) -> None: Adds an item to the set.
    - remove(item: Any) -> None: Removes an item from the set.
    - discard(item: Any) -> None: Removes an item from the set if it is present.
    - pop() -> Any: Removes and returns an arbitrary item from the set.
    - clear() -> None: Removes all items from the set.
    - update(*s: Iterable[Any]) -> None: Updates the set with the union of itself and other iterables.
    - intersection_update(*s: Iterable[Any]) -> None: Updates the set with the intersection of itself and other iterables.
    - difference_update(*s: Iterable[Any]) -> None: Updates the set with the difference of itself and other iterables.
    - symmetric_difference_update(*s: Iterable[Any]) -> None: Updates the set with the symmetric difference of itself and other iterables.
    - __or__(other: Any) -> Any: Returns the union of the set and another set.
    - __ior__(other: Any) -> Any: Updates the set with the union of itself and another set.
    - __and__(other: Any) -> set: Returns the intersection of the set and another set.
    - __iand__(other: Any) -> Any: Updates the set with the intersection of itself and another set.
    - __sub__(other: Any) -> set: Returns the difference of the set and another set.
    - __isub__(other: Any) -> Any: Updates the set with the difference of itself and another set.
    - __xor__(other: Any) -> set: Returns the symmetric difference of the set and another set.
    - __ixor__(other: Any) -> Any: Updates the set with the symmetric difference of itself and another set.
    """

    def __init__(self,
                 data: set = None,  # type: ignore
                 *,
                 on_change: Optional[Callable] = None,
                 _parent: Optional[ObservableCollection] = None,
                 ) -> None:
        """
        Initialize an ObservableSet.

        Args:
            data (set, optional): The initial data to populate the set with. Defaults to None.
            on_change (Callable, optional): A callback function to be called when the set changes. Defaults to None.
            _parent (ObservableCollection, optional): The parent collection, if any. Defaults to None.

        Returns:
            None
        """
        super().__init__(factory=set, data=data, on_change=on_change, _parent=_parent)
        for item in self:
            super().add(self._observe(item))

    def add(self, item: Any) -> None:
        """
        Add an item to the observable set.

        This method adds the specified item to the observable set. The item will be observed
        for any changes and the `_handle_change()` method will be called after the item is added.

        Args:
            item (Any): The item to be added to the set.

        Returns:
            None
        """
        super().add(self._observe(item))
        self._handle_change()

    def remove(self, item: Any) -> None:
        """
        Removes the specified item from the observable set.

        Args:
            item (Any): The item to be removed.

        Returns:
            None

        Raises:
            None

        Notes:
            This method removes the specified item from the observable set.
            After removing the item, it triggers the `_handle_change()` method
            to notify any observers of the change.
        """
        super().remove(item)
        self._handle_change()

    def discard(self, item: Any) -> None:
        """
        Removes the specified item from the observable set if it is present.

        Args:
            item (Any): The item to be removed.

        Returns:
            None
        """
        super().discard(item)
        self._handle_change()

    def pop(self) -> Any:
        """
        Removes and returns an arbitrary item from the observable set.

        Returns:
            Any: The removed item.

        Raises:
            KeyError: If the set is empty.
        """
        item = super().pop()
        self._handle_change()
        return item

    def clear(self) -> None:
        """
        Removes all items from the observable set.

        Returns:
            None
        """
        super().clear()
        self._handle_change()

    def update(self, *s: Iterable[Any]) -> None:
        """
        Updates the set with the union of itself and other iterables.

        Args:
            *s (Iterable[Any]): The iterables to update the set with.

        Returns:
            None
        """
        super().update(self._observe(set(*s)))
        self._handle_change()

    def intersection_update(self, *s: Iterable[Any]) -> None:
        """
        Updates the set with the intersection of itself and other iterables.

        Args:
            *s (Iterable[Any]): The iterables to intersect the set with.

        Returns:
            None
        """
        super().intersection_update(*s)
        self._handle_change()

    def difference_update(self, *s: Iterable[Any]) -> None:
        """
        Updates the set with the difference of itself and other iterables.

        Args:
            *s (Iterable[Any]): The iterables to calculate the difference with.

        Returns:
            None
        """
        super().difference_update(*s)
        self._handle_change()

    def symmetric_difference_update(self, *s: Iterable[Any]) -> None:
        """
        Updates the set with the symmetric difference of itself and other iterables.

        Args:
            *s (Iterable[Any]): The iterables to calculate the symmetric difference with.

        Returns:
            None
        """
        super().symmetric_difference_update(*s)
        self._handle_change()

    def __or__(self, other: Any) -> Any:
        """
        Returns the union of the set and another set.

        Args:
            other (Any): The other set to perform the union with.

        Returns:
            Any: The union of the two sets.
        """
        return super().__or__(other)

    def __ior__(self, other: Any) -> Any:
        """
        Updates the set with the union of itself and another set.

        Args:
            other (Any): The other set to perform the union with.

        Returns:
            Any: The updated set.
        """
        super().__ior__(self._observe(other))
        self._handle_change()
        return self

    def __and__(self, other: Any) -> set:
        """
        Returns the intersection of the set and another set.

        Args:
            other (Any): The other set to perform the intersection with.

        Returns:
            set: The intersection of the two sets.
        """
        return super().__and__(other)

    def __iand__(self, other: Any) -> Any:
        """
        Updates the set with the intersection of itself and another set.

        Args:
            other (Any): The other set to perform the intersection with.

        Returns:
            Any: The updated set.
        """
        super().__iand__(self._observe(other))
        self._handle_change()
        return self

    def __sub__(self, other: Any) -> set:
        """
        Returns the difference of the set and another set.

        Args:
            other (Any): The other set to calculate the difference with.

        Returns:
            set: The difference of the two sets.
        """
        return super().__sub__(other)

    def __isub__(self, other: Any) -> Any:
        """
        Updates the set with the difference of itself and another set.

        Args:
            other (Any): The other set to calculate the difference with.

        Returns:
            Any: The updated set.
        """
        super().__isub__(self._observe(other))
        self._handle_change()
        return self

    def __xor__(self, other: Any) -> set:
        """
        Returns the symmetric difference of the set and another set.

        Args:
            other (Any): The other set to calculate the symmetric difference with.

        Returns:
            set: The symmetric difference of the two sets.
        """
        return super().__xor__(other)

    def __ixor__(self, other: Any) -> Any:
        """
        Updates the set with the symmetric difference of itself and another set.

        Args:
            other (Any): The other set to calculate the symmetric difference with.

        Returns:
            Any: The updated set.
        """
        super().__ixor__(self._observe(other))
        self._handle_change()
        return self
