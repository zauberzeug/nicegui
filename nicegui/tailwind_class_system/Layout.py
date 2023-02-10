
from typing import Literal
from nicegui.element import Element

AspectRatio = Literal["aspect-auto","aspect-square","aspect-video"]

Container = Literal["container"]

Columns = Literal["columns-1","columns-2","columns-3","columns-4","columns-5","columns-6","columns-7","columns-8","columns-9","columns-10","columns-11","columns-12","columns-auto","columns-3xs","columns-2xs","columns-xs","columns-sm","columns-md","columns-lg","columns-xl","columns-2xl","columns-3xl","columns-4xl","columns-5xl","columns-6xl","columns-7xl"]

BreakAfter = Literal["break-after-auto","break-after-avoid","break-after-all","break-after-avoid-page","break-after-page","break-after-left","break-after-right","break-after-column"]

BreakBefore = Literal["break-before-auto","break-before-avoid","break-before-all","break-before-avoid-page","break-before-page","break-before-left","break-before-right","break-before-column"]

BreakInside = Literal["break-inside-auto","break-inside-avoid","break-inside-avoid-page","break-inside-avoid-column"]

BoxDecorationBreak = Literal["box-decoration-clone","box-decoration-slice"]

BoxSizing = Literal["box-border","box-content"]

Display = Literal["block","inline-block","inline","flex","inline-flex","table","inline-table","table-caption","table-cell","table-column","table-column-group","table-footer-group","table-header-group","table-row-group","table-row","flow-root","grid","inline-grid","contents","list-item","hidden"]

Floats = Literal["float-right","float-left","float-none"]

Clear = Literal["clear-left","clear-right","clear-both","clear-none"]

Isolation = Literal["isolate","isolation-auto"]

ObjectFit = Literal["object-contain","object-cover","object-fill","object-none","object-scale-down"]

ObjectPosition = Literal["object-bottom","object-center","object-left","object-left-bottom","object-left-top","object-right","object-right-bottom","object-right-top","object-top"]

Overflow = Literal["overflow-auto","overflow-hidden","overflow-clip","overflow-visible","overflow-scroll","overflow-x-auto","overflow-y-auto","overflow-x-hidden","overflow-y-hidden","overflow-x-clip","overflow-y-clip","overflow-x-visible","overflow-y-visible","overflow-x-scroll","overflow-y-scroll"]

OverscrollBehavior = Literal["overscroll-auto","overscroll-contain","overscroll-none","overscroll-y-auto","overscroll-y-contain","overscroll-y-none","overscroll-x-auto","overscroll-x-contain","overscroll-x-none"]

Position = Literal["static","fixed","absolute","relative","sticky"]

TopRightBottomLeft = Literal["inset-0","inset-x-0","inset-y-0","top-0","right-0","bottom-0","left-0","inset-px","inset-x-px","inset-y-px","top-px","right-px","bottom-px","left-px","inset-0.5","inset-x-0.5","inset-y-0.5","top-0.5","right-0.5","bottom-0.5","left-0.5","inset-1","inset-x-1","inset-y-1","top-1","right-1","bottom-1","left-1","inset-1.5","inset-x-1.5","inset-y-1.5","top-1.5","right-1.5","bottom-1.5","left-1.5","inset-2","inset-x-2","inset-y-2","top-2","right-2","bottom-2","left-2","inset-2.5","inset-x-2.5","inset-y-2.5","top-2.5","right-2.5","bottom-2.5","left-2.5","inset-3","inset-x-3","inset-y-3","top-3","right-3","bottom-3","left-3","inset-3.5","inset-x-3.5","inset-y-3.5","top-3.5","right-3.5","bottom-3.5","left-3.5","inset-4","inset-x-4","inset-y-4","top-4","right-4","bottom-4","left-4","inset-5","inset-x-5","inset-y-5","top-5","right-5","bottom-5","left-5","inset-6","inset-x-6","inset-y-6","top-6","right-6","bottom-6","left-6","inset-7","inset-x-7","inset-y-7","top-7","right-7","bottom-7","left-7","inset-8","inset-x-8","inset-y-8","top-8","right-8","bottom-8","left-8","inset-9","inset-x-9","inset-y-9","top-9","right-9","bottom-9","left-9","inset-10","inset-x-10","inset-y-10","top-10","right-10","bottom-10","left-10","inset-11","inset-x-11","inset-y-11","top-11","right-11","bottom-11","left-11","inset-12","inset-x-12","inset-y-12","top-12","right-12","bottom-12","left-12","inset-14","inset-x-14","inset-y-14","top-14","right-14","bottom-14","left-14","inset-16","inset-x-16","inset-y-16","top-16","right-16","bottom-16","left-16","inset-20","inset-x-20","inset-y-20","top-20","right-20","bottom-20","left-20","inset-24","inset-x-24","inset-y-24","top-24","right-24","bottom-24","left-24","inset-28","inset-x-28","inset-y-28","top-28","right-28","bottom-28","left-28","inset-32","inset-x-32","inset-y-32","top-32","right-32","bottom-32","left-32","inset-36","inset-x-36","inset-y-36","top-36","right-36","bottom-36","left-36","inset-40","inset-x-40","inset-y-40","top-40","right-40","bottom-40","left-40","inset-44","inset-x-44","inset-y-44","top-44","right-44","bottom-44","left-44","inset-48","inset-x-48","inset-y-48","top-48","right-48","bottom-48","left-48","inset-52","inset-x-52","inset-y-52","top-52","right-52","bottom-52","left-52","inset-56","inset-x-56","inset-y-56","top-56","right-56","bottom-56","left-56","inset-60","inset-x-60","inset-y-60","top-60","right-60","bottom-60","left-60","inset-64","inset-x-64","inset-y-64","top-64","right-64","bottom-64","left-64","inset-72","inset-x-72","inset-y-72","top-72","right-72","bottom-72","left-72","inset-80","inset-x-80","inset-y-80","top-80","right-80","bottom-80","left-80","inset-96","inset-x-96","inset-y-96","top-96","right-96","bottom-96","left-96","inset-auto","inset-1/2","inset-1/3","inset-2/3","inset-1/4","inset-2/4","inset-3/4","inset-full","inset-x-auto","inset-x-1/2","inset-x-1/3","inset-x-2/3","inset-x-1/4","inset-x-2/4","inset-x-3/4","inset-x-full","inset-y-auto","inset-y-1/2","inset-y-1/3","inset-y-2/3","inset-y-1/4","inset-y-2/4","inset-y-3/4","inset-y-full","top-auto","top-1/2","top-1/3","top-2/3","top-1/4","top-2/4","top-3/4","top-full","right-auto","right-1/2","right-1/3","right-2/3","right-1/4","right-2/4","right-3/4","right-full","bottom-auto","bottom-1/2","bottom-1/3","bottom-2/3","bottom-1/4","bottom-2/4","bottom-3/4","bottom-full","left-auto","left-1/2","left-1/3","left-2/3","left-1/4","left-2/4","left-3/4","left-full"]

