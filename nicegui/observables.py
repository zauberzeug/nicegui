from typing import Any, Callable, Dict, Iterable, List, overload


class ObservableDict(dict):

    def __init__(self, on_change: Callable, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        for key, value in self.items():
            super().__setitem__(key, make_observable(value, on_change))
        self.on_change = on_change

    def pop(self, k: Any, d: Any = None) -> Any:
        item = super().pop(k, d)
        self.on_change()
        return item

    def popitem(self) -> Any:
        item = super().popitem()
        self.on_change()
        return item

    def update(self, *args: Any, **kwargs: Any) -> None:
        super().update(make_observable(dict(*args, **kwargs), self.on_change))
        self.on_change()

    def clear(self) -> None:
        super().clear()
        self.on_change()

    def setdefault(self, __key: Any, __default: Any = None) -> Any:
        item = super().setdefault(__key, make_observable(__default, self.on_change))
        self.on_change()
        return item

    def __setitem__(self, __key: Any, __value: Any) -> None:
        super().__setitem__(__key, make_observable(__value, self.on_change))
        self.on_change()

    def __delitem__(self, __key: Any) -> None:
        super().__delitem__(__key)
        self.on_change()

    def __ior__(self, other: Any) -> Any:
        super().__ior__(make_observable(other, self.on_change))
        self.on_change()
        return self


class ObservableList(list):

    def __init__(self, on_change: Callable, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        for i, item in enumerate(self):
            super().__setitem__(i, make_observable(item, on_change))
        self.on_change = on_change

    def append(self, item: Any) -> None:
        super().append(make_observable(item, self.on_change))
        self.on_change()

    def extend(self, iterable: Iterable) -> None:
        super().extend(make_observable(iterable, self.on_change))
        self.on_change()

    def insert(self, index: int, object: Any) -> None:
        super().insert(index, make_observable(object, self.on_change))
        self.on_change()

    def remove(self, value: Any) -> None:
        super().remove(value)
        self.on_change()

    def pop(self, index: int = -1) -> Any:
        item = super().pop(index)
        self.on_change()
        return item

    def clear(self) -> None:
        super().clear()
        self.on_change()

    def sort(self, **kwargs: Any) -> None:
        super().sort(**kwargs)
        self.on_change()

    def reverse(self) -> None:
        super().reverse()
        self.on_change()

    def __delitem__(self, key: int) -> None:
        super().__delitem__(key)
        self.on_change()

    def __setitem__(self, key: int, value: Any) -> None:
        super().__setitem__(key, make_observable(value, self.on_change))
        self.on_change()

    def __setslice__(self, i: int, j: int, sequence: Any) -> None:
        super().__setslice__(i, j, make_observable(sequence, self.on_change))
        self.on_change()

    def __delslice__(self, i: int, j: int) -> None:
        super().__delslice__(i, j)
        self.on_change()

    def __iadd__(self, other: Any) -> Any:
        super().__iadd__(make_observable(other, self.on_change))
        self.on_change()
        return self


@overload
def make_observable(d: Dict, on_change: Callable) -> ObservableDict:
    ...


@overload
def make_observable(d: List, on_change: Callable) -> ObservableList:
    ...


def make_observable(a: Any, on_change: Callable) -> Any:
    if isinstance(a, dict):
        return ObservableDict(on_change, a)
    if isinstance(a, list):
        return ObservableList(on_change, a)
    return a
