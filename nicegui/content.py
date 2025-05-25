from __future__ import annotations

import inspect
import re
from fnmatch import fnmatch
from typing import Any, AsyncGenerator, Awaitable, Callable, Dict, Generator, List, Optional, Self, Set, Union

from . import ui
from .builder_utils import run_safe
from .client import Client
from .content_view import ContentView
from .context import context
from .logging import log
from .single_page_router import SinglePageRouter
from .single_page_target import SinglePageTarget

PAGE_TEMPLATE_METHOD_NAME = 'page_template'


class Content:
    def __init__(self,
                 path: str,
                 *,
                 parent: Optional[Content] = None,
                 on_instance_created: Optional[Callable[[SinglePageRouter], None]] = None,
                 on_navigate: Optional[Callable[[str], Optional[Union[SinglePageTarget, str]]]] = None,
                 router_class: Optional[Callable[..., SinglePageRouter]] = None,
                 **kwargs) -> None:
        """Content: Building Single-Page Applications

        In NiceGUI, the content decorator facilitates the creation of single-page applications by enabling seamless
        transitions between views without full page reloads. The decorator allows defining the layout of the
        page once at the top level and then adding multiple views that are rendered inside the layout.

        The decorated function has to be a generator function containing a `yield` statement separating the layout from
        the content area. The actual content is added at the point where the yield statement is reached.


        Notes:

        - The `yield` statement can be used to return a dictionary of keyword arguments that are passed to each
          of its views. Such keyword arguments can be references to shared UI elements such as the sidebar or header but
          also any other data that should be shared between the views.
        - Content can be nested to create complex single page applications with multiple levels of navigation.
        - Linking and navigating via `ui.navigate` or `ui.link` works for content as for classic pages.

        :param path: route of the new page (path must start with '/')
        :param on_instance_created: Called when a new instance is created. Each browser tab creates is a new instance.
            This can be used to initialize the state of the application.
        :param on_navigate: Called when a navigation event is triggered. Can be used to
            prevent or modify the navigation. Return the new URL if the navigation should be allowed, modify the URL
            or return None to prevent the navigation.
        :param router_class: Class which is used to create the router instance. By default, SinglePageRouter is used.
        :param parent: The parent content.
        :param kwargs: additional keyword arguments passed to FastAPI's @app.get method
        """
        super().__init__()
        self.routes: Dict[str, ContentPath] = {}
        self.base_path = path
        self.included_paths: Set[str] = set()
        self.excluded_paths: Set[str] = set()
        self.on_instance_created: Optional[Callable] = on_instance_created
        self.on_navigate: Optional[Callable[[str], Optional[Union[SinglePageTarget, str]]]] = on_navigate
        self.use_browser_history = True
        self.page_template = None
        self._setup_configured = False
        self.parent_config = parent
        if self.parent_config is not None:
            self.parent_config._register_child(self)
        self.child_routers: List[Content] = []
        self.page_kwargs = kwargs
        self.router_class = SinglePageRouter if router_class is None else router_class
        self.content_builder: Union[
            None,
            Callable[..., Any],
            Callable[..., Awaitable[Any]],
            Generator[Dict[str, Any], None, None],
            AsyncGenerator[Dict[str, Any], None]
        ] = None
        if parent is None:
            Client.top_level_content[path] = self

    async def build_page_template(self, **kwargs):
        """Set up the content area for the single page router."""
        properties = {}

        def add_properties(result):
            if isinstance(result, dict):
                properties.update(result)

        if self.content_builder is None:
            raise ValueError(
                'The content builder function is not defined. Use the @content decorator to define it or '
                'pass it as an argument to the SinglePageRouter constructor.'
            )
        frame = run_safe(self.content_builder, **kwargs)
        if inspect.iscoroutine(frame):
            frame = await frame
        if frame is None:
            if self.routes:
                log.warning(f'The content function for "{self.base_path}" is not a generator (does not yield). '
                            'Sub-content will not be available.')
            return  # NOTE if content builder is not a generator, run_safe already added all content
        is_async = inspect.isasyncgen(frame)

        current_frame = SinglePageRouter.current_frame()
        if is_async:
            # Handle asynchronous generator function
            try:
                add_properties(await frame.__anext__())  # Insert UI elements before yield
                if current_frame is not None:
                    current_frame.update_user_data(properties)
                yield properties
                add_properties(await frame.__anext__())  # Insert UI elements after yield
                if current_frame is not None:
                    current_frame.update_user_data(properties)
            except StopAsyncIteration:
                pass
        else:
            # Handle synchronous generator function
            try:
                add_properties(next(frame))  # Insert UI elements before yield
                if current_frame is not None:
                    current_frame.update_user_data(properties)
                yield properties
                add_properties(next(frame))  # Insert UI elements after yield
                if current_frame is not None:
                    current_frame.update_user_data(properties)
            except StopIteration:
                pass

    def __call__(self, func: Callable[..., Any]) -> Self:
        """Decorator for the content builder function"""

        async def create_content(**kwargs):
            result = self.build_page(**kwargs)
            if inspect.isawaitable(result):
                await result

        self.content_builder = func
        if self.parent_config is None:
            self.setup_page()
        else:
            relative_path = self.base_path[len(self.parent_config.base_path):]
            ContentView(self.parent_config, relative_path)(create_content)
        return self

    def setup_page(self) -> Self:
        """Setup the NiceGUI page with all it's endpoints and their base UI structure for the root routers."""
        for _, route in Client.page_routes.items():
            if route.startswith(self.base_path.rstrip('/') + '/') and route.rstrip('/') not in self.included_paths:
                self.excluded_paths.add(route)

        @ui.page(self.base_path, **self.page_kwargs)
        @ui.page(f'{self.base_path}' + '{_:path}', **self.page_kwargs)  # all other pages
        async def root_page():
            await ui.context.client.connected(30.0)  # to ensure storage.tab and storage.client availability
            request = context.client.request
            initial_url = request.url.path
            query = request.url.query
            if query:
                initial_url += '?' + query
            await self.build_page(initial_url=initial_url)

        return self

    def add_view(self, path: str, builder: Callable, title: Optional[str] = None,
                 on_open: Optional[Callable[[SinglePageTarget], SinglePageTarget]] = None) -> None:
        """Add a new route to the single page router

        :param path: The path of the route, including FastAPI path parameters
        :param builder: The builder function (the view to be displayed)
        :param title: Optional title of the page
        :param on_open: Optional on_resolve function which is called when this path was selected.
        """
        path_mask = ContentPath.create_path_mask(path.rstrip('/'))
        self.included_paths.add(path_mask)
        self.routes[path] = ContentPath(path, builder, title, on_open=on_open).verify()

    def add_router_entry(self, entry: ContentPath) -> None:
        """Adds a fully configured ContentPath to the router

        :param entry: The ContentPath to add"""
        self.routes[entry.path] = entry.verify()

    def resolve_target(self, target: Union[Callable, str]) -> SinglePageTarget:
        """Tries to resolve a target such as a builder function or a URL path with route and query parameters.

        :param target: The URL path to open or a builder function
        :return: The resolved target. Defines .valid if the target is valid"""
        if callable(target):
            for route_target, entry in self.routes.items():
                if entry.builder == route_target:
                    return SinglePageTarget(router_path=entry)
            raise ValueError('The target builder function is not registered in the router.')
        resolved = None
        path = target.split('#')[0].split('?')[0]
        for router in self.child_routers:
            # replace {} placeholders with * to match the fnmatch pattern
            mask = ContentPath.create_path_mask(router.base_path.rstrip('/') + '/*')
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

    async def build_page(self, initial_url: Optional[str] = None, **kwargs) -> None:
        """Builds the page with the given initial URL

        :param initial_url: The initial URL to initialize the router's content with
        :param kwargs: Additional keyword arguments passed to the page template generator function"""
        kwargs['url_path'] = initial_url

        # Determine if build_page_template is asynchronous
        template = run_safe(self.build_page_template, **kwargs)
        # Initialize properties dictionary
        new_user_data = {}
        content_area = None

        def add_properties(result):
            if isinstance(result, dict):
                new_user_data.update(result)
        try:
            new_properties = await template.__anext__()  # Insert UI elements before yield
            add_properties(new_properties)
            content_area = self.create_router_instance(initial_url, user_data=new_user_data)
            new_properties = await template.__anext__()  # Insert UI elements after yield
            add_properties(new_properties)
        except StopAsyncIteration:
            pass
        if content_area:
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

        parent_router = SinglePageRouter.current_frame()
        prepare_arguments()
        content = self.router_class(content=self,
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
            content.navigate_to(initial_url, server_side=True, history=False)
        return content

    def content(self, path: str, **kwargs) -> Content:
        """Defines nested content

        :param path: The relative path of the content
        :param kwargs: Additional arguments for the nested content
        """
        abs_path = self.base_path.rstrip('/') + path
        return Content(abs_path, parent=self, **kwargs)

    @property
    def current_url(self) -> str:
        """Returns the current URL.

        Only works when called from within the content builder function.

        :return: The current URL"""
        cur_router = SinglePageRouter.current_frame()
        if cur_router is None:
            raise ValueError('The current URL can only be retrieved from within a nested content or view builder '
                             'function.')
        return cur_router.target_url

    def _register_child(self, router_config: Content) -> None:
        """Registers a child config to the parent router config"""
        self.child_routers.append(router_config)


class ContentPath:
    """A data class which holds the configuration of one router path"""

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
        """Verifies a ContentPath for correctness. Raises a ValueError if the entry is invalid."""
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

    def __repr__(self):
        return f'ContentPath(path={self.path}, builder={self.builder}, title={self.title}, on_open={self.on_open})'
