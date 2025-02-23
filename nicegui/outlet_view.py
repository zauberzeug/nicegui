from __future__ import annotations

from typing import TYPE_CHECKING, Any, Callable, Optional

from nicegui.single_page_target import SinglePageTarget

if TYPE_CHECKING:
    from nicegui.content import Content


class OutletView:
    """Defines a single view / "content page" which is displayed in an outlet"""

    def __init__(self, parent: Content, path: str, title: Optional[str] = None):
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
