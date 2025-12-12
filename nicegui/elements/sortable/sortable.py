from __future__ import annotations

from typing import Any

from nicegui.element import Element
from nicegui.events import GenericEventArguments, Handler


class Sortable(Element, component='sortable.js', esm={'nicegui-sortable': 'dist'}, default_classes='nicegui-sortable'):

    def __init__(self, options: dict[str, Any] | None = None, *, on_change: Handler[GenericEventArguments] | None = None) -> None:
        super().__init__()

        self._props['options'] = {'animation': 150, **(options or {})}

        if on_change:
            self.on('sort_change', on_change)
