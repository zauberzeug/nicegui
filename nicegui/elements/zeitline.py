from pathlib import Path
from typing import Any, Callable, Optional, Union
from ..element import Element
from .mixins.value_element import ValueElement
from nicegui.elements.mixins.disableable_element import DisableableElement


class Zeitline(DisableableElement, component='zeitline.js'):
    # VALUE_PROP: str = 'value'
    LOOPBACK = False

    def __init__(self,
                 *,
                 events: list[Union[str, tuple[str, str]]] = [],
                 placeholder: Optional[str] = None,
                 ) -> None:
        """Zeitline

        An interactive polylinear timeline.

        """
        super().__init__()
        self.add_resource(Path(__file__).parent / 'lib' / 'zeitline')
        self._classes.append('js-zeitline')
        self._props['conf'] = {}
        for event in events:
            args = [event] if isinstance(event, str) else [*event]
            self.add_event(*args)


    def add_event(self, date: str, label: str = ''):
        self._props['conf'].setdefault('data', []).append({'date': date, 'label': label})
        print(self._props)
        self.update()

    def set_range(self, start: str, end: str):
        self._props['conf']['dateRange'] = [{'date': start}, {'date': end}]
        self.update()

    def add_interval(self, start: str, end: str, weight: int = 100):
        self._props['conf'].setdefault('intervals', []).append([{'date': start}, {'date': end}, weight])
        self.update()
