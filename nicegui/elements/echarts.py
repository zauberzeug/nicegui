from typing import Dict, List

from ..element import Element


class ECharts(
    Element, component="echarts.js", libraries=["lib/echarts/*.js"], extra_libraries=["lib/echarts/extensions/*.js"]
):
    def __init__(self, options: Dict, *, extras: List[str] = []) -> None:
        """ECharts

        An element to create a chart using `ECharts <https://echarts.apache.org/>`_.
        Updates can be pushed to the chart by changing the `options` property.
        After data has changed, call the `update` method to refresh the chart.

        :param options: dictionary of EChart options
        :param extras: list of extra extensions to include
        """
        super().__init__()
        self._props["options"] = options
        self._props["extras"] = extras
        self.libraries.extend(library for library in self.extra_libraries if library.path.stem in extras)

    @property
    def options(self) -> Dict:
        return self._props["options"]

    def update(self) -> None:
        super().update()
        self.run_method("update_chart")