Visibility = Literal["visible","invisible","collapse"]

ZIndex = Literal["z-0","z-10","z-20","z-30","z-40","z-50","z-auto"]


class Layout:
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


    def aspect_ratio(self, _ratio: AspectRatio):
        """
        Utilities for controlling the aspect ratio of an element.
        """
        self.__add(_ratio)
        return self
        

    def container(self, _container: Container):
        """
        A component for fixing an element's width to the current breakpoint.
        """
        self.__add(_container)
        return self
        

    def columns(self, _columns: Columns):
        """
        Utilities for controlling the number of columns within an element.
        """
        self.__add(_columns)
        return self
        

    def break_after(self, _after: BreakAfter):
        """
        Utilities for controlling how a column or page should break after an element.
        """
        self.__add(_after)
        return self
        

    def break_before(self, _before: BreakBefore):
        """
        Utilities for controlling how a column or page should break before an element.
        """
        self.__add(_before)
        return self
        

    def break_inside(self, _inside: BreakInside):
        """
        Utilities for controlling how a column or page should break within an element.
        """
        self.__add(_inside)
        return self
        

    def box_decoration_break(self, _break: BoxDecorationBreak):
        """
        Utilities for controlling how element fragments should be rendered across multiple lines, columns, or pages.
        """
        self.__add(_break)
        return self
        

    def box_sizing(self, _sizing: BoxSizing):
        """
        Utilities for controlling how the browser should calculate an element's total size.
        """
        self.__add(_sizing)
        return self
        

    def display(self, _display: Display):
        """
        Utilities for controlling the display box type of an element.
        """
        self.__add(_display)
        return self
        

    def floats(self, _floats: Floats):
        """
        Utilities for controlling the wrapping of content around an element.
        """
        self.__add(_floats)
        return self
        

    def clear(self, _clear: Clear):
        """
        Utilities for controlling the wrapping of content around an element.
        """
        self.__add(_clear)
        return self
        

    def isolation(self, _isolation: Isolation):
        """
        Utilities for controlling whether an element should explicitly create a new stacking context.
        """
        self.__add(_isolation)
        return self
        

    def object_fit(self, _fit: ObjectFit):
        """
        Utilities for controlling how a replaced element's content should be resized.
        """
        self.__add(_fit)
        return self
        

    def object_position(self, _position: ObjectPosition):
        """
        Utilities for controlling how a replaced element's content should be positioned within its container.
        """
        self.__add(_position)
        return self
        

    def overflow(self, _overflow: Overflow):
        """
        Utilities for controlling how an element handles content that is too large for the container.
        """
        self.__add(_overflow)
        return self
        

    def overscroll_behavior(self, _behavior: OverscrollBehavior):
        """
        Utilities for controlling how the browser behaves when reaching the boundary of a scrolling area.
        """
        self.__add(_behavior)
        return self
        

    def position(self, _position: Position):
        """
        Utilities for controlling how an element is positioned in the DOM.
        """
        self.__add(_position)
        return self
        

    def toprightbottomleft(self, _left: TopRightBottomLeft):
        """
        Utilities for controlling the placement of positioned elements.
        """
        self.__add(_left)
        return self
        

    def visibility(self, _visibility: Visibility):
        """
        Utilities for controlling the visibility of an element.
        """
        self.__add(_visibility)
        return self
        

    def z_index(self, _z_index: ZIndex):
        """
        Utilities for controlling the stack order of an element.
        """
        self.__add(_z_index)
        return self
        