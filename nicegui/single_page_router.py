import fnmatch
import re
from functools import wraps
from typing import Callable, Dict, Union, Optional, Tuple, Self, List, Set, Any, Generator

from fastapi.routing import APIRoute

from nicegui import background_tasks, helpers, ui, core, context
from nicegui.elements.router_frame import RouterFrame
from nicegui.single_page_target import SinglePageTarget


class SinglePageRouterEntry:
    """The SinglePageRouterEntry is a data class which holds the configuration of a single page router route"""

    def __init__(self, path: str, builder: Callable, title: Union[str, None] = None):
        """
        :param path: The path of the route
        :param builder: The builder function which is called when the route is opened
        :param title: Optional title of the page
        """
        self.path = path
        self.builder = builder
        self.title = title

    def verify(self) -> Self:
        """Verifies a SinglePageRouterEntry for correctness. Raises a ValueError if the entry is invalid."""
        path = self.path
        if '{' in path:
            # verify only a single open and close curly bracket is present
            elements = path.split('/')
            for cur_element in elements:
                if '{' in cur_element:
                    if cur_element.count('{') != 1 or cur_element.count('}') != 1 or len(cur_element) < 3 or \
                            not (cur_element.startswith('{') and cur_element.endswith('}')):
                        raise ValueError('Only simple path parameters are supported. /path/{value}/{another_value}\n'
                                         f'failed for path: {path}')
        return self

    @staticmethod
    def create_path_mask(path: str) -> str:
        """Converts a path to a mask which can be used for fnmatch matching

        /site/{value}/{other_value} --> /site/*/*
        :param path: The path to convert
        :return: The mask with all path parameters replaced by a wildcard
        """
        return re.sub(r'{[^}]+}', '*', path)


class SinglePageRouter:
    """The SinglePageRouter allows the development of a Single Page Application (SPA).

    SPAs are web applications which load a single HTML page and dynamically update the content of the page.
    This allows faster page switches and a more dynamic user experience."""

    def __init__(self,
                 path: str,
                 outlet_builder: Optional[Callable] = None,
                 browser_history: bool = True,
                 parent: Optional["SinglePageRouter"] = None,
                 on_instance_created: Optional[Callable] = None,
                 **kwargs) -> None:
        """
        :param path: the base path of the single page router.
        :param outlet_builder: A layout definition function which defines the layout of the page. The layout builder
            must be a generator function and contain a yield statement to separate the layout from the content area.
        :param browser_history: Optional flag to enable or disable the browser history management. Default is True.
        :param parent: The parent router of this router if this router is a nested router.
        :param on_instance_created: Optional callback which is called when a new instance is created. Each browser tab
        or window is a new instance. This can be used to initialize the state of the application.
        :param kwargs: Additional arguments for the @page decorators
        """
        super().__init__()
        self.routes: Dict[str, SinglePageRouterEntry] = {}
        self.base_path = path
        self.included_paths: Set[str] = set()
        self.on_instance_created: Optional[Callable] = on_instance_created
        self.use_browser_history = browser_history
        self._setup_configured = False
        self.outlet_builder: Optional[Callable] = outlet_builder
        self.parent_router = parent
        if self.parent_router is not None:
            self.parent_router._register_child_router(self)
        self.child_routers: List["SinglePageRouter"] = []
        self.page_kwargs = kwargs

    def setup_pages(self):
        @ui.page(self.base_path, **self.page_kwargs)
        @ui.page(f'{self.base_path}' + '{_:path}', **self.page_kwargs)  # all other pages
        async def root_page():
            self.setup_content_area()

    def add_view(self, path: str, builder: Callable, title: Optional[str] = None) -> None:
        """Add a new route to the single page router

        :param path: The path of the route, including FastAPI path parameters
        :param builder: The builder function (the view to be displayed)
        :param title: Optional title of the page
        """
        path_mask = SinglePageRouterEntry.create_path_mask(path.rstrip('/'))
        self.included_paths.add(path_mask)
        self.routes[path] = SinglePageRouterEntry(path, builder, title).verify()

    def add_router_entry(self, entry: SinglePageRouterEntry) -> None:
        """Adds a fully configured SinglePageRouterEntry to the router

        :param entry: The SinglePageRouterEntry to add
        """
        self.routes[entry.path] = entry.verify()

    def resolve_target(self, target: Union[Callable, str]) -> SinglePageTarget:
        """Tries to resolve a target such as a builder function or an URL path w/ route and query parameters.

        :param target: The URL path to open or a builder function
        :return: The resolved target. Defines .valid if the target is valid
        """
        if isinstance(target, Callable):
            for target, entry in self.routes.items():
                if entry.builder == target:
                    return SinglePageTarget(entry=entry)
        else:
            for cur_router in self.child_routers:
                if target.startswith((cur_router.base_path.rstrip("/")+"/")) or target == cur_router.base_path:
                    target = cur_router.base_path
                    break
            parser = SinglePageTarget(target)
            return parser.parse_single_page_route(self.routes, target)

    def navigate_to(self, target: Union[Callable, str, SinglePageTarget]) -> bool:
        """Navigate to a target

        :param target: The target to navigate to
        """
        if not isinstance(target, SinglePageTarget):
            target = self.resolve_target(target)
        router_frame = context.get_client().single_page_router_frame
        if not target.valid or router_frame is None:
            return False
        router_frame.navigate_to(target)
        return True

    def setup_content_area(self):
        """Setups the content area for the single page router
        """
        if self.outlet_builder is None:
            raise ValueError('The outlet builder function is not defined. Use the @outlet decorator to define it or'
                             ' pass it as an argument to the SinglePageRouter constructor.')
        frame = self.outlet_builder()
        if not isinstance(frame, Generator):
            raise ValueError('The outlet builder must be a generator function and contain a yield statement'
                             ' to separate the layout from the content area.')
        next(frame)  # insert ui elements before yield
        parent_router_frame = None
        for slot in reversed(context.get_slot_stack()):  # we need to inform the parent router frame abot
            if isinstance(slot.parent, RouterFrame):  # our existence so it can navigate to our pages
                parent_router_frame = slot.parent
                break
        content = RouterFrame(base_path=self.base_path,
                              valid_path_masks=list(self.included_paths),
                              use_browser_history=self.use_browser_history,
                              parent_router_frame=parent_router_frame)  # exchangeable content of the page
        if parent_router_frame is None:  # register root routers to the client
            context.get_client().single_page_router_frame = content
        content.on_resolve(self.resolve_target)
        try:
            next(frame)  # if provided insert ui elements after yield
        except StopIteration:
            pass

    def _register_child_router(self, router: "SinglePageRouter") -> None:
        """Registers a child router to the parent router"""
        self.child_routers.append(router)
