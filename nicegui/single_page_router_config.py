import re
import typing
from fnmatch import fnmatch
from typing import Callable, Dict, Union, Optional, Self, List, Set, Generator, Any

from nicegui import ui
from nicegui.context import context
from nicegui.client import Client
from nicegui.elements.router_frame import RouterFrame
from nicegui.single_page_router import SinglePageRouter
from nicegui.single_page_target import SinglePageTarget

if typing.TYPE_CHECKING:
    from nicegui.single_page_router import SinglePageRouter


class SinglePageRouterConfig:
    """The SinglePageRouterConfig allows the development of Single Page Applications (SPAs).

    It registers the root page of the SPAs at a given base path as FastAPI endpoint and manages the routing of nested
    routers."""

    def __init__(self,
                 path: str,
                 browser_history: bool = True,
                 parent: Optional['SinglePageRouterConfig'] = None,
                 page_template: Optional[Callable[[], Generator]] = None,
                 on_instance_created: Optional[Callable[['SinglePageRouter'], None]] = None,
                 on_resolve: Optional[Callable[[str], Optional[SinglePageTarget]]] = None,
                 on_open: Optional[Callable[[SinglePageTarget], SinglePageTarget]] = None,
                 on_navigate: Optional[Callable[[str], Optional[str]]] = None,
                 **kwargs) -> None:
        """:param path: the base path of the single page router.
        :param browser_history: Optional flag to enable or disable the browser history management. Default is True.
        :param parent: The parent router of this router if this router is a nested router.
        :param page_template: Optional page template generator function which defines the layout of the page. It
            needs to yield a value to separate the layout from the content area.
        :param on_instance_created: Optional callback which is called when a new router instance is created. Each
        :param on_resolve: Optional callback which is called when a URL path is resolved to a target. Can be used
            to resolve or redirect a URL path to a target.
        :param on_open: Optional callback which is called when a target is opened. Can be used to modify the target
            such as title or the actually called builder function.
        :param on_navigate: Optional callback which is called when a navigation event is triggered. Can be used to
            prevent or modify the navigation. Return the new URL if the navigation should be allowed, modify the URL
            or return None to prevent the navigation.
        browser tab or window is a new instance. This can be used to initialize the state of the application.
        :param kwargs: Additional arguments for the @page decorators"""
        super().__init__()
        self.routes: Dict[str, "SinglePageRouterPath"] = {}
        self.base_path = path
        self.included_paths: Set[str] = set()
        self.excluded_paths: Set[str] = set()
        self.on_instance_created: Optional[Callable] = on_instance_created
        self.on_resolve: Optional[Callable[[str], Optional[SinglePageTarget]]] = on_resolve
        self.on_open: Optional[Callable[[SinglePageTarget], SinglePageTarget]] = on_open
        self.on_navigate: Optional[Callable[[str], Optional[str]]] = on_navigate
        self.use_browser_history = browser_history
        self.page_template = page_template
        self._setup_configured = False
        self.parent_config = parent
        if self.parent_config is not None:
            self.parent_config._register_child_config(self)
        self.child_routers: List['SinglePageRouterConfig'] = []
        self.page_kwargs = kwargs

    def setup_pages(self, overwrite=False) -> Self:
        """Setups the NiceGUI page endpoints and their base UI structure for the root routers
        
        :param overwrite: Optional flag to force the setup of a given page even if one with a conflicting path is
            already existing. Default is False. Classes such as SinglePageApp use this flag to avoid conflicts with
            other routers and resolve those conflicts by rerouting the pages."""
        for key, route in Client.page_routes.items():
            if route.startswith(
                    self.base_path.rstrip('/') + '/') and route.rstrip('/') not in self.included_paths:
                self.excluded_paths.add(route)
            if overwrite:
                continue
            if self.base_path.startswith(route.rstrip('/') + '/'):  # '/sub_router' after '/' - forbidden
                raise ValueError(f'Another router with path "{route.rstrip("/")}/*" is already registered which '
                                 f'includes this router\'s base path "{self.base_path}". You can declare the nested '
                                 f'router first to prioritize it and avoid this issue.')

        @ui.page(self.base_path, **self.page_kwargs)
        @ui.page(f'{self.base_path}' + '{_:path}', **self.page_kwargs)  # all other pages
        async def root_page(request_data=None):
            await ui.context.client.connected()  # to ensure storage.tab and storage.client availability
            initial_url = None
            if request_data is not None:
                initial_url = request_data['url']['path']
                query = request_data['url'].get('query', None)
                if query:
                    initial_url += '?' + query
            self.build_page(initial_url=initial_url)

        return self

    def add_view(self, path: str, builder: Callable, title: Optional[str] = None,
                 on_open: Optional[Callable[[SinglePageTarget], SinglePageTarget]] = None) -> None:
        """Add a new route to the single page router

        :param path: The path of the route, including FastAPI path parameters
        :param builder: The builder function (the view to be displayed)
        :param title: Optional title of the page
        :param on_open: Optional on_resolve function which is called when this path was selected.
        """
        path_mask = SinglePageRouterPath.create_path_mask(path.rstrip('/'))
        self.included_paths.add(path_mask)
        self.routes[path] = SinglePageRouterPath(path, builder, title, on_open=on_open).verify()

    def add_router_entry(self, entry: 'SinglePageRouterPath') -> None:
        """Adds a fully configured SinglePageRouterPath to the router

        :param entry: The SinglePageRouterPath to add"""
        self.routes[entry.path] = entry.verify()

    def resolve_target(self, target: Union[Callable, str]) -> SinglePageTarget:
        """Tries to resolve a target such as a builder function or a URL path w/ route and query parameters.

        :param target: The URL path to open or a builder function
        :return: The resolved target. Defines .valid if the target is valid"""
        if isinstance(target, Callable):
            for target, entry in self.routes.items():
                if entry.builder == target:
                    return SinglePageTarget(router_path=entry)
        else:
            cur_config = self
            while cur_config is not None:  # try custom on_resolve functions first for manual resolution
                if cur_config.on_resolve is not None:
                    resolved = cur_config.on_resolve(target)
                    if resolved is not None:
                        return resolved
                cur_config = cur_config.parent_config
            resolved = None
            path = target.split('#')[0].split('?')[0]
            for cur_router in self.child_routers:
                # replace {} placeholders with * to match the fnmatch pattern
                mask = SinglePageRouterPath.create_path_mask(cur_router.base_path.rstrip('/') + '/*')
                if fnmatch(path, mask) or path == cur_router.base_path:
                    resolved = cur_router.resolve_target(target)
                    if resolved.valid:
                        target = cur_router.base_path
                        if '*' in mask:
                            # isolate the real path elements and update target accordingly
                            target = '/'.join(path.split('/')[:len(cur_router.base_path.split('/'))])
                        break
            result = SinglePageTarget(target).parse_url_path(routes=self.routes)
            if resolved is not None:
                result.original_path = resolved.original_path
            return result

    def navigate_to(self, target: Union[Callable, str, SinglePageTarget], server_side=True) -> bool:
        """Navigate to a target

        :param target: The target to navigate to
        :param server_side: Optional flag which defines if the call is originated on the server side"""
        org_target = target
        if not isinstance(target, SinglePageTarget):
            target = self.resolve_target(target)
        router = context.client.single_page_router
        if not target.valid or router is None:
            return False
        router.navigate_to(org_target, server_side=server_side)
        return True

    def handle_navigate(self, url: str) -> Optional[str]:
        """Handles a navigation event and returns the new URL if the navigation should be allowed

        :param url: The URL to navigate to
        :return: The new URL if the navigation should be allowed, None otherwise"""
        if self.on_navigate is not None:
            new_url = self.on_navigate(url)
            if new_url != url:
                return new_url
        if self.parent_config is not None:
            return self.parent_config.handle_navigate(url)
        return url

    def build_page_template(self) -> Generator:
        """Builds the page template. Needs to call insert_content_area at some point which defines the exchangeable
        content of the page.

        :return: The page template generator function"""

        def default_template():
            yield

        if self.page_template is not None:
            return self.page_template()
        else:
            return default_template()

    def build_page(self, initial_url: Optional[str] = None, **kwargs) -> None:
        """Builds the page with the given initial URL

        :param initial_url: The initial URL to initialize the router's content with
        :param kwargs: Additional keyword arguments passed to the page template generator function"""
        kwargs['url_path'] = initial_url
        template = RouterFrame.run_safe(self.build_page_template, **kwargs)
        if not isinstance(template, Generator):
            raise ValueError('The page template method must yield a value to separate the layout from the content '
                             'area.')
        new_user_data = {}
        new_properties = next(template)
        if isinstance(new_properties, dict):
            new_user_data.update(new_properties)
        content_area = self.create_router_instance(initial_url, user_data=new_user_data)
        try:
            new_properties = next(template)
            if isinstance(new_properties, dict):
                new_user_data.update(new_properties)
        except StopIteration:
            pass
        content_area.update_user_data(new_user_data)

    def create_router_instance(self,
                               initial_url: Optional[str] = None,
                               user_data: Optional[Dict] = None) -> SinglePageRouter:
        """Creates a new router instance for the current visitor.

        :param initial_url: The initial URL to initialize the router's content with
        :param user_data: Optional user data to pass to the content area
        :return: The created router instance"""
        parent_router = SinglePageRouter.get_current_router()
        content = SinglePageRouter(config=self,
                                   included_paths=sorted(list(self.included_paths)),
                                   excluded_paths=sorted(list(self.excluded_paths)),
                                   use_browser_history=self.use_browser_history,
                                   parent_router=parent_router,
                                   target_url=initial_url,
                                   user_data=user_data)
        if parent_router is None:  # register root routers to the client
            context.client.single_page_router = content
        initial_url = content.target_url
        if self.on_instance_created is not None:
            self.on_instance_created(content)
        if initial_url is not None:
            content.navigate_to(initial_url, server_side=True, sync=True, history=False)
        return content

    def _register_child_config(self, router_config: 'SinglePageRouterConfig') -> None:
        """Registers a child router config to the parent router config"""
        self.child_routers.append(router_config)


class SinglePageRouterPath:
    """The SinglePageRouterPath is a data class which holds the configuration of one router path"""

    def __init__(self, path: str, builder: Callable, title: Union[str, None] = None,
                 on_open: Optional[Callable[[SinglePageTarget, Any], SinglePageTarget]] = None):
        """
        :param path: The path of the route
        :param builder: The builder function which is called when the route is opened
        :param title: Optional title of the page
        :param on_open: Optional on_resolve function which is called when this path was selected."""
        self.path = path
        self.builder = builder
        self.title = title
        self.on_open = on_open

    def verify(self) -> Self:
        """Verifies a SinglePageRouterPath for correctness. Raises a ValueError if the entry is invalid."""
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
        :return: The mask with all path parameters replaced by a wildcard"""
        return re.sub(r'{[^}]+}', '*', path)
