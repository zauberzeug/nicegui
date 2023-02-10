
from typing import Literal
from nicegui.element import Element

FlexBasis = Literal["basis-0","basis-1","basis-2","basis-3","basis-4","basis-5","basis-6","basis-7","basis-8","basis-9","basis-10","basis-11","basis-12","basis-14","basis-16","basis-20","basis-24","basis-28","basis-32","basis-36","basis-40","basis-44","basis-48","basis-52","basis-56","basis-60","basis-64","basis-72","basis-80","basis-96","basis-auto","basis-px","basis-0.5","basis-1.5","basis-2.5","basis-3.5","basis-1/2","basis-1/3","basis-2/3","basis-1/4","basis-2/4","basis-3/4","basis-1/5","basis-2/5","basis-3/5","basis-4/5","basis-1/6","basis-2/6","basis-3/6","basis-4/6","basis-5/6","basis-1/12","basis-2/12","basis-3/12","basis-4/12","basis-5/12","basis-6/12","basis-7/12","basis-8/12","basis-9/12","basis-10/12","basis-11/12","basis-full"]

FlexDirection = Literal["flex-row","flex-row-reverse","flex-col","flex-col-reverse"]

FlexWrap = Literal["flex-wrap","flex-wrap-reverse","flex-nowrap"]

Flex = Literal["flex-1","flex-auto","flex-initial","flex-none"]

FlexGrow = Literal["grow","grow-0"]

FlexShrink = Literal["shrink","shrink-0"]

Order = Literal["order-1","order-2","order-3","order-4","order-5","order-6","order-7","order-8","order-9","order-10","order-11","order-12","order-first","order-last","order-none"]

GridTemplateColumns = Literal["grid-cols-1","grid-cols-2","grid-cols-3","grid-cols-4","grid-cols-5","grid-cols-6","grid-cols-7","grid-cols-8","grid-cols-9","grid-cols-10","grid-cols-11","grid-cols-12","grid-cols-none"]

GridColumnStartEnd = Literal["col-auto","col-span-1","col-span-2","col-span-3","col-span-4","col-span-5","col-span-6","col-span-7","col-span-8","col-span-9","col-span-10","col-span-11","col-span-12","col-span-full","col-start-1","col-start-2","col-start-3","col-start-4","col-start-5","col-start-6","col-start-7","col-start-8","col-start-9","col-start-10","col-start-11","col-start-12","col-start-13","col-start-auto","col-end-1","col-end-2","col-end-3","col-end-4","col-end-5","col-end-6","col-end-7","col-end-8","col-end-9","col-end-10","col-end-11","col-end-12","col-end-13","col-end-auto"]

GridTemplateRows = Literal["grid-rows-1","grid-rows-2","grid-rows-3","grid-rows-4","grid-rows-5","grid-rows-6","grid-rows-none"]

GridRowStartEnd = Literal["row-auto","row-span-1","row-span-2","row-span-3","row-span-4","row-span-5","row-span-6","row-span-full","row-start-1","row-start-2","row-start-3","row-start-4","row-start-5","row-start-6","row-start-7","row-start-auto","row-end-1","row-end-2","row-end-3","row-end-4","row-end-5","row-end-6","row-end-7","row-end-auto"]

GridAutoFlow = Literal["grid-flow-row","grid-flow-col","grid-flow-dense","grid-flow-row-dense","grid-flow-col-dense"]

GridAutoColumns = Literal["auto-cols-auto","auto-cols-min","auto-cols-max","auto-cols-fr"]

GridAutoRows = Literal["auto-rows-auto","auto-rows-min","auto-rows-max","auto-rows-fr"]

Gap = Literal["gap-0","gap-x-0","gap-y-0","gap-px","gap-x-px","gap-y-px","gap-0.5","gap-x-0.5","gap-y-0.5","gap-1","gap-x-1","gap-y-1","gap-1.5","gap-x-1.5","gap-y-1.5","gap-2","gap-x-2","gap-y-2","gap-2.5","gap-x-2.5","gap-y-2.5","gap-3","gap-x-3","gap-y-3","gap-3.5","gap-x-3.5","gap-y-3.5","gap-4","gap-x-4","gap-y-4","gap-5","gap-x-5","gap-y-5","gap-6","gap-x-6","gap-y-6","gap-7","gap-x-7","gap-y-7","gap-8","gap-x-8","gap-y-8","gap-9","gap-x-9","gap-y-9","gap-10","gap-x-10","gap-y-10","gap-11","gap-x-11","gap-y-11","gap-12","gap-x-12","gap-y-12","gap-14","gap-x-14","gap-y-14","gap-16","gap-x-16","gap-y-16","gap-20","gap-x-20","gap-y-20","gap-24","gap-x-24","gap-y-24","gap-28","gap-x-28","gap-y-28","gap-32","gap-x-32","gap-y-32","gap-36","gap-x-36","gap-y-36","gap-40","gap-x-40","gap-y-40","gap-44","gap-x-44","gap-y-44","gap-48","gap-x-48","gap-y-48","gap-52","gap-x-52","gap-y-52","gap-56","gap-x-56","gap-y-56","gap-60","gap-x-60","gap-y-60","gap-64","gap-x-64","gap-y-64","gap-72","gap-x-72","gap-y-72","gap-80","gap-x-80","gap-y-80","gap-96","gap-x-96","gap-y-96"]

