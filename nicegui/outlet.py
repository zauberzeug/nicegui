from typing import Any, Callable, Generator, Optional, Self, Union, Dict, Set, List

import inspect
import re
from fnmatch import fnmatch

from nicegui import ui
from nicegui.client import Client
from nicegui.elements.router_frame import RouterFrame
from nicegui.outlet_view import OutletView
from nicegui.single_page_router import SinglePageRouter
from nicegui.single_page_target import SinglePageTarget
from nicegui.context import context

PAGE_TEMPLATE_METHOD_NAME = "page_template"


class Outlet:
    """An outlet allows the creation of single page applications which do not reload the page when navigating between
    different views. The outlet is a container for multiple views and can contain further, nested outlets.

    To define a new outlet, use the @ui.outlet decorator on a function which defines the layout of the outlet.
    The layout function must be a generator function and contain a yield statement to separate the layout from the
    actual content area. The yield can also be used to pass properties to the content are by return a dictionary
    with the properties. Each property can be received as function argument in all nested views and outlets.

    Once the outlet is defined, multiple views can be added to the outlet using the @<outlet_function>.view decorator on
    a function."""

    def __init__(self,
                 path: str,
                 outlet_builder: Optional[Callable] = None,
                 browser_history: bool = True,
                 parent: Optional['Outlet'] = None,
                 on_instance_created: Optional[Callable[['SinglePageRouter'], None]] = None,
                 on_navigate: Optional[Callable[[str], Optional[Union[SinglePageTarget, str]]]] = None,
                 router_class: Optional[Callable[..., SinglePageRouter]] = None,
                 **kwargs) -> None:
        """
        :param path: the base path of the single page router.
        :param outlet_builder: A layout definition function which defines the layout of the page. The layout builder
            must be a generator function and contain a yield statement to separate the layout from the content area.
        :param layout_builder: A layout builder function which defines the layout of the page. The layout builder
            must be a generator function and contain a yield statement to separate the layout from the content area.
        :param browser_history: Optional flag to enable or disable the browser history management. Default is True.
        :param on_instance_created: Optional callback which is called when a new instance is created. Each browser tab
        or window is a new instance. This can be used to initialize the state of the application.
        :param on_navigate: Optional callback which is called when a navigation event is triggered. Can be used to
            prevent or modify the navigation. Return the new URL if the navigation should be allowed, modify the URL
            or return None to prevent the navigation.
        :param router_class: Optional class which is used to create the router instance. The class must be a subclass
            of SinglePageRouter. If not provided, the default SinglePageRouter is used.

            If the class defines a method with the name 'page_template', this method is used as the outlet builder.
        :param parent: The parent outlet of this outlet.
        :param kwargs: Additional arguments
        """
        super().__init__()
        self.routes: Dict[str, 'OutletPath'] = {}
        self.base_path = path
        self.included_paths: Set[str] = set()
        self.excluded_paths: Set[str] = set()
        self.on_instance_created: Optional[Callable] = on_instance_created
        self.on_navigate: Optional[Callable[[str], Optional[Union[SinglePageTarget, str]]]] = on_navigate
        self.use_browser_history = browser_history
        self.page_template = None
        self._setup_configured = False
        self.parent_config = parent
        if self.parent_config is not None:
            self.parent_config._register_child_outlet(self)
        self.child_routers: List['Outlet'] = []
        self.page_kwargs = kwargs
        self.router_class = SinglePageRouter if router_class is None else router_class
        self.outlet_builder: Optional[Callable] = None
        if parent is None:
            Client.top_level_outlets[path] = self
        if router_class is not None:
            # check if class defines outlet builder function
            if hasattr(router_class, PAGE_TEMPLATE_METHOD_NAME):
                outlet_builder = getattr(router_class, PAGE_TEMPLATE_METHOD_NAME)
        if outlet_builder is not None:
            self(outlet_builder)

    def build_page_template(self, **kwargs):
        """Setups the content area for the single page router"""
        if self.outlet_builder is None:
            raise ValueError('The outlet builder function is not defined. Use the @outlet decorator to define it or'
                             ' pass it as an argument to the SinglePageRouter constructor.')
        frame = RouterFrame.run_safe(self.outlet_builder, **kwargs)
        # if not isinstance(frame, Generator):
        #     raise ValueError('The outlet builder must be a generator function and contain a yield statement'
        #                      ' to separate the layout from the content area.')
        properties = {}

        def add_properties(result):
            if isinstance(result, dict):
                properties.update(result)

        router_frame = SinglePageRouter.current_router()
        if isinstance(frame, Generator):
            add_properties(next(frame))  # insert ui elements before yield
        if router_frame is not None:
            router_frame.update_user_data(properties)
        yield properties
        try:
            if isinstance(frame, Generator):
                add_properties(next(frame))  # if provided insert ui elements after yield
            if router_frame is not None:
                router_frame.update_user_data(properties)
        except StopIteration:
            pass

    def __call__(self, func: Callable[..., Any]) -> Self:
        """Decorator for the layout builder / "outlet" function"""

        def outlet_view(**kwargs):
            self.build_page(**kwargs)

        self.outlet_builder = func
        if self.parent_config is None:
            self.setup_page()
        else:
            relative_path = self.base_path[len(self.parent_config.base_path):]
            OutletView(self.parent_config, relative_path)(outlet_view)
        return self

    def setup_page(self, overwrite=False) -> Self:
        """Setup the NiceGUI page with all it's endpoints and their base UI structure for the root routers

        :param overwrite: Optional flag to force the setup of a given page even if one with a conflicting path is
            already existing. Default is False. Classes such as SinglePageApp use this flag to avoid conflicts with
            other routers and resolve those conflicts by rerouting the pages."""
        for key, route in Client.page_routes.items():
            if route.startswith(self.base_path.rstrip('/') + '/') and route.rstrip('/') not in self.included_paths:
                self.excluded_paths.add(route)
            if overwrite:
                continue
            if self.base_path.startswith(route.rstrip('/') + '/'):  # '/sub_router' after '/' - forbidden
                raise ValueError(f'Another router with path "{route.rstrip("/")}/*" is already registered which '
                                 f'includes this router\'s base path "{self.base_path}". You can declare the nested '
                                 f'router first to prioritize it and avoid this issue.')

        @ui.page(self.base_path, **self.page_kwargs)
        @ui.page(f'{self.base_path}' + '{_:path}', **self.page_kwargs)  # all other pages
        async def root_page():
            await ui.context.client.connected()  # to ensure storage.tab and storage.client availability
            request = context.client.request
            initial_url = request.url.path
            query = request.url.query
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
        path_mask = OutletPath.create_path_mask(path.rstrip('/'))
        self.included_paths.add(path_mask)
        self.routes[path] = OutletPath(path, builder, title, on_open=on_open).verify()

    def add_router_entry(self, entry: 'OutletPath') -> None:
        """Adds a fully configured OutletPath to the router

        :param entry: The OutletPath to add"""
        self.routes[entry.path] = entry.verify()

    def resolve_target(self, target: Union[Callable, str]) -> SinglePageTarget:
        """Tries to resolve a target such as a builder function or a URL path with route and query parameters.

        :param target: The URL path to open or a builder function
        :return: The resolved target. Defines .valid if the target is valid"""
        if callable(target):
            for target, entry in self.routes.items():
                if entry.builder == target:
                    return SinglePageTarget(router_path=entry)
            raise ValueError('The target builder function is not registered in the router.')
        resolved = None
        path = target.split('#')[0].split('?')[0]
        for router in self.child_routers:
            # replace {} placeholders with * to match the fnmatch pattern
            mask = OutletPath.create_path_mask(router.base_path.rstrip('/') + '/*')
            if fnmatch(path, mask) or path == router.base_path:
                resolved = router.resolve_target(target)
                if resolved.valid:
                    target = router.base_path
                    if '*' in mask:
                        # isolate the real path elements and update target accordingly
                        target = '/'.join(path.split('/')[:len(router.base_path.split('/'))])
                    break
        result = SinglePageTarget(target).parse_url_path(routes=self.routes)
        if resolved is not None:
            result.original_path = resolved.original_path
        return result

    def handle_navigate(self, url: str) -> Optional[Union[SinglePageTarget, str]]:
        """Handles a navigation event and returns the new URL if the navigation should be allowed

        :param url: The URL to navigate to
        :return: The new URL if the navigation should be allowed, None otherwise"""
        if self.on_navigate is not None:
            new_target = self.on_navigate(url)
            if isinstance(new_target, SinglePageTarget):
                return new_target
            if new_target != url:
                return new_target
        if self.parent_config is not None:
            return self.parent_config.handle_navigate(url)
        return url

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

        user_data_kwargs = {}

        def prepare_arguments():
            nonlocal parent_router, user_data_kwargs
            init_params = inspect.signature(self.router_class.__init__).parameters
            param_names = set(init_params.keys()) - {'self'}
            user_data_kwargs = {k: v for k, v in user_data.items() if k in param_names}
            cur_parent = parent_router
            while cur_parent is not None:
                user_data_kwargs.update({k: v for k, v in cur_parent.user_data.items() if k in param_names})
                cur_parent = cur_parent.parent

        parent_router = SinglePageRouter.current_router()
        prepare_arguments()
        content = self.router_class(config=self,
                                    included_paths=sorted(list(self.included_paths)),
                                    excluded_paths=sorted(list(self.excluded_paths)),
                                    use_browser_history=self.use_browser_history,
                                    parent=parent_router,
                                    target_url=initial_url,
                                    user_data=user_data,
                                    **user_data_kwargs)
        if parent_router is None:  # register root routers to the client
            context.client.single_page_router = content
        initial_url = content.target_url
        if self.on_instance_created is not None:
            self.on_instance_created(content)
        if initial_url is not None:
            content.navigate_to(initial_url, server_side=True, sync=True, history=False)
        return content

    def view(self,
             path: str,
             title: Optional[str] = None
             ) -> 'OutletView':
        """Decorator for the view function.

        With the view function you define the actual content of the page. The view function is called when the user
        navigates to the specified path relative to the outlet's base path.

        :param path: The path of the view, relative to the base path of the outlet
        :param title: Optional title of the view. If a title is set, it will be displayed in the browser tab
            when the view is active, otherwise the default title of the application is displayed.
        """
        return OutletView(self, path, title=title)

    def outlet(self, path: str, **kwargs) -> 'Outlet':
        """Defines a nested outlet

        :param path: The relative path of the outlet
        :param kwargs: Additional arguments for the nested ui.outlet
        """
        abs_path = self.base_path.rstrip('/') + path
        return Outlet(abs_path, parent=self, **kwargs)

    @property
    def current_url(self) -> str:
        """Returns the current URL of the outlet.

        Only works when called from within the outlet or view builder function.

        :return: The current URL of the outlet"""
        cur_router = SinglePageRouter.current_router()
        if cur_router is None:
            raise ValueError('The current URL can only be retrieved from within a nested outlet or view builder '
                             'function.')
        return cur_router.target_url

    def _register_child_outlet(self, router_config: 'Outlet') -> None:
        """Registers a child outlet config to the parent router config"""
        self.child_routers.append(router_config)


class OutletPath:
    """The OutletPath is a data class which holds the configuration of one router path"""

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
        """Verifies a OutletPath for correctness. Raises a ValueError if the entry is invalid."""
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
