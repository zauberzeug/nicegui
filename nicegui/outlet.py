from typing import Any, Callable, Generator, Optional, Self, Union

from nicegui.client import Client
from nicegui.elements.router_frame import RouterFrame
from nicegui.single_page_router import SinglePageRouter
from nicegui.single_page_router_config import SinglePageRouterConfig
from nicegui.single_page_target import SinglePageTarget

PAGE_TEMPLATE_METHOD_NAME = "page_template"


class Outlet(SinglePageRouterConfig):
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
                 parent: Optional['SinglePageRouterConfig'] = None,
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
        super().__init__(path, browser_history=browser_history, on_instance_created=on_instance_created,
                         on_navigate=on_navigate,
                         router_class=router_class,
                         parent=parent, **kwargs)
        self.outlet_builder: Optional[Callable] = None
        if parent is None:
            Client.single_page_routes[path] = self
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
        if not isinstance(frame, Generator):
            raise ValueError('The outlet builder must be a generator function and contain a yield statement'
                             ' to separate the layout from the content area.')
        properties = {}

        def add_properties(result):
            if isinstance(result, dict):
                properties.update(result)

        router_frame = SinglePageRouter.current_router()
        add_properties(next(frame))  # insert ui elements before yield
        if router_frame is not None:
            router_frame.update_user_data(properties)
        yield properties
        try:
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
            self.setup_pages()
        else:
            relative_path = self.base_path[len(self.parent_config.base_path):]
            OutletView(self.parent_config, relative_path)(outlet_view)
        return self

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


class OutletView:
    """Defines a single view / "content page" which is displayed in an outlet"""

    def __init__(self, parent: SinglePageRouterConfig, path: str, title: Optional[str] = None):
        """
        :param parent: The parent outlet in which this view is displayed
        :param path: The path of the view, relative to the base path of the outlet
        :param title: Optional title of the view. If a title is set, it will be displayed in the browser tab
            when the view is active, otherwise the default title of the application is displayed.
        """
        self.path = path
        self.title = title
        self.parent_outlet = parent

    @property
    def url(self) -> str:
        """The absolute URL of the view

        :return: The absolute URL of the view
        """
        return (self.parent_outlet.base_path.rstrip('/') + '/' + self.path.lstrip('/')).rstrip('/')

    def handle_resolve(self, target: SinglePageTarget, **kwargs) -> SinglePageTarget:
        """Is called when the target is resolved to this view

        :param target: The resolved target
        :return: The resolved target or a modified target
        """
        return target

    def __call__(self, func: Callable[..., Any]) -> Callable[..., Any]:
        """Decorator for the view function"""
        abs_path = self.url
        self.parent_outlet.add_view(
            abs_path, func, title=self.title, on_open=self.handle_resolve)
        return self
