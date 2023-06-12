from nicegui.dependencies import register_component
from nicegui.element import Element

register_component('search', __file__, 'search.vue')


class search(Element):

    def __init__(self) -> None:
        """Search NiceGUI documentation"""
        super().__init__('search')
