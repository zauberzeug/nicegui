from typing import Any, List, Tuple, cast

from .. import binding, globals  # pylint: disable=redefined-builtin
from ..element import Element
from ..events import GenericEventArguments
from .leaflet_layer import Layer


class Leaflet(Element, component='leaflet.js'):
    # pylint: disable=import-outside-toplevel
    from .leaflet_layers import Marker as marker
    from .leaflet_layers import TileLayer as tile_layer

    location = binding.BindableProperty(lambda sender, _: cast(Leaflet, sender).update())
    zoom = binding.BindableProperty(lambda sender, _: cast(Leaflet, sender).update())

    def __init__(self,
                 location: Tuple[float, float] = (0, 0),
                 zoom: int = 13,
                 draw_control: bool = False,
                 ) -> None:
        super().__init__()
        self.layers: List[Layer] = []

        self.set_location(location)
        self.set_zoom(zoom)
        self.draw_control = draw_control

        self.is_initialized = False
        self.on('init', self.handle_init)
        self.on('moveend', lambda e: self.set_location((e.args['lat'], e.args['lng'])))
        self.on('zoomend', lambda e: self.set_zoom(e.args))

        self.tile_layer(
            url_template='http://{s}.tile.osm.org/{z}/{x}/{y}.png',
            options={'attribution': '&copy; <a href="https://openstreetmap.org">OpenStreetMap</a> contributors'},
        )

    def __enter__(self) -> 'Leaflet':
        Layer.current_leaflet = self
        return super().__enter__()

    def __getattribute__(self, name: str) -> Any:
        attribute = super().__getattribute__(name)
        if isinstance(attribute, type) and issubclass(attribute, Layer):
            Layer.current_leaflet = self
        return attribute

    def handle_init(self, e: GenericEventArguments) -> None:
        self.is_initialized = True
        with globals.socket_id(e.args['socket_id']):
            for layer in self.layers:
                self.run_method('add_layer', layer.to_dict())

    def run_method(self, name: str, *args: Any) -> None:
        if not self.is_initialized:
            return
        super().run_method(name, *args)

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
            'drawControl': self.draw_control,
        }
        super().update()

    def delete(self) -> None:
        binding.remove(self.layers, Layer)
        super().delete()
