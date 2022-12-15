from typing import Tuple

from nicegui import ui
from nicegui.element import Element
from nicegui.vue import register_component

register_component('leaflet', __file__, 'leaflet.js')


class leaflet(Element):

    def __init__(self) -> None:
        super().__init__('leaflet')
        ui.add_head_html('<link href="https://unpkg.com/leaflet@1.6.0/dist/leaflet.css" rel="stylesheet"/>')
        ui.add_head_html('<script src="https://unpkg.com/leaflet@1.6.0/dist/leaflet.js"></script>')

    def set_location(self, location: Tuple[float, float]) -> None:
        self.run_method('set_location', location[0], location[1])
