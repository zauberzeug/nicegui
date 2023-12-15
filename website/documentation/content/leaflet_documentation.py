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
    The default map style is OpenStreetMap.
    You can find more map styles at <https://leaflet-extras.github.io/leaflet-providers/preview/>.
    Each call to `tile_layer` stacks upon the previous ones.
    So if you want to change the map style, you have to remove the default one first.
''')
def map_style() -> None:
    m = ui.leaflet(location=(51.505, -0.090), zoom=3)
    del m.layers[0]
    m.tile_layer(
        url_template=r'https://{s}.tile.opentopomap.org/{z}/{x}/{y}.png',
        options={
            'maxZoom': 17,
            'attribution':
                'Map data: &copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors, <a href="http://viewfinderpanoramas.org">SRTM</a> | '
                'Map style: &copy; <a href="https://opentopomap.org">OpenTopoMap</a> (<a href="https://creativecommons.org/licenses/by-sa/3.0/">CC-BY-SA</a>)'
        },
    )


@doc.demo('Add Markers on Click', '''
    You can add markers to the map with `marker`. 
    The `location` argument is a tuple of latitude and longitude.
    This demo adds markers by clicking on the map.
    Note that the "map-click" event refers to the click event of the map object,
    while the "click" event refers to the click event of the container div.
''')
def markers() -> None:
    from nicegui import events

    m = ui.leaflet(location=(51.505, -0.09))

    def handle_click(e: events.GenericEventArguments):
        lat = e.args['latlng']['lat']
        lng = e.args['latlng']['lng']
        m.marker(location=(lat, lng))
    m.on('map-click', handle_click)


@doc.demo('Vector Layers', '''
    Leaflet supports a set of [vector layers](https://leafletjs.com/reference.html#:~:text=VideoOverlay-,Vector%20Layers,-Path) like circle, polygon etc.
    These can be added with the `generic_layer` method.
    We are happy to review any pull requests to add more specific layers to simplify usage.
''')
def vector_layers() -> None:
    m = ui.leaflet(location=(51.505, -0.09)).classes('h-32')
    m.generic_layer(name='circle',
                    args=[[51.505, -0.09], {'color': 'red', 'radius': 300}])


@doc.demo('Draw on Map', '''
    You can enable a toolbar to draw on the map.
    The `draw_control` can be used to configure the toolbar.
    This demo adds markers and polygons by clicking on the map.
''')
def draw_on_map() -> None:
    from nicegui import events

    def handle_draw(e: events.GenericEventArguments):
        if e.args['layerType'] == 'marker':
            m.marker(location=(e.args['layer']['_latlng']['lat'],
                               e.args['layer']['_latlng']['lng']))
        if e.args['layerType'] == 'polygon':
            m.generic_layer(name='polygon', args=[e.args['layer']['_latlngs']])

    draw_control = {
        'draw': {
            'polygon': True,
            'marker': True,
            'circle': False,
            'rectangle': False,
            'polyline': False,
            'circlemarker': False,
        },
        'edit': False,
    }
    m = ui.leaflet(location=(51.505, -0.09), zoom=13, draw_control=draw_control)
    m.on('draw:created', handle_draw)


doc.reference(ui.leaflet)
