# Import necessary methods
from nicegui import ui

# Index page that shows the map


@ui.page('/')
async def ui_index():
    m: ui.leaflet = ui.leaflet(center=(51.505, -0.09),
                               additional_resources=[
                                   'https://unpkg.com/leaflet-rotatedmarker@0.2.0/leaflet.rotatedMarker.js',
    ])

    await m.initialized()

    # Create a rotated marker
    map_fstr: str = f'var map = getElement({m.id}).map;'
    ui.run_javascript(map_fstr + """
    L.marker([51.51, -0.09], {rotationAngle: 45}).addTo(map);
    """)

ui.run()
