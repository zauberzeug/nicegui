from __future__ import annotations

import uuid
from abc import abstractmethod
from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Any, ClassVar

from ...awaitable_response import AwaitableResponse
from ...dataclasses import KWONLY_SLOTS

if TYPE_CHECKING:
    from .leaflet import Leaflet


@dataclass(**KWONLY_SLOTS)
class Layer:
    current_leaflet: ClassVar[Leaflet | None] = None
    leaflet: Leaflet = field(init=False)
    id: str = field(init=False)

    def __post_init__(self) -> None:
        self.id = str(uuid.uuid4())
        assert self.current_leaflet is not None
        self.leaflet = self.current_leaflet
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
