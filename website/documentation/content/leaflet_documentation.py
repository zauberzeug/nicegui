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


@doc.demo('Layers and markers', '''
    The following demo shows how to add custom layers and markers to a map.
''')
def layers_and_markers() -> None:
    m = ui.leaflet(location=(51.505, -0.090))
    m.tile_layer(url_template=r'https://{s}.tile.openstreetmap.fr/hot/{z}/{x}/{y}.png')
    ui.button(icon='add_location', on_click=lambda: m.marker(location=m.location))


doc.reference(ui.leaflet)
