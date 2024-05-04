import re
from typing import Callable, Dict, Union, Optional, Self, List, Set, Generator

from nicegui import ui
from nicegui.context import context
from nicegui.client import Client
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
                 browser_history: bool = True,
                 parent: Optional["SinglePageRouter"] = None,
                 page_template: Optional[Callable[[], Generator]] = None,
                 on_instance_created: Optional[Callable] = None,
                 **kwargs) -> None:
        """
        :param path: the base path of the single page router.
        :param browser_history: Optional flag to enable or disable the browser history management. Default is True.
        :param parent: The parent router of this router if this router is a nested router.
        :param page_template: Optional page template generator function which defines the layout of the page. It
            needs to yield a value to separate the layout from the content area.
        :param on_instance_created: Optional callback which is called when a new instance is created. Each browser tab
        or window is a new instance. This can be used to initialize the state of the application.
        :param kwargs: Additional arguments for the @page decorators
        """
        super().__init__()
        self.routes: Dict[str, SinglePageRouterEntry] = {}
        self.base_path = path
        self.included_paths: Set[str] = set()
        self.excluded_paths: Set[str] = set()
        self.on_instance_created: Optional[Callable] = on_instance_created
        self.use_browser_history = browser_history
        self.page_template = page_template
        self._setup_configured = False
        self.parent_router = parent
        if self.parent_router is not None:
            self.parent_router._register_child_router(self)
        self.child_routers: List["SinglePageRouter"] = []
        self.page_kwargs = kwargs

    def setup_pages(self, force=False) -> Self:
        for key, route in Client.page_routes.items():
            if route.startswith(
                    self.base_path.rstrip("/") + "/") and route.rstrip("/") not in self.included_paths:
                self.excluded_paths.add(route)
            if force:
                continue
            if self.base_path.startswith(route.rstrip("/") + "/"):  # '/sub_router' after '/' - forbidden
                raise ValueError(f'Another router with path "{route.rstrip("/")}/*" is already registered which '
                                 f'includes this router\'s base path "{self.base_path}". You can declare the nested '
                                 f'router first to prioritize it and avoid this issue.')

        @ui.page(self.base_path, **self.page_kwargs)
        @ui.page(f'{self.base_path}' + '{_:path}', **self.page_kwargs)  # all other pages
        async def root_page(request_data=None):
            initial_url = None
            if request_data is not None:
                initial_url = request_data["url"]["path"]
                query = request_data["url"].get("query", {})
                if query:
                    initial_url += "?" + query
            self.build_page(initial_url=initial_url)

        return self

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
                    return SinglePageTarget(entry=entry, router=self)
        else:
            resolved = None
            path = target.split("#")[0].split("?")[0]
            for cur_router in self.child_routers:
                if path.startswith((cur_router.base_path.rstrip("/") + "/")) or path == cur_router.base_path:
                    resolved = cur_router.resolve_target(target)
                    if resolved.valid:
                        target = cur_router.base_path
                        break
            parser = SinglePageTarget(target, router=self)
            result = parser.parse_single_page_route(self.routes, target)
            if resolved is not None:
                result.original_path = resolved.original_path
            return result

    def navigate_to(self, target: Union[Callable, str, SinglePageTarget], server_side=True) -> bool:
        """Navigate to a target

        :param target: The target to navigate to
        :param server_side: Optional flag which defines if the call is originated on the server side
        """
        org_target = target
        if not isinstance(target, SinglePageTarget):
            target = self.resolve_target(target)
        router_frame = context.client.single_page_router_frame
        if not target.valid or router_frame is None:
            return False
        router_frame.navigate_to(org_target, _server_side=server_side)
        return True

    def build_page_template(self) -> Generator:
        """Builds the page template. Needs to call insert_content_area at some point which defines the exchangeable
        content of the page.

        :return: The page template generator function"""
        if self.build_page_template is not None:
            return self.page_template()
        else:
            raise ValueError('No page template generator function provided.')

    def build_page(self, initial_url: Optional[str] = None):
        template = self.build_page_template()
        if not isinstance(template, Generator):
            raise ValueError('The page template method must yield a value to separate the layout from the content '
                             'area.')
        next(template)
        self.insert_content_area(initial_url)
        try:
            next(template)
        except StopIteration:
            pass

    def insert_content_area(self, initial_url: Optional[str] = None):
        """Setups the content area"""
        parent_router_frame = None
        for slot in reversed(context.slot_stack):  # we need to inform the parent router frame about
            if isinstance(slot.parent, RouterFrame):  # our existence so it can navigate to our pages
                parent_router_frame = slot.parent
                break
        content = RouterFrame(router=self,
                              included_paths=sorted(list(self.included_paths)),
                              excluded_paths=sorted(list(self.excluded_paths)),
                              use_browser_history=self.use_browser_history,
                              parent_router_frame=parent_router_frame,
                              target_url=initial_url)
        content.on_resolve(self.resolve_target)
        if parent_router_frame is None:  # register root routers to the client
            context.client.single_page_router_frame = content
        initial_url = content.target_url
        if initial_url is not None:
            content.navigate_to(initial_url, _server_side=False, _sync=True)

    def _register_child_router(self, router: "SinglePageRouter") -> None:
        """Registers a child router to the parent router"""
        self.child_routers.append(router)
