from __future__ import annotations
import justpy as jp
from ..globals import view_stack
from ..binding import active_links
from .element import Element

class Group(Element):

    def __enter__(self):
        view_stack.append(self.view)
        return self

    def __exit__(self, *_):
        view_stack.pop()

    def tight(self) -> Group:
        return self.classes(replace='').style(replace='')

    def clear(self):
        def collect_components(view: jp.HTMLBaseComponent) -> list[jp.HTMLBaseComponent]:
            return view.components + [view for child in view.components for view in collect_components(child)]
        components = collect_components(self.view)
        obsolete_links = [link for link in active_links if link[0] in components or link[2] in components]
        active_links[:] = [l for l in active_links if l not in obsolete_links]
        self.view.delete_components()
