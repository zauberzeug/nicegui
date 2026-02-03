import asyncio
from pathlib import Path
from typing import Any, cast

from typing_extensions import Self

from ... import binding
from ...awaitable_response import AwaitableResponse, NullResponse
from ...defaults import DEFAULT_PROP, resolve_defaults
from ...element import Element
from ...events import GenericEventArguments
from .leaflet_layer import Layer


class Leaflet(Element, component='leaflet.js', esm={'nicegui-leaflet': 'dist'}, default_classes='nicegui-leaflet'):
    # pylint: disable=import-outside-toplevel
    from .leaflet_layers import GenericLayer as generic_layer
    from .leaflet_layers import ImageOverlay as image_overlay
    from .leaflet_layers import Marker as marker
    from .leaflet_layers import TileLayer as tile_layer
    from .leaflet_layers import VideoOverlay as video_overlay
    from .leaflet_layers import WmsLayer as wms_layer

    center = binding.BindableProperty(lambda sender, value: cast(Leaflet, sender).set_center(value))
    zoom = binding.BindableProperty(lambda sender, value: cast(Leaflet, sender).set_zoom(value))

    @resolve_defaults
    def __init__(self,
                 center: tuple[float, float] = DEFAULT_PROP | (0.0, 0.0),
                 zoom: int = DEFAULT_PROP | 13,
                 *,
                 options: dict = DEFAULT_PROP | {},
                 draw_control: bool | dict = DEFAULT_PROP | False,
                 hide_drawn_items: bool = DEFAULT_PROP | False,
                 additional_resources: list[str] | None = DEFAULT_PROP | None,
                 ) -> None:
        """Leaflet map

        This element is a wrapper around the `Leaflet <https://leafletjs.com/>`_ JavaScript library.

        :param center: initial center location of the map (latitude/longitude, default: (0.0, 0.0))
        :param zoom: initial zoom level of the map (default: 13)
        :param draw_control: whether to show the draw toolbar (default: False)
        :param options: additional options passed to the Leaflet map (default: {})
        :param hide_drawn_items: whether to hide drawn items on the map (default: False, *added in version 2.0.0*)
        :param additional_resources: additional resources like CSS or JS files to load (default: None, *added in version 2.11.0*)
        """
        super().__init__()
        self.add_resource(Path(__file__).parent / 'dist')

        self.layers: list[Layer] = []
        self.is_initialized = False

        # read-write public API
        self.center = center
        self.zoom = zoom

        # internal state, mutates client state via _to_dict
        self._props['center'] = center
        self._props['zoom'] = zoom

        # client state
        self._client_center = center
        self._client_zoom = zoom

        self._props['options'] = {**options}
        self._props['draw-control'] = draw_control
        self._props['hide-drawn-items'] = hide_drawn_items
        self._props['additional-resources'] = additional_resources or []

        self._props.add_rename('draw_control', 'draw-control')  # DEPRECATED: remove in NiceGUI 4.0
        self._props.add_rename('hide_drawn_items', 'hide-drawn-items')  # DEPRECATED: remove in NiceGUI 4.0
        self._props.add_rename('additional_resources', 'additional-resources')  # DEPRECATED: remove in NiceGUI 4.0

        self.on('init', self._handle_init)
        self.on('map-moveend', self._handle_move_or_zoom_end)
        self.on('map-zoomend', self._handle_move_or_zoom_end)

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

    def _handle_init(self) -> None:
        self.is_initialized = True
        for layer in self.layers:
            self.run_method('add_layer', layer.to_dict(), layer.id)

    async def initialized(self) -> None:
        """Wait until the map is initialized."""
        event = asyncio.Event()
        self.on('init', event.set, [])
        await self.client.connected()
        await event.wait()

    def _handle_move_or_zoom_end(self, e: GenericEventArguments) -> None:
        self._send_update_on_value_change = False
        self.center = self._client_center = e.args['center']
        self.zoom = self._client_zoom = e.args['zoom']
        self._send_update_on_value_change = True

    def run_method(self, name: str, *args: Any, timeout: float = 1) -> AwaitableResponse:
        if not self.is_initialized:
            return NullResponse()
        return super().run_method(name, *args, timeout=timeout)

    def set_center(self, center: tuple[float, float]) -> None:
        """Set the center location of the map."""
        if self._props['center'] == center:
            return
        self._props['center'] = center

    def set_zoom(self, zoom: int) -> None:
        """Set the zoom level of the map."""
        if self._props['zoom'] == zoom:
            return
        self._props['zoom'] = zoom

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

    def _to_dict(self):
        if self._send_update_on_value_change and (
            self._props['center'] != self._client_center or
            self._props['zoom'] != self._client_zoom
        ):
            self.run_map_method('setView', self._props['center'], self._props['zoom'])
        return super()._to_dict()
