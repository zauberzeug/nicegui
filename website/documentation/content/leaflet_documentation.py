from nicegui import ui

from . import doc


@doc.demo(ui.leaflet)
def main_demo() -> None:
    m = ui.leaflet(location=(51.505, -0.09))
    ui.label().bind_text_from(m, 'location', lambda location: f'Location: {location[0]:.3f}, {location[1]:.3f}')
    ui.label().bind_text_from(m, 'zoom', lambda zoom: f'Zoom: {zoom}')

    with ui.grid(columns=2):
        ui.button('London', on_click=lambda: m.set_location((51.505, -0.090)))
        ui.button('Berlin', on_click=lambda: m.set_location((52.520, 13.405)))
        ui.button(icon='zoom_in', on_click=lambda: m.set_zoom(m.zoom + 1))
        ui.button(icon='zoom_out', on_click=lambda: m.set_zoom(m.zoom - 1))


@doc.demo('Changing the Map Style', '''
    The default map style is OpenStreetMap. You can find more map styles at <https://leaflet-extras.github.io/leaflet-providers/preview/>.
    Each call to `tile_layer` stacks upon the previous ones. So if you want to change the map style, you have to remove the default one first.
''')
def map_style() -> None:
    m = ui.leaflet(location=(51.505, -0.090), zoom=3)
    del m.layers[0]
    m.tile_layer(url_template=r'https://{s}.tile.opentopomap.org/{z}/{x}/{y}.png',
                 options={
                     'maxZoom': 17,
                     'attribution': 'Map data: &copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors, <a href="http://viewfinderpanoramas.org">SRTM</a> | Map style: &copy; <a href="https://opentopomap.org">OpenTopoMap</a> (<a href="https://creativecommons.org/licenses/by-sa/3.0/">CC-BY-SA</a>)'
                 })


@doc.demo('Add markers', '''
    
''')
def markers() -> None:
    m = ui.leaflet(location=(51.505, -0.09)).classes('h-32')
    ui.button(icon='pin_drop', on_click=lambda: m.marker(location=m.location))


doc.reference(ui.leaflet)
