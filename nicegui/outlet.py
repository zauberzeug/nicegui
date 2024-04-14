from typing import Callable, Any, Self, Optional

from nicegui.single_page_router import SinglePageRouter


class Outlet(SinglePageRouter):
    """An outlet function defines the page layout of a single page application into which dynamic content can be
    inserted. It is a high-level abstraction which manages the routing and content area of the SPA."""

    def __init__(self,
                 path: str,
                 browser_history: bool = True,
                 on_instance_created: Optional[Callable] = None,
                 **kwargs) -> None:
        """
        :param path: the base path of the single page router.
        :param layout_builder: A layout builder function which defines the layout of the page. The layout builder
            must be a generator function and contain a yield statement to separate the layout from the content area.
        :param browser_history: Optional flag to enable or disable the browser history management. Default is True.
        :param on_instance_created: Optional callback which is called when a new instance is created. Each browser tab
        or window is a new instance. This can be used to initialize the state of the application.
        :param parent: The parent outlet of this outlet.
        :param kwargs: Additional arguments for the @page decorators
        """
        super().__init__(path, browser_history=browser_history, on_instance_created=on_instance_created, **kwargs)

    def __call__(self, func: Callable[..., Any]) -> Self:
        """Decorator for the layout builder / "outlet" function"""
        def outlet_view():
            self.setup_content_area()

        self.outlet_builder = func
        if self.parent_router is None:
            self.setup_pages()
        else:
            relative_path = self.base_path[len(self.parent_router.base_path):]
            OutletView(self.parent_router, relative_path)(outlet_view)
        return self

    def view(self, path: str, title: Optional[str] = None) -> 'OutletView':
        """Decorator for the view function
        :param path: The path of the view, relative to the base path of the outlet
        :param title: Optional title of the view. If a title is set, it will be displayed in the browser tab
            when the view is active, otherwise the default title of the application is displayed.
        """
        return OutletView(self, path, title=title)

    def outlet(self, path: str) -> 'Outlet':
        """Defines a nested outlet

        :param path: The relative path of the outlet
        """
        abs_path = self.base_path.rstrip('/') + path
        return Outlet(abs_path, parent=self)


class OutletView:
    """Defines a single view / "content page" which is displayed in an outlet"""

    def __init__(self, parent_outlet: SinglePageRouter, path: str, title: Optional[str] = None):
        """
        :param parent_outlet: The parent outlet in which this view is displayed
        :param path: The path of the view, relative to the base path of the outlet
        :param title: Optional title of the view. If a title is set, it will be displayed in the browser tab
            when the view is active, otherwise the default title of the application is displayed.
        """
        self.path = path
        self.title = title
        self.parent_outlet = parent_outlet

    def __call__(self, func: Callable[..., Any]) -> Callable[..., Any]:
        """Decorator for the view function"""
        self.parent_outlet.add_view(
            self.parent_outlet.base_path.rstrip('/') + self.path, func, title=self.title)
        return func
