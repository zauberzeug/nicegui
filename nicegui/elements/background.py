from abc import ABCMeta
from typing import Any, Dict, Optional, Tuple

from typing_extensions import Self

from ..dependencies import register_component
from ..element import Element

register_component('background', __file__, 'background.js')


class AbstractSingleton(ABCMeta):

    def __init__(cls, name: str, bases: Tuple, dict: Dict[str, Any]) -> None:
        super().__init__(name, bases, dict)
        cls.instance = None

    def __call__(cls, *args: Any, **kwargs: Any) -> Any:
        if cls.instance is None:
            cls.instance = super().__call__(*args, **kwargs)
        return cls.instance


class Background(Element, metaclass=AbstractSingleton):

    def __init__(self) -> None:
        super().__init__('background')
        self._props['classes'] = []
        self._props['style'] = {}
        self._props['props'] = {}

    def classes(self, add: Optional[str] = None, *, remove: Optional[str] = None, replace: Optional[str] = None) \
            -> Self:
        classes = self._update_classes_list(self._props['classes'], add, remove, replace)
        new_classes = [c for c in classes if c not in self._props['classes']]
        old_classes = [c for c in self._props['classes'] if c not in classes]
        if new_classes:
            self.run_method('add_classes', new_classes)
        if old_classes:
            self.run_method('remove_classes', old_classes)
        self._props['classes'] = classes
        return self

    def style(self, add: Optional[str] = None, *, remove: Optional[str] = None, replace: Optional[str] = None) \
            -> Self:
        old_style = Element._parse_style(remove)
        for key in old_style:
            self._props['style'].pop(key, None)
        if old_style:
            self.run_method('remove_style', list(old_style))
        self._props['style'].update(Element._parse_style(add))
        self._props['style'].update(Element._parse_style(replace))
        if self._props['style']:
            self.run_method('add_style', self._props['style'])
        return self

    def props(self, add: Optional[str] = None, *, remove: Optional[str] = None) -> Self:
        old_props = self._parse_props(remove)
        for key in old_props:
            self._props['props'].pop(key, None)
        if old_props:
            self.run_method('remove_props', list(old_props))
        new_props = self._parse_props(add)
        self._props['props'].update(new_props)
        if self._props['props']:
            self.run_method('add_props', self._props['props'])
        return self
