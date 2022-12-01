import logging
from typing import Tuple

from nicegui import ui


class map(ui.card):

    def __init__(self) -> None:
        super().__init__()
        self.classes('osm-map').style('width:100%;height:300px')
        self.add_leaflet_js()

    async def set_location(self, location: Tuple[float, float]) -> None:
        print(location, flush=True)
        try:
            await ui.run_javascript(f'''
                window.target = L.latLng("{location[0]}", "{location[1]}");
                window.map.setView(target, 9);
                if (window.marker != undefined) window.map.removeLayer(window.marker);
                window.marker = L.marker(target);
                window.marker.addTo(window.map);
            ''', respond=False)
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
                        subtree: true,
                    });
                });
            }
            document.addEventListener("DOMContentLoaded", function() {
                waitForElm('.osm-map').then((container) => {
                    window.map = L.map(container);
                    L.tileLayer('http://{s}.tile.osm.org/{z}/{x}/{y}.png', {
                        attribution: '&copy; <a href="http://osm.org/copyright">OpenStreetMap</a> contributors'
                    }).addTo(window.map);
                });
            });
        </script>
        ''')