JustifyContent = Literal["justify-start","justify-end","justify-center","justify-between","justify-around","justify-evenly"]

JustifyItems = Literal["justify-items-start","justify-items-end","justify-items-center","justify-items-stretch"]

JustifySelf = Literal["justify-self-auto","justify-self-start","justify-self-end","justify-self-center","justify-self-stretch"]

AlignContent = Literal["content-center","content-start","content-end","content-between","content-around","content-evenly","content-baseline"]

AlignItems = Literal["items-start","items-end","items-center","items-baseline","items-stretch"]

AlignSelf = Literal["self-auto","self-start","self-end","self-center","self-stretch","self-baseline"]

PlaceContent = Literal["place-content-center","place-content-start","place-content-end","place-content-between","place-content-around","place-content-evenly","place-content-baseline","place-content-stretch"]

PlaceItems = Literal["place-items-start","place-items-end","place-items-center","place-items-baseline","place-items-stretch"]

PlaceSelf = Literal["place-self-auto","place-self-start","place-self-end","place-self-center","place-self-stretch"]


class FlexboxGrid:
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


    def flex_basis(self, _basis: FlexBasis):
        """
        Utilities for controlling the initial size of flex items.
        """
        self.__add(_basis)
        return self
        

    def flex_direction(self, _direction: FlexDirection):
        """
        Utilities for controlling the direction of flex items.
        """
        self.__add(_direction)
        return self
        

    def flex_wrap(self, _wrap: FlexWrap):
        """
        Utilities for controlling how flex items wrap.
        """
        self.__add(_wrap)
        return self
        

    def flex(self, _flex: Flex):
        """
        Utilities for controlling how flex items both grow and shrink.
        """
        self.__add(_flex)
        return self
        

    def flex_grow(self, _grow: FlexGrow):
        """
        Utilities for controlling how flex items grow.
        """
        self.__add(_grow)
        return self
        

    def flex_shrink(self, _shrink: FlexShrink):
        """
        Utilities for controlling how flex items shrink.
        """
        self.__add(_shrink)
        return self
        

    def order(self, _order: Order):
        """
        Utilities for controlling the order of flex and grid items.
        """
        self.__add(_order)
        return self
        

    def grid_template_columns(self, _columns: GridTemplateColumns):
        """
        Utilities for specifying the columns in a grid layout.
        """
        self.__add(_columns)
        return self
        

    def grid_column_startend(self, _end: GridColumnStartEnd):
        """
        Utilities for controlling how elements are sized and placed across grid columns.
        """
        self.__add(_end)
        return self
        

    def grid_template_rows(self, _rows: GridTemplateRows):
        """
        Utilities for specifying the rows in a grid layout.
        """
        self.__add(_rows)
        return self
        

    def grid_row_startend(self, _end: GridRowStartEnd):
        """
        Utilities for controlling how elements are sized and placed across grid rows.
        """
        self.__add(_end)
        return self
        

    def grid_auto_flow(self, _flow: GridAutoFlow):
        """
        Utilities for controlling how elements in a grid are auto-placed.
        """
        self.__add(_flow)
        return self
        

    def grid_auto_columns(self, _columns: GridAutoColumns):
        """
        Utilities for controlling the size of implicitly-created grid columns.
        """
        self.__add(_columns)
        return self
        

    def grid_auto_rows(self, _rows: GridAutoRows):
        """
        Utilities for controlling the size of implicitly-created grid rows.
        """
        self.__add(_rows)
        return self
        

    def gap(self, _gap: Gap):
        """
        Utilities for controlling gutters between grid and flexbox items.
        """
        self.__add(_gap)
        return self
        

    def justify_content(self, _content: JustifyContent):
        """
        Utilities for controlling how flex and grid items are positioned along a container's main axis.
        """
        self.__add(_content)
        return self
        

    def justify_items(self, _items: JustifyItems):
        """
        Utilities for controlling how grid items are aligned along their inline axis.
        """
        self.__add(_items)
        return self
        

    def justify_self(self, _self: JustifySelf):
        """
        Utilities for controlling how an individual grid item is aligned along its inline axis.
        """
        self.__add(_self)
        return self
        

    def align_content(self, _content: AlignContent):
        """
        Utilities for controlling how rows are positioned in multi-row flex and grid containers.
        """
        self.__add(_content)
        return self
        

    def align_items(self, _items: AlignItems):
        """
        Utilities for controlling how flex and grid items are positioned along a container's cross axis.
        """
        self.__add(_items)
        return self
        

    def align_self(self, _self: AlignSelf):
        """
        Utilities for controlling how an individual flex or grid item is positioned along its container's cross axis.
        """
        self.__add(_self)
        return self
        

    def place_content(self, _content: PlaceContent):
        """
        Utilities for controlling how content is justified and aligned at the same time.
        """
        self.__add(_content)
        return self
        

    def place_items(self, _items: PlaceItems):
        """
        Utilities for controlling how items are justified and aligned at the same time.
        """
        self.__add(_items)
        return self
        

    def place_self(self, _self: PlaceSelf):
        """
        Utilities for controlling how an individual item is justified and aligned at the same time.
        """
        self.__add(_self)
        return self
        