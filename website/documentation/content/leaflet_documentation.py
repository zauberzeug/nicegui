from nicegui import ui

from . import doc


@doc.demo(ui.leaflet)
def main_demo() -> None:
    m = ui.leaflet(center=(51.505, -0.09))
    ui.label().bind_text_from(m, 'center', lambda center: f'Center: {center[0]:.3f}, {center[1]:.3f}')
    ui.label().bind_text_from(m, 'zoom', lambda zoom: f'Zoom: {zoom}')

    with ui.grid(columns=2):
        ui.button('London', on_click=lambda: m.set_center((51.505, -0.090)))
        ui.button('Berlin', on_click=lambda: m.set_center((52.520, 13.405)))
        ui.button(icon='zoom_in', on_click=lambda: m.set_zoom(m.zoom + 1))
        ui.button(icon='zoom_out', on_click=lambda: m.set_zoom(m.zoom - 1))


@doc.demo('Changing the Map Style', '''
    The default map style is OpenStreetMap.
    You can find more map styles at <https://leaflet-extras.github.io/leaflet-providers/preview/>.
    Each call to `tile_layer` stacks upon the previous ones.
    So if you want to change the map style, you have to remove the default one first.
''')
def map_style() -> None:
    m = ui.leaflet(center=(51.505, -0.090), zoom=3)
    m.clear_layers()
    m.tile_layer(
        url_template=r'https://{s}.tile.opentopomap.org/{z}/{x}/{y}.png',
        options={
            'maxZoom': 17,
            'attribution':
                'Map data: &copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors, <a href="https://viewfinderpanoramas.org/">SRTM</a> | '
                'Map style: &copy; <a href="https://opentopomap.org">OpenTopoMap</a> (<a href="https://creativecommons.org/licenses/by-sa/3.0/">CC-BY-SA</a>)'
        },
    )


@doc.demo('Add Markers on Click', '''
    You can add markers to the map with `marker`.
    The `center` argument is a tuple of latitude and longitude.
    This demo adds markers by clicking on the map.
    Note that the "map-click" event refers to the click event of the map object,
    while the "click" event refers to the click event of the container div.
''')
def markers() -> None:
    from nicegui import events

    m = ui.leaflet(center=(51.505, -0.09))

    def handle_click(e: events.GenericEventArguments):
        lat = e.args['latlng']['lat']
        lng = e.args['latlng']['lng']
        m.marker(latlng=(lat, lng))
    m.on('map-click', handle_click)


@doc.demo('Move Markers', '''
    You can move markers with the `move` method.
''')
def move_markers() -> None:
    m = ui.leaflet(center=(51.505, -0.09))
    marker = m.marker(latlng=m.center)
    ui.button('Move marker', on_click=lambda: marker.move(51.51, -0.09))


@doc.demo('Vector Layers', '''
    Leaflet supports a set of [vector layers](https://leafletjs.com/reference.html#:~:text=VideoOverlay-,Vector%20Layers,-Path) like circle, polygon etc.
    These can be added with the `generic_layer` method.
    We are happy to review any pull requests to add more specific layers to simplify usage.
''')
def vector_layers() -> None:
    m = ui.leaflet(center=(51.505, -0.09)).classes('h-32')
    m.generic_layer(name='circle', args=[m.center, {'color': 'red', 'radius': 300}])


@doc.demo('Disable Pan and Zoom', '''
    There are [several options to configure the map in Leaflet](https://leafletjs.com/reference.html#map).
    This demo disables the pan and zoom controls.
''')
def disable_pan_zoom() -> None:
    options = {
        'zoomControl': False,
        'scrollWheelZoom': False,
        'doubleClickZoom': False,
        'boxZoom': False,
        'keyboard': False,
        'dragging': False,
    }
    ui.leaflet(center=(51.505, -0.09), options=options)


@doc.demo('Draw on Map', '''
    You can enable a toolbar to draw on the map.
    The `draw_control` can be used to configure the toolbar.
    This demo adds markers and polygons by clicking on the map.
    By setting "edit" and "remove" to `True` (the default), you can enable editing and deleting drawn shapes.
''')
def draw_on_map() -> None:
    from nicegui import events

    def handle_draw(e: events.GenericEventArguments):
        layer_type = e.args['layerType']
        coords = e.args['layer'].get('_latlng') or e.args['layer'].get('_latlngs')
        ui.notify(f'Drawn a {layer_type} at {coords}')

    draw_control = {
        'draw': {
            'polygon': True,
            'marker': True,
            'circle': True,
            'rectangle': True,
            'polyline': True,
            'circlemarker': True,
        },
        'edit': {
            'edit': True,
            'remove': True,
        },
    }
    m = ui.leaflet(center=(51.505, -0.09), draw_control=draw_control)
    m.classes('h-96')
    m.on('draw:created', handle_draw)
    m.on('draw:edited', lambda: ui.notify('Edit completed'))
    m.on('draw:deleted', lambda: ui.notify('Delete completed'))


@doc.demo('Draw with Custom Options', '''
    You can draw shapes with custom options like stroke color and weight.
    To hide the default rendering of drawn items, set `hide_drawn_items` to `True`.
''')
def draw_custom_options():
    from nicegui import events

    def handle_draw(e: events.GenericEventArguments):
        options = {'color': 'red', 'weight': 1}
        m.generic_layer(name='polygon', args=[e.args['layer']['_latlngs'], options])

    draw_control = {
        'draw': {
            'polygon': True,
            'marker': False,
            'circle': False,
            'rectangle': False,
            'polyline': False,
            'circlemarker': False,
        },
        'edit': {
            'edit': False,
            'remove': False,
        },
    }
    m = ui.leaflet(center=(51.5, 0), draw_control=draw_control, hide_drawn_items=True)
    m.on('draw:created', handle_draw)


@doc.demo('Run Map Methods', '''
    You can run methods of the Leaflet map object with `run_map_method`.
    This demo shows how to fit the map to the whole world.
''')
def run_map_methods() -> None:
    m = ui.leaflet(center=(51.505, -0.09)).classes('h-32')
    ui.button('Fit world', on_click=lambda: m.run_map_method('fitWorld'))


@doc.demo('Run Layer Methods', '''
    You can run methods of the Leaflet layer objects with `run_layer_method`.
    This demo shows how to change the opacity of a marker or change its icon.
''')
def run_layer_methods() -> None:
    m = ui.leaflet(center=(51.505, -0.09)).classes('h-32')
    marker = m.marker(latlng=m.center)
    ui.button('Hide', on_click=lambda: marker.run_method('setOpacity', 0.3))
    ui.button('Show', on_click=lambda: marker.run_method('setOpacity', 1.0))

    icon = 'L.icon({iconUrl: "https://leafletjs.com/examples/custom-icons/leaf-green.png"})'
    ui.button('Change icon', on_click=lambda: marker.run_method(':setIcon', icon))


@doc.demo('Wait for Initialization', '''
    You can wait for the map to be initialized with the `initialized` method.
    This is necessary when you want to run methods like fitting the bounds of the map right after the map is created.
''')
async def wait_for_init() -> None:
    # @ui.page('/')
    async def page():
        m = ui.leaflet(zoom=5)
        central_park = m.generic_layer(name='polygon', args=[[
            (40.767809, -73.981249),
            (40.800273, -73.958291),
            (40.797011, -73.949683),
            (40.764704, -73.973741),
        ]])
        await m.initialized()
        bounds = await central_park.run_method('getBounds')
        m.run_map_method('fitBounds', [[bounds['_southWest'], bounds['_northEast']]])
    ui.timer(0, page, once=True)  # HIDE

doc.reference(ui.leaflet)
