from __future__ import annotations

import uuid
import weakref
from abc import abstractmethod
from contextvars import ContextVar
from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Any, ClassVar

from ...awaitable_response import AwaitableResponse

if TYPE_CHECKING:
    from .leaflet import Leaflet


@dataclass(kw_only=True, slots=True)
class Layer:
    _current_leaflet: ClassVar[ContextVar[weakref.ref[Leaflet] | None]] = ContextVar('_current_leaflet', default=None)
    leaflet: Leaflet = field(init=False)
    id: str = field(init=False)

    def __post_init__(self) -> None:
        self.id = str(uuid.uuid4())
        leaflet_ref = Layer._current_leaflet.get()
        leaflet = leaflet_ref() if leaflet_ref is not None else None
        if leaflet is None:
            raise RuntimeError('The current map cannot be determined because no map has been entered in this task '
                               'or the map has been deleted.\n'
                               'This may happen if you create a layer from an event handler or a timer.\n'
                               'To fix this, enter the target map explicitly using `with map_element:`.')
        self.leaflet = leaflet
        self.leaflet.layers.append(self)
        self.leaflet.run_method('add_layer', self.to_dict(), self.id)

    @abstractmethod
    def to_dict(self) -> dict:
        """Return a dictionary representation of the layer."""

    def run_method(self, name: str, *args: Any, timeout: float = 1) -> AwaitableResponse:
        """Run a method of the Leaflet layer.

        If the function is awaited, the result of the method call is returned.
        Otherwise, the method is executed without waiting for a response.

        :param name: name of the method (a prefix ":" indicates that the arguments are JavaScript expressions)
        :param args: arguments to pass to the method
        :param timeout: timeout in seconds (default: 1 second)

        :return: AwaitableResponse that can be awaited to get the result of the method call
        """
        return self.leaflet.run_method('run_layer_method', self.id, name, *args, timeout=timeout)
