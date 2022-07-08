from __future__ import annotations

from typing import List

import justpy as jp

from ..binding import active_links, bindable_properties, bindings
from ..globals import view_stack
from .element import Element


class Group(Element):

    def __enter__(self):
        view_stack.append(self.view)
        return self

    def __exit__(self, *_):
        view_stack.pop()
        if len(view_stack) <= 1:
            self.update()  # NOTE: update when we are back on top of the stack (only the first page is in view stack)

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
