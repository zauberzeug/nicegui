from typing import Tuple, cast

from ..binding import BindableProperty
from ..element import Element


class Leaflet(Element, component='leaflet.js'):
    location = BindableProperty(lambda sender, value: cast(Leaflet, sender).on_location_change(value))
    zoom = BindableProperty(lambda sender, value: cast(Leaflet, sender).on_zoom_change(value))

    def __init__(self, location: Tuple[float, float] = (0, 0), zoom: int = 13) -> None:
        super().__init__()
        self._props['map_options'] = {
            'center': {
                'lat': location[0],
                'lng': location[1],
            },
            'zoom': zoom,
        }
        self._props['layers'] = [{
            'url_template': 'http://{s}.tile.osm.org/{z}/{x}/{y}.png',
            'options': {
                'attribution': '&copy; <a href="https://openstreetmap.org/copyright">OpenStreetMap contributors</a>',
            },
        }]
        self.set_location(location)
        self.set_zoom(zoom)
        self.on('moveend', lambda e: self.set_location((e.args['lat'], e.args['lng'])))
        self.on('zoomend', lambda e: self.set_zoom(e.args))

    def set_location(self, location: Tuple[float, float]) -> None:
        self.location = location

    def set_zoom(self, zoom: int) -> None:
        self.zoom = zoom

    def on_location_change(self, location: Tuple[float, float]) -> None:
        self._props['map_options']['center']['lat'] = location[0]
        self._props['map_options']['center']['lng'] = location[1]
        self.update()

    def on_zoom_change(self, zoom: int) -> None:
        self._props['map_options']['zoom'] = zoom
        self.update()
