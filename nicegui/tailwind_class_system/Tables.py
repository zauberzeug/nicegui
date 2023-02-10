
from typing import Literal
from nicegui.element import Element

BorderCollapse = Literal["border-collapse","border-separate"]

BorderSpacing = Literal["border-spacing-0","border-spacing-x-0","border-spacing-y-0","border-spacing-px","border-spacing-x-px","border-spacing-y-px","border-spacing-0.5","border-spacing-x-0.5","border-spacing-y-0.5","border-spacing-1","border-spacing-x-1","border-spacing-y-1","border-spacing-1.5","border-spacing-x-1.5","border-spacing-y-1.5","border-spacing-2","border-spacing-x-2","border-spacing-y-2","border-spacing-2.5","border-spacing-x-2.5","border-spacing-y-2.5","border-spacing-3","border-spacing-x-3","border-spacing-y-3","border-spacing-3.5","border-spacing-x-3.5","border-spacing-y-3.5","border-spacing-4","border-spacing-x-4","border-spacing-y-4","border-spacing-5","border-spacing-x-5","border-spacing-y-5","border-spacing-6","border-spacing-x-6","border-spacing-y-6","border-spacing-7","border-spacing-x-7","border-spacing-y-7","border-spacing-8","border-spacing-x-8","border-spacing-y-8","border-spacing-9","border-spacing-x-9","border-spacing-y-9","border-spacing-10","border-spacing-x-10","border-spacing-y-10","border-spacing-11","border-spacing-x-11","border-spacing-y-11","border-spacing-12","border-spacing-x-12","border-spacing-y-12","border-spacing-14","border-spacing-x-14","border-spacing-y-14","border-spacing-16","border-spacing-x-16","border-spacing-y-16","border-spacing-20","border-spacing-x-20","border-spacing-y-20","border-spacing-24","border-spacing-x-24","border-spacing-y-24","border-spacing-28","border-spacing-x-28","border-spacing-y-28","border-spacing-32","border-spacing-x-32","border-spacing-y-32","border-spacing-36","border-spacing-x-36","border-spacing-y-36","border-spacing-40","border-spacing-x-40","border-spacing-y-40","border-spacing-44","border-spacing-x-44","border-spacing-y-44","border-spacing-48","border-spacing-x-48","border-spacing-y-48","border-spacing-52","border-spacing-x-52","border-spacing-y-52","border-spacing-56","border-spacing-x-56","border-spacing-y-56","border-spacing-60","border-spacing-x-60","border-spacing-y-60","border-spacing-64","border-spacing-x-64","border-spacing-y-64","border-spacing-72","border-spacing-x-72","border-spacing-y-72","border-spacing-80","border-spacing-x-80","border-spacing-y-80","border-spacing-96","border-spacing-x-96","border-spacing-y-96"]

TableLayout = Literal["table-auto","table-fixed"]


class Tables:
    def __init__(self, element: Element = Element("")) -> None:
        self.element = element

    def __add(self, _class: str) -> None:
        """
        Internal
        """
        self.element.classes(add=_class)

    def apply(self, ex_element: Element) -> Element:
        """
        Apply the Style to an outer element

        Args:
            ex_element (Element): External Element

        Returns:
            Element: External Element
        """
        return ex_element.classes(add=" ".join(self.element._classes))


    def border_collapse(self, _collapse: BorderCollapse):
        """
        Utilities for controlling whether table borders should collapse or be separated.
        """
        self.__add(_collapse)
        return self
        

    def border_spacing(self, _spacing: BorderSpacing):
        """
        Utilities for controlling the spacing between table borders.
        """
        self.__add(_spacing)
        return self
        

    def table_layout(self, _layout: TableLayout):
        """
        Utilities for controlling the table layout algorithm.
        """
        self.__add(_layout)
        return self
        