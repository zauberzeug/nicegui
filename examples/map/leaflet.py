import logging
from typing import Dict, Optional, Tuple, Union

from nicegui import ui
from nicegui.events import ValueChangeEventArguments


class map(ui.card):

    def __init__(self):
        super().__init__()
        self.classes('osm-map').style('width:100%;height:300px;transition:opacity 1s;opacity:0.1')
        self.add_leaflet_js()

    async def set_location(self, location: Union[Optional[Tuple[float, float]], Dict[str, Tuple[float, float]], ValueChangeEventArguments]):
        try:
            if isinstance(location, ValueChangeEventArguments):
                location = location.value
            if isinstance(location, dict):
                location = location.get('location', location.get('value', None))
            if not isinstance(location, tuple) or len(location) != 2 or not all(
                    isinstance(x, float) or isinstance(x, int) for x in location):
                self.style('opacity: 0.1;')
                logging.warning(f'Invalid location: {location}')
                return
            self.style('opacity: 1;')
            await ui.run_javascript(f'''
                target = L.latLng("{location[0]}", "{location[1]}")
                map.setView(target, 9);
                if (marker != undefined) map.removeLayer(marker);
                marker = L.marker(target);
                marker.addTo(map);
                0 // return something so we do net get a js error
            ''')
        except:
            logging.exception(f'could not update {location}')

    @staticmethod
    def add_leaflet_js():
        ui.add_head_html(r'''
        <script src="https://unpkg.com/leaflet@1.6.0/dist/leaflet.js"></script>
        <link href="https://unpkg.com/leaflet@1.6.0/dist/leaflet.css" rel="stylesheet"/>
        <script>
            function waitForElm(selector) {
                return new Promise(resolve => {
                    if (document.querySelector(selector)) {
                        return resolve(document.querySelector(selector));
                    }

                    const observer = new MutationObserver(mutations => {
                        if (document.querySelector(selector)) {
                            resolve(document.querySelector(selector));
                            observer.disconnect();
                        }
                    });

                    observer.observe(document.body, {
                        childList: true,
                        subtree: true
                    });
                });
            }
            var marker;
            var map;
            document.addEventListener("DOMContentLoaded", function() {
                waitForElm('.osm-map').then((container) => {
                    map = L.map(container);
                    L.tileLayer('http://{s}.tile.osm.org/{z}/{x}/{y}.png', {
                        attribution: '&copy; <a href="http://osm.org/copyright">OpenStreetMap</a> contributors'
                    }).addTo(map);                    
                });
            });
        </script>
        ''')
