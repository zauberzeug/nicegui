from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Tuple, cast

from ..binding import BindableProperty
from ..element import Element
from ..helpers import KWONLY_SLOTS


@dataclass(**KWONLY_SLOTS)
class LeafletLayer:
    url_template: str
    options: Dict

    @staticmethod
    def default() -> LeafletLayer:
        return LeafletLayer(url_template='http://{s}.tile.osm.org/{z}/{x}/{y}.png', options={
            'attribution': '&copy; <a href="https://openstreetmap.org/copyright">OpenStreetMap</a> contributors',
        })


class Leaflet(Element, component='leaflet.js'):
    location = BindableProperty(lambda sender, _: cast(Leaflet, sender).update())
    zoom = BindableProperty(lambda sender, _: cast(Leaflet, sender).update())

    def __init__(self, location: Tuple[float, float] = (0, 0), zoom: int = 13) -> None:
        super().__init__()
        self.layers = [LeafletLayer.default()]
        self.set_location(location)
        self.set_zoom(zoom)
        self.on('moveend', lambda e: self.set_location((e.args['lat'], e.args['lng'])))
        self.on('zoomend', lambda e: self.set_zoom(e.args))

    def set_location(self, location: Tuple[float, float]) -> None:
        self.location = location

    def set_zoom(self, zoom: int) -> None:
        self.zoom = zoom

    def update(self) -> None:
        self._props['map_options'] = {
            'center': {
                'lat': self.location[0],
                'lng': self.location[1],
            },
            'zoom': self.zoom,
        }
        self._props['layers'] = [
            {
                'url_template': layer.url_template,
                'options': layer.options
            }
            for layer in self.layers
        ]
        super().update()
