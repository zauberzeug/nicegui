from dataclasses import dataclass, field
from typing import Any, Dict, List, NewType, Tuple

from typing_extensions import Self

from ..dataclasses import KWONLY_SLOTS
from .leaflet_layer import Layer

LatLng = NewType("LatLng", Tuple[float, float])

@dataclass(**KWONLY_SLOTS)
class GenericLayer(Layer):
    name: str
    args: List[Any] = field(default_factory=list)

    def to_dict(self) -> Dict:
        return {
            'type': self.name,
            'args': self.args,
        }


@dataclass(**KWONLY_SLOTS)
class TileLayer(Layer):
    url_template: str
    options: Dict = field(default_factory=dict)

    def to_dict(self) -> Dict:
        return {
            'type': 'tileLayer',
            'args': [self.url_template, self.options],
        }


@dataclass(**KWONLY_SLOTS)
class WmsLayer(Layer):
    url_template: str
    options: Dict = field(default_factory=dict)

    def to_dict(self) -> Dict:
        return {
            'type': 'tileLayer.wms',
            'args': [self.url_template, self.options],
        }


@dataclass(**KWONLY_SLOTS)
class Marker(Layer):
    latlng: Tuple[float, float]
    options: Dict = field(default_factory=dict)

    def to_dict(self) -> Dict:
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

@dataclass(**KWONLY_SLOTS)
class _Path(Layer):
    """Base class for leaflet Path types"""
    def redraw(self):
        raise NotImplementedError

@dataclass(**KWONLY_SLOTS)
class Polyline(_Path):
    """Draw a polyline overlay on the map.
    """

    latlngs: List[LatLng] = field(default_factory=list)
    options: Dict = field(default_factory=dict)

    def to_dict(self) -> Dict:
        return {
                'type': 'polyline',
                'args': [self.latlngs, self.options]
                }

    def addLatLng(self, latlng: LatLng):
        """Add a new point to the polyline.

        :param latlng: Latitude, longitude coordinates
        """
        self.run_method('addLatLng', latlng)

    def setLatLngs(self, latlngs: List[LatLng]):
        """Replace all points in the polyline with the given list

        :param latlngs List of geographic points
        """
        self.run_method('setLatLngs', latlngs)

@dataclass(**KWONLY_SLOTS)
class CircleMarker(_Path):
    """A circle of fixed size with radius specified in pixels.
    """

    latlng: LatLng = field(default_factory=tuple)
    options: Dict = field(default_factory=dict)

    def to_dict(self) -> Dict:
        return {
            'type': 'circleMarker',
            'args': [self.latlng, self.options]
        }
    
    def setLatLng(self, latlng: LatLng):
        """Set the center position of the circle marker to a new location.

        :param latlng: Coordinates (latitude, longitude)
        """
        self.latlng = latlng
        self.run_method('setLatLng', latlng)

    def setRadius(self, radius: float):
        """Set the radius of the circle

        :param radius: Radius of the circle, in pixels
        """
        self.run_method('setRadius', radius)

@dataclass
class Circle(CircleMarker):
    """Draws circle overlays on a map. Extends CircleMarker
    """
    
    def to_dict(self) -> Dict:
        return {
            'type': 'circle',
            'args': [self.latlng, self.options]
        }

