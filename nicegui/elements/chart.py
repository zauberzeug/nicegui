from typing import Callable, Dict, List, Optional

from .. import optional_features

try:
    from nicegui_highcharts import highcharts
    optional_features.register('highcharts')
except ImportError:
    pass


class Chart(highcharts):

    def __init__(self, options: Dict, *,
                 type: str = 'chart', extras: List[str] = [],  # pylint: disable=redefined-builtin
                 on_point_click: Optional[Callable] = None,
                 on_point_drag_start: Optional[Callable] = None,
                 on_point_drag: Optional[Callable] = None,
                 on_point_drop: Optional[Callable] = None,
                 ) -> None:
        super().__init__(options, type=type, extras=extras,
                         on_point_click=on_point_click,
                         on_point_drag_start=on_point_drag_start,
                         on_point_drag=on_point_drag,
                         on_point_drop=on_point_drop)
        if not optional_features.has('highcharts'):
            raise ImportError('Highcharts is not installed. Please run "pip install nicegui_highcharts".')
