from dataclasses import dataclass, field
from typing import Any

from typing_extensions import Self

from .leaflet_layer import Layer


@dataclass(kw_only=True, slots=True)
class GenericLayer(Layer):
    name: str
    args: list[Any] = field(default_factory=list)

    def to_dict(self) -> dict:
        return {
            'type': self.name,
            'args': self.args,
        }


@dataclass(kw_only=True, slots=True)
class TileLayer(Layer):
    url_template: str
    options: dict = field(default_factory=dict)

    def to_dict(self) -> dict:
        return {
            'type': 'tileLayer',
            'args': [self.url_template, self.options],
        }


@dataclass(kw_only=True, slots=True)
class WmsLayer(Layer):
    url_template: str
    options: dict = field(default_factory=dict)

    def to_dict(self) -> dict:
        return {
            'type': 'tileLayer.wms',
            'args': [self.url_template, self.options],
        }


@dataclass(kw_only=True, slots=True)
class ImageOverlay(Layer):
    url: str
    bounds: list[list[float]]
    options: dict = field(default_factory=dict)

    def to_dict(self) -> dict:
        return {
            'type': 'imageOverlay',
            'args': [self.url, self.bounds, self.options],
        }


@dataclass(kw_only=True, slots=True)
class VideoOverlay(Layer):
    url: str | list[str]
    bounds: list[list[float]]
    options: dict = field(default_factory=dict)

    def to_dict(self) -> dict:
        return {
            'type': 'videoOverlay',
            'args': [self.url, self.bounds, self.options],
        }


@dataclass(kw_only=True, slots=True)
class Marker(Layer):
    latlng: tuple[float, float]
    options: dict = field(default_factory=dict)

    def to_dict(self) -> dict:
        return {
            'type': 'marker',
            'args': [{'lat': self.latlng[0], 'lng': self.latlng[1]}, self.options],
        }

    def draggable(self, value: bool = True) -> Self:
        """Make the marker draggable."""
        self.options['draggable'] = value
        return self

    def move(self, lat: float, lng: float) -> None:
        """Move the marker to a new position.

        :param lat: latitude
        :param lng: longitude
        """
        self.latlng = (lat, lng)
        self.run_method('setLatLng', (lat, lng))
