__all__ = [
    "bottom",
    "center",
    "left",
    "middle",
    "parent",
    "previous",
    "right",
    "top",
]

import numbers
from functools import partial
from string import Template
from typing import Self

from nicegui import Tailwind
from nicegui.element import Element


PseudoElement = str
Elementish = Element|PseudoElement


CALC_LEFT_FOR_CENTER = "(var(--internal-width-$parent_id) / 2 - var(--external-width-$self_id) / 2)"
CALC_TOP_FOR_MIDDLE = "(var(--internal-height-$parent_id) / 2 - var(--external-height-$self_id) / 2)"
LEFT_FOR_CENTER = f"margin-left: 0; left: calc({CALC_LEFT_FOR_CENTER})"
TOP_FOR_MIDDLE = f"margin-top: 0; top: calc({CALC_TOP_FOR_MIDDLE})"


class At:
    def __init__(self, element: Element):
        self.element = element

    @staticmethod
    def prop(spec):
        def getter(self) -> Self:
            parent = self.element.parent_slot.parent
            if style := spec.get("style"):
                if isinstance(style, Template):
                    style = style.substitute({"parent_id": f"c{parent.id}", "self_id": f"c{self.element.id}"})
                self.element.style(style)
            if classes := spec.get("classes"):
                self.element.classes(classes)
            return self

        return property(getter)

    top = prop({"style": "left: 0; right: 0; top: 0"})
    bottom = prop({"style": "left: 0; right: 0; bottom: 0"})
    left = prop({"style": "left: 0; bottom: 0; top: 0"})
    right = prop({"style": "bottom: 0; right: 0; top: 0"})
    top_left = prop({"style": "left: 0; top: 0"})
    top_right = prop({"style": "right: 0; top: 0"})
    bottom_left = prop({"style": "left: 0; bottom: 0"})
    bottom_right = prop({"style": "right: 0; bottom: 0"})
    left_right = prop({"style": "left: 0; right: 0"})
    top_bottom = prop({"style": "top: 0; bottom: 0"})
    top_center = prop({"style": Template(f"top: 0; {LEFT_FOR_CENTER}")})
    bottom_center = prop({"style": Template(f"bottom: 0; {LEFT_FOR_CENTER}")})
    left_center = prop({"style": Template(f"left: 0; {TOP_FOR_MIDDLE}")})
    right_center = prop({"style": Template(f"right: 0; {TOP_FOR_MIDDLE}")})
    center = prop({"style": Template(f"{LEFT_FOR_CENTER}; {TOP_FOR_MIDDLE}")})
    fit_height = prop({"classes": "dynamic-height"})
    fit_width = prop({"classes": "dynamic-width"})
    fit_size = prop({"classes": "dynamic-size"})
    ignore_for_size = prop({"classes": "ignore-for-size"})

    def above(self, element: Elementish):
        self.a(center=center(element))
        self.a(bottom=top(element))
        return self

    def below(self, element: Elementish):
        self.a(center=center(element))
        self.a(top=bottom(element))
        return self

    def left_of(self, element: Elementish):
        self.a(middle=middle(element))
        self.a(right=left(element))
        return self

    def right_of(self, element: Elementish):
        self.a(middle=middle(element))
        self.a(left=right(element))
        return self

    def a(
        self,
        top=None,
        bottom=None,
        left=None,
        right=None,
        center=None,
        middle=None,
        width=None,
        height=None,
    ) -> Self:
        kwargs = {
            "top": top,
            "bottom": bottom,
            "left": left,
            "right": right,
            "center": center,
            "middle": middle,
            "width": width,
            "height": height,
        }

        for kwarg_name, anchor_value in kwargs.items():
            if anchor_value is None:
                continue

            if kwarg_name == "center":
                target_str = f"margin-left: 0px; left: calc(($source) - (var(--external-width-c{self.element.id}) / 2))"
            elif kwarg_name == "middle":
                target_str = f"margin-top: 0px; top: calc(($source) - (var(--external-height-c{self.element.id}) / 2))"
            else:
                target_str = f"{kwarg_name}: calc($source)"
            target_template = Template(target_str)

            if isinstance(anchor_value, Anchor):
                source_value = anchor_value.get_style(self.element, kwarg_name)
            elif isinstance(anchor_value, str):
                source_value = anchor_value
            elif isinstance(anchor_value, numbers.Number):
                source_value = f"{anchor_value}px"
            else:
                raise TypeError(f"Unexpected value type for {kwarg_name}: {type(anchor_value)}")

            full_style = target_template.substitute({"source": source_value})
            self.element.style(full_style)

        return self

    @property
    def tailwind(self) -> Tailwind:
        return self.element.tailwind

    def style(self, *args, **kwargs) -> Element:
        return self.element.style(*args, **kwargs)

    def classes(self, *args, **kwargs) -> Element:
        return self.element.classes(*args, **kwargs)

    def props(self, *args, **kwargs) -> Element:
        return self.element.props(*args, **kwargs)

    def __enter__(self) -> Self:
        return self.element.__enter__()

    def __exit__(self, *_) -> None:
        return self.element.__exit__(*_)


