from pathlib import Path
from typing import Any, Dict, List, Tuple, cast

from typing_extensions import Self

from nicegui.observables import ObservableDict

from .. import binding
from ..awaitable_response import AwaitableResponse, NullResponse
from ..element import Element
from ..events import GenericEventArguments
from .leaflet_layer import Layer


class Leaflet(Element, component='leaflet.js'):
    # pylint: disable=import-outside-toplevel
    from .leaflet_layers import GenericLayer as generic_layer
    from .leaflet_layers import Marker as marker
    from .leaflet_layers import TileLayer as tile_layer

    def __init__(self,
                 location: Tuple[float, float] = (0, 0),
                 zoom: int = 13,
                 draw_control: bool = False,
                 ) -> None:
        """Leaflet map

        This element is a wrapper around the `Leaflet <https://leafletjs.com/>`_ JavaScript library.

        :param location: initial location of the map
        :param zoom: initial zoom level of the map
        :param draw_control: whether to show the draw control toolbar
        """
        super().__init__()
        self.add_resource(Path(__file__).parent / 'lib' / 'leaflet')
        self._classes.append('nicegui-leaflet')

        self.layers: List[Layer] = []
        self._props['map_options'] = ObservableDict()
        self.set_location(location)
        self.set_zoom(zoom)
        self.draw_control = draw_control

        self.is_initialized = False
        self.on('init', self._handle_init)
        self.on('moveend', lambda e: self.set_location((e.args['lat'], e.args['lng'])))
        self.on('zoomend', lambda e: self.set_zoom(e.args))

        self.tile_layer(
            url_template=r'https://{s}.tile.osm.org/{z}/{x}/{y}.png',
            options={'attribution': '&copy; <a href="https://openstreetmap.org">OpenStreetMap</a> contributors'},
        )

    def __enter__(self) -> Self:
        Layer.current_leaflet = self
        return super().__enter__()

    def __getattribute__(self, name: str) -> Any:
        attribute = super().__getattribute__(name)
        if isinstance(attribute, type) and issubclass(attribute, Layer):
            Layer.current_leaflet = self
        return attribute

    @property
    def options(self) -> ObservableDict[str, Any]:
        """Options configuring the Leaflet map."""
        return self._props['map_options']

    @options.setter
    def options(self, value: ObservableDict[str, Any]) -> None:
        assert isinstance(value, ObservableDict)
        self._props['map_options'] = value

    def _handle_init(self, e: GenericEventArguments) -> None:
        self.is_initialized = True
        with self.client.individual_target(e.args['socket_id']):
            for layer in self.layers:
                self.run_method('add_layer', layer.to_dict())

    def run_method(self, name: str, *args: Any, timeout: float = 1, check_interval: float = 0.01) -> AwaitableResponse:
        if not self.is_initialized:
            return NullResponse()
        return super().run_method(name, *args, timeout=timeout, check_interval=check_interval)

    def set_location(self, location: Tuple[float, float]) -> None:
        """Set the location of the map."""
        self.options['center'] = {
            'lat': location[0],
            'lng': location[1],
        }
        self.update()

    def set_zoom(self, zoom: int) -> None:
        """Set the zoom level of the map."""
        self.options['zoom'] = zoom
        self.update()

    @property
    def location(self) -> Tuple[float, float]:
        """The current location of the map."""
        return cast(Tuple[float, float], (self.options['center']['lat'], self.options['center']['lng']))

    @property
    def zoom(self) -> int:
        """The current zoom level of the map."""
        return self.options['zoom']

    def _handle_delete(self) -> None:
        binding.remove(self.layers, Layer)
        super().delete()
