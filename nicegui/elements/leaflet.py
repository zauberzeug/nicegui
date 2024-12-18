import asyncio
from pathlib import Path
from typing import Any, Dict, List, Tuple, Union, cast

from typing_extensions import Self

from .. import binding
from ..awaitable_response import AwaitableResponse, NullResponse
from ..element import Element
from ..events import GenericEventArguments
from .leaflet_layer import Layer


class Leaflet(Element, component='leaflet.js', default_classes='nicegui-leaflet'):
    # pylint: disable=import-outside-toplevel
    from .leaflet_layers import GenericLayer as generic_layer
    from .leaflet_layers import Marker as marker
    from .leaflet_layers import TileLayer as tile_layer

    center = binding.BindableProperty(lambda sender, value: cast(Leaflet, sender).set_center(value))
    zoom = binding.BindableProperty(lambda sender, value: cast(Leaflet, sender).set_zoom(value))

    def __init__(self,
                 center: Tuple[float, float] = (0.0, 0.0),
                 zoom: int = 13,
                 *,
                 options: Dict = {},  # noqa: B006
                 draw_control: Union[bool, Dict] = False,
                 hide_drawn_items: bool = False,
                 ) -> None:
        """Leaflet map

        This element is a wrapper around the `Leaflet <https://leafletjs.com/>`_ JavaScript library.

        :param center: initial center location of the map (latitude/longitude, default: (0.0, 0.0))
        :param zoom: initial zoom level of the map (default: 13)
        :param draw_control: whether to show the draw toolbar (default: False)
        :param options: additional options passed to the Leaflet map (default: {})
        :param hide_drawn_items: whether to hide drawn items on the map (default: False)
        """
        super().__init__()
        self.add_resource(Path(__file__).parent / 'lib' / 'leaflet')

        self.layers: List[Layer] = []
        self.is_initialized = False

        self.center = center
        self.zoom = zoom
        self._props['center'] = center
        self._props['zoom'] = zoom
        self._props['options'] = {**options}
        self._props['draw_control'] = draw_control
        self._props['hide_drawn_items'] = hide_drawn_items

        self.on('init', self._handle_init)
        self.on('map-moveend', self._handle_moveend)
        self.on('map-zoomend', self._handle_zoomend)

        self.tile_layer(
            url_template=r'https://{s}.tile.osm.org/{z}/{x}/{y}.png',
            options={'attribution': '&copy; <a href="https://openstreetmap.org">OpenStreetMap</a> contributors'},
        )

        self._send_update_on_value_change = True

    def __enter__(self) -> Self:
        Layer.current_leaflet = self
        return super().__enter__()

    def __getattribute__(self, name: str) -> Any:
        attribute = super().__getattribute__(name)
        if isinstance(attribute, type) and issubclass(attribute, Layer):
            Layer.current_leaflet = self
        return attribute

    def _handle_init(self, e: GenericEventArguments) -> None:
        self.is_initialized = True
        with self.client.individual_target(e.args['socket_id']):
            for layer in self.layers:
                self.run_method('add_layer', layer.to_dict(), layer.id)

    async def initialized(self, timeout: float = 3.0) -> None:
        """Wait until the map is initialized.

        :param timeout: timeout in seconds (default: 3 seconds)
        """
        event = asyncio.Event()
        self.on('init', event.set, [])
        await self.client.connected(timeout=timeout)
        await event.wait()

    def _handle_moveend(self, e: GenericEventArguments) -> None:
        self._send_update_on_value_change = False
        self.center = e.args['center']
        self._send_update_on_value_change = True

    def _handle_zoomend(self, e: GenericEventArguments) -> None:
        self._send_update_on_value_change = False
        self.zoom = e.args['zoom']
        self._send_update_on_value_change = True

    def run_method(self, name: str, *args: Any, timeout: float = 1) -> AwaitableResponse:
        if not self.is_initialized:
            return NullResponse()
        return super().run_method(name, *args, timeout=timeout)

    def set_center(self, center: Tuple[float, float]) -> None:
        """Set the center location of the map."""
        if self._props['center'] == center:
            return
        self._props['center'] = center
        if self._send_update_on_value_change:
            self.update()

    def set_zoom(self, zoom: int) -> None:
        """Set the zoom level of the map."""
        if self._props['zoom'] == zoom:
            return
        self._props['zoom'] = zoom
        if self._send_update_on_value_change:
            self.update()

    def remove_layer(self, layer: Layer) -> None:
        """Remove a layer from the map."""
        self.layers.remove(layer)
        self.run_method('remove_layer', layer.id)

    def clear_layers(self) -> None:
        """Remove all layers from the map."""
        self.layers.clear()
        self.run_method('clear_layers')

    def run_map_method(self, name: str, *args, timeout: float = 1) -> AwaitableResponse:
        """Run a method of the Leaflet map instance.

        Refer to the `Leaflet documentation <https://leafletjs.com/reference.html#map-methods-for-modifying-map-state>`_ for a list of methods.

        If the function is awaited, the result of the method call is returned.
        Otherwise, the method is executed without waiting for a response.

        :param name: name of the method (a prefix ":" indicates that the arguments are JavaScript expressions)
        :param args: arguments to pass to the method
        :param timeout: timeout in seconds (default: 1 second)

        :return: AwaitableResponse that can be awaited to get the result of the method call
        """
        return self.run_method('run_map_method', name, *args, timeout=timeout)

    def run_layer_method(self, layer_id: str, name: str, *args, timeout: float = 1) -> AwaitableResponse:
        """Run a method of a Leaflet layer.

        If the function is awaited, the result of the method call is returned.
        Otherwise, the method is executed without waiting for a response.

        :param layer_id: ID of the layer
        :param name: name of the method (a prefix ":" indicates that the arguments are JavaScript expressions)
        :param args: arguments to pass to the method
        :param timeout: timeout in seconds (default: 1 second)

        :return: AwaitableResponse that can be awaited to get the result of the method call
        """
        return self.run_method('run_layer_method', layer_id, name, *args, timeout=timeout)

    def _handle_delete(self) -> None:
        binding.remove(self.layers)
        super()._handle_delete()
