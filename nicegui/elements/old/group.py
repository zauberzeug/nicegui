from __future__ import annotations

from typing import List, Union

import justpy as jp

from ..auto_context import get_view_stack
from ..binding import active_links, bindable_properties, bindings
from .element import Element


class Group(Element):

    def __enter__(self):
        self._child_count_on_enter = len(self.view)
        get_view_stack().append(self.view)
        return self

    def __exit__(self, *_):
        get_view_stack().pop()
        if self._child_count_on_enter != len(self.view):
            self.update()

    def tight(self) -> Group:
        return self.classes(replace='').style(replace='')

    def clear(self):
        def collect_components(view: jp.HTMLBaseComponent) -> List[jp.HTMLBaseComponent]:
            return getattr(view, 'components', []) + \
                [view for child in getattr(view, 'components', []) for view in collect_components(child)]
        components = collect_components(self.view)

        active_links[:] = [
            (source_obj, source_name, target_obj, target_name, transform)
            for source_obj, source_name, target_obj, target_name, transform in active_links
            if not (
                isinstance(source_obj, jp.HTMLBaseComponent) and source_obj in components or
                isinstance(target_obj, jp.HTMLBaseComponent) and target_obj in components or
                isinstance(source_obj, Element) and source_obj.view in components or
                isinstance(target_obj, Element) and target_obj.view in components
            )
        ]

        for key, binding_list in list(bindings.items()):
            binding_list[:] = [
                (source_obj, target_obj, target_name, transform)
                for source_obj, target_obj, target_name, transform in binding_list
                if not (
                    isinstance(source_obj, jp.HTMLBaseComponent) and source_obj in components or
                    isinstance(target_obj, jp.HTMLBaseComponent) and target_obj in components or
                    isinstance(source_obj, Element) and source_obj.view in components or
                    isinstance(target_obj, Element) and target_obj.view in components
                )
            ]
            if not binding_list:
                del bindings[key]

        for (obj_id, name), obj in list(bindable_properties.items()):
            if isinstance(obj, jp.HTMLBaseComponent) and obj in components or \
               isinstance(obj, Element) and obj.view in components:
                del bindable_properties[(obj_id, name)]

        self.view.delete_components()
        self.update()

    def remove(self, element: Union[Element, int]) -> None:
        view = element.view if isinstance(element, Element) else self.view.get_components()[element]
        self.view.remove_component(view)
        self.update()