class Anchor:
    def __init__(
        self,
        element: Elementish,
        edge_name: str|None = None,
        dimension_name: str|None = None,
        direction_name: str|None = None,
    ):
        if [edge_name, dimension_name, direction_name].count(None) != 2:
            raise ValueError(
                "Provide exactly one of edge_name (top, left, ...), dimension_name (width, height), "
                "direction_name (vertical, horizontal)"
            )

        self.element = element
        self.edge_name = edge_name
        self.dimension_name = dimension_name
        self.direction_name = direction_name

        if isinstance(element, Element):
            element_id = element.id
        else:
            element_id = f"${element}_id"  # E.g. $parent_id for string Templating

        if edge_name:
            self.style = f"anchor(--c{element_id} {edge_name})"
        elif dimension_name:
            self.style = f"var(--internal-{dimension_name}-c{element_id})"
        elif direction_name == "horizontal":
            self.style = f"anchor(--c{element_id} left) + (var(--external-width-c{element_id}) / 2)"
        elif direction_name == "vertical":
            self.style = f"anchor(--c{element_id} top) + (var(--external-height-c{element_id}) / 2)"
        else:
            RuntimeError(f"Could not process values: {edge_name=}, {dimension_name=}, {direction_name=}")

    def __str__(self):
        return self.style

    def get_style(self, target_element: Element, target_anchor_name: str):
        parent_id = target_element.parent_slot.parent.id
        siblings = target_element.parent_slot.children
        previous_index = siblings.index(target_element) - 1
        previous_id = siblings[previous_index].id if previous_index >= 0 else ""

        return Template(self.style).substitute({"parent_id": parent_id, "previous_id": previous_id})

    def add_operation(self, operator, lhs, rhs):
        if isinstance(lhs, (int, float)):
            lhs = f"{lhs}px"
        if isinstance(rhs, (int, float)):
            rhs = f"{rhs}px"

        return self.add_plain_operation(operator, lhs, rhs)

    def add_plain_operation(self, operator, lhs, rhs):
        self.style = f"({lhs} {operator} {rhs})"
        return self

    def __add__(self, other):
        return self.add_operation("+", self, other)

    def __radd__(self, other):
        return self.add_operation("+", other, self)

    def __sub__(self, other):
        return self.add_operation("-", self, other)

    def __rsub__(self, other):
        return self.add_operation("-", other, self)

    def __mul__(self, other):
        return self.add_plain_operation("*", self, other)

    def __rmul__(self, other):
        return self.add_plain_operation("*", other, self)

    def __truediv__(self, other):
        return self.add_plain_operation("/", self, other)

    def __rtruediv__(self, other):
        return self.add_plain_operation("/", other, self)

    def __lt__(self, other):
        # Called for max()
        if isinstance(other, (int, float)):
            other = f"{other}px"
        self.style = f"max({self},{other})"
        return self

    def __gt__(self, other):
        # Called for min()
        if isinstance(other, (int, float)):
            other = f"{other}px"
        self.style = f"min({self},{other})"
        return self

    def __bool__(self):
        return False


parent: PseudoElement = "parent"
previous: PseudoElement = "previous"


def edge(edge_name: str, element: Elementish = parent) -> Anchor:
    return Anchor(element, edge_name=edge_name)

def direction(direction_name: str, element: Elementish = parent) -> Anchor:
    return Anchor(element, direction_name=direction_name)

def dimension(dimension_name: str, element: Elementish = parent) -> Anchor:
    return Anchor(element, dimension_name=dimension_name)

top = partial(edge, "top")
bottom = partial(edge, "bottom")
left = partial(edge, "left")
right = partial(edge, "right")

center = partial(direction, "horizontal")
middle = partial(direction, "vertical")

width = partial(dimension, "width")
height = partial(dimension, "height")
